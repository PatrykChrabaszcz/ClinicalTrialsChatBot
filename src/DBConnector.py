import pickle

import psycopg2
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSignal

import src.utils as utils
from src.LogWindow import logger
from src.utils import get_subcategories


# Hostname:  aact-prod.cr4nrslb1lw7.us-east-1.rds.amazonaws.com
# Port: 5432
# Database name:  aact
# User name:  aact
# Password:  aact


class SQLGenerator:
    disease_join = "INNER JOIN conditions on studies.nct_id = conditions.nct_id "
    location_join = "INNER JOIN facilities on studies.nct_id = facilities.nct_id "
    joins = {
        'disease': disease_join,
        'geo-city': location_join,
        'geo-country': location_join,
        'status': location_join,
    }
    groups = {
        'geo-city': "facilities.city",
        'geo-country': "facilities.country",
        'disease': "conditions.name",
        'date-period': "EXTRACT(YEAR from studies.start_date)",
        'phase': "studies.phase",
    }
    filters = {
        'phase': "studies.phase IN %(phase)s",
        'disease': "conditions.name IN %(disease)s",
        'geo-country': "facilities.country IN %(geo-country)s",
        'geo-city': "facilities.city IN %(geo-city)s",
        'status': "facilities.status IN %(status)s",
        'date-period': "EXTRACT(YEAR from studies.start_date) in %(date-period)s"
    }

    @staticmethod
    def generate_query(parameters, group=None):
        # We want geo-city and geo-country to be the first element used for grouping
        group = sorted(group, key=lambda x: x != 'geo-city' and x != 'geo-country')
        join_sqls = set(
            [SQLGenerator.joins[key] for key in list(parameters.keys()) + group if key in SQLGenerator.joins])
        where_sqls = [SQLGenerator.filters[key] for key in parameters.keys() if key in SQLGenerator.filters]

        sql = [
            "SELECT ",
            " COUNT(DISTINCT studies.nct_id) "
        ]

        if group is not None:
            sql.extend([
                ", %s " % SQLGenerator.groups[g] for g in group
            ])

        if where_sqls:
            sql.extend([
                "FROM ",
                "studies ",
                " ".join(join_sqls),
                " WHERE ",
                " AND ".join(where_sqls)
            ])
        else:
            sql.extend([
                "FROM ",
                "studies ",
                " ".join(join_sqls)
            ])

        if group is not None and len(group) != 0:
            sql.extend([
                " GROUP BY ",
            ])
            sql.append(', '.join([SQLGenerator.groups[g] for g in group]))

        return ''.join(sql)

    # Will simply convert each param value to a tuple
    @staticmethod
    def convert_params(params):
        new_params = {}
        for k, v in params.items():
            if k == 'geo-country' and isinstance(v, list):
                v = [e.replace('United States of America', 'United States') for e in v]
                v = [e.replace('United Kingdom of Great Britain and Northern Ireland', 'United Kingdom') for e in v]
            if k == 'date-period' and isinstance(v, list):
                v = [i[:4] for i in v]
            elif k == 'date-period':
                v = v[:4]

            if isinstance(v, tuple):
                new_params[k] = v
            elif isinstance(v, list):
                new_params[k] = tuple(v)
            else:
                new_params[k] = (v,)

        return new_params

    # Will remove empty lists
    @staticmethod
    def cleared_params(params):
        new_params = {}
        for k, v in params.items():
            if isinstance(v, list):
                if len(v) != 0:
                    new_params[k] = v
            else:
                if len(v) != 0:
                    new_params[k] = v

        return new_params


class QueryThread(QtCore.QThread):
    def __init__(self, db_connector, parameters, group=None):
        super(QueryThread, self).__init__()
        self.parameters = parameters
        self.group = group
        self.db_connector = db_connector

    def run(self):
        self.db_connector.run_query(self.parameters, self.group)
        self.db_connector.query_thread = None


class DBConnector(QObject):
    A_comp = 'compare'
    A_comp_grp_city = 'compare_grouping_city'
    A_comp_grp_country = 'compare_grouping_country'
    # Emits a signal whenever database query based on the bot request was successful
    bot_request_processed_signal = pyqtSignal([dict, list])

    connection_info = "dbname='aact' " \
                      "user='aact' " \
                      "host='aact-prod.cr4nrslb1lw7.us-east-1.rds.amazonaws.com' " \
                      "password='aact' " \
                      "port=5432"

    def __init__(self, parent=None):
        super().__init__(parent)
        self._conn = None
        self.query_thread = None
        with open(utils.find_data_file("disease_num2name.p"), "rb") as f:
            self.disease_dictionary = pickle.load(f)

    # Connect to the database if connection is not present
    def get_cursor(self):
        if self._conn is None:
            self._connect_first_time()

        try:
            cur = self._conn.cursor()
            cur.execute('SELECT 1')
        except psycopg2.OperationalError:
            self._conn = psycopg2.connect(DBConnector.connection_info)

        return self._conn.cursor()

    def _connect_first_time(self):
        try:
            self._conn = psycopg2.connect(DBConnector.connection_info)
            logger.log("Connected to the database")
        except psycopg2.OperationalError:
            self._conn = None
            logger.log("I am unable to connect to the database")

    # Queries:
    def run_query(self, parameters, group=None):
        logger.log('Requested to compare countries, query the database')

        # If there is a disease in the parameters we need to include all sub-diseases as well
        if 'disease' in parameters:
            diseases = parameters['disease']
            results = []
            for disease in diseases:
                parameters['disease'] = get_subcategories(disease, self.disease_dictionary)
                if 'success_rate' in parameters:
                    parameters['status'] = ["Completed"]
                    query = SQLGenerator.generate_query(parameters, group=group)
                    cursor = self.get_cursor()
                    cursor.execute(query, SQLGenerator.convert_params(parameters))
                    print(cursor.query)
                    completed_studies = cursor.fetchall()
                    parameters['status'] = ["Withdrawn", "Terminated"]
                    query = SQLGenerator.generate_query(parameters, group=group)
                    cursor = self.get_cursor()
                    cursor.execute(query, SQLGenerator.convert_params(parameters))
                    print(cursor.query)
                    failed_studies = cursor.fetchall()
                    results.extend(
                        [r + (disease,) for r in self.calculate_accuracies(completed_studies, failed_studies)])
                else:
                    query = SQLGenerator.generate_query(parameters, group=group)
                    cursor = self.get_cursor()
                    cursor.execute(query, SQLGenerator.convert_params(parameters))
                    print(cursor.query)
                    results.extend([r + (disease,) for r in cursor.fetchall()])
        else:
            query = SQLGenerator.generate_query(parameters, group=group)
            cursor = self.get_cursor()
            cursor.execute(query, SQLGenerator.convert_params(parameters))
            print(cursor.query)
            results = cursor.fetchall()

        '''elif 'success_rate' in parameters:
            diseases = parameters['disease']
            results = []
            for disease in diseases:
                parameters['disease'] = get_subcategories(disease, self.disease_dictionary)
                #parameters['disease'] = get_subcategories((parameters['disease'])[0], self.disease_dictionary)
        '''

        parameters["result"] = results

        print(results)
        self.bot_request_processed_signal.emit(parameters, group)

    # Called to calculate the accuracies of a certain study
    def calculate_accuracies(self, pos_instances, neg_instances):
        results = []
        pos = {}
        neg = {}
        if pos_instances is None or len(pos_instances) == 0:
            return results
        for count, location in pos_instances:
            pos[location] = count
        if neg_instances is not None and len(neg_instances) > 0:
            for count, location in neg_instances:
                neg[location] = count
            for location in pos:
                if location in neg:
                    completed_studies = pos[location]
                    accuracy = (completed_studies / (completed_studies + neg[location])) * 100
                    results.append((accuracy, location))
                else:
                    results.append((100, location))
        else:
            for location in pos:
                results.append((100, location))
        return results

    # This slot is called when response is received from the DialogFlow bot
    def process_bot_request(self, resolved_query, parameters, contexts, action, threaded=True):
        param = SQLGenerator.cleared_params(parameters)
        print(param)
        param["action"] = action

        if action in [DBConnector.A_comp, DBConnector.A_comp_grp_city, DBConnector.A_comp_grp_country]:
            # Find out which parameters have more values and group by them
            group_by = []
            for k, v in param.items():
                # Special case for disease, we need to browse sub-diseases
                if isinstance(v, list) and len(v) > 1 and k != 'disease':
                    group_by.append(k)

            if action == DBConnector.A_comp_grp_city:
                group_by.append('geo-city')

            if action == DBConnector.A_comp_grp_country:
                group_by.append('geo-country')

            if not threaded:
                self.run_query(param, group=list(set(group_by)))
            else:
                self.query_thread = QueryThread(self, param, group=list(set(group_by)))
                self.query_thread.start()


if __name__ == '__main__':
    db = DBConnector()
    c = db.get_cursor()
    c.execute(
        "SELECT COUNT(DISTINCT studies.nct_id) , facilities.city , studies.phase, studies.nct_id FROM studies"
        " INNER JOIN conditions on studies.nct_id = conditions.nct_id  INNER JOIN facilities on "
        "studies.nct_id = facilities.nct_id  WHERE studies.phase IN ('Phase 1', 'Phase 2') AND facilities.country "
        "IN ('Italy') AND conditions.name IN ('Osteoarthritis') GROUP BY facilities.city, studies.phase, studies.nct_id")

    print(c.fetchall())
