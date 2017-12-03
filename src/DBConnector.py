import psycopg2
import datetime
from PyQt5.QtCore import QObject, pyqtSignal
from src.LogWindow import logger
from src.utils import get_subcategories
import pickle
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
        join_sqls = set([SQLGenerator.joins[key] for key in list(parameters.keys()) + group if key in SQLGenerator.joins])
        where_sqls = [SQLGenerator.filters[key] for key in parameters.keys() if key in SQLGenerator.filters]

        sql = [
            "SELECT ",
            " COUNT(DISTINCT studies.nct_id) "
        ]

        if group is not None:
            sql.extend([
                ", %s " % SQLGenerator.groups[g] for g in group
            ])

        sql.extend([
            "FROM ",
            "studies ",
            " ".join(join_sqls),
            " WHERE ",
            " AND ".join(where_sqls)
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
            # Right now we only use start date and year to filter by time
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
                new_params[k] = v

        return new_params


class DBConnector(QObject):

    A_comp = 'compare'
    A_comp_grp_city = 'compare_grouping_city'
    A_comp_grp_country = 'compare_grouping_country'
    # Emits a signal whenever database query based on the bot request was successful
    bot_request_processed_signal = pyqtSignal([dict, list])

    connection_info = "dbname='aact' " \
                      "user='aact' " \
                      "host='aact-prod.cr4nrslb1lw7.us-east-1.rds.amazonaws.com' "\
                      "password='aact' "\
                      "port=5432"

    def __init__(self, parent=None):
        super().__init__(parent)
        self._conn = None
        with open("resources/disease_num2name.p", "rb") as f:
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

        if 'disease' in parameters.keys():
            diseases = parameters['disease']
            results = []
            for disease in diseases:
                parameters['disease'] = get_subcategories(disease, self.disease_dictionary)
                query = SQLGenerator.generate_query(parameters, group=group)
                cursor = self.get_cursor()
                cursor.execute(query, SQLGenerator.convert_params(parameters))
                print(cursor.query)
                results.extend([r + (disease,) for r in cursor.fetchall()])
        elif 'success_rate' in parameters.keys():
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
            results = self.calculate_accuracies(completed_studies, failed_studies)

        else:
            query = SQLGenerator.generate_query(parameters, group=group)
            cursor = self.get_cursor()
            cursor.execute(query, SQLGenerator.convert_params(parameters))
            print(cursor.query)
            results = cursor.fetchall()

        parameters["result"] = results

        print(results)
        self.bot_request_processed_signal.emit(parameters, group)

    # Called to calculate the accuracies of a certain study
    def calculate_accuracies(self, pos_instances, neg_instances):
        results = []
        pos = {}
        neg = {}
        if pos_instances == None or len(pos_instances) == 0:
            return results
        for count, location in pos_instances:
            pos[location] = count
        if neg_instances != None and len(neg_instances) > 0:
            for count, location in neg_instances:
                neg[location] = count
            for location in pos_instances:
                if location in neg_instances:
                    completed_studies = pos_instances[location]
                    accuracy = (completed_studies / (completed_studies + neg_instances[location])) * 100
                    results.append(location, accuracy)
                else:
                    results.append(location, 100)
        else:
            for location in dict:
                results.append((100, location))

        return results

    # This slot is called when response is received from the DialogFlow bot
    def process_bot_request(self, resolved_query, parameters, contexts, action):
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

            self.run_query(param, group=list(set(group_by)))

if __name__ == '__main__':

    db = DBConnector()
    c = db.get_cursor()
    c.execute("SELECT COUNT(DISTINCT studies.nct_id) , facilities.city , studies.phase, studies.nct_id FROM studies INNER JOIN conditions on studies.nct_id = conditions.nct_id  INNER JOIN facilities on studies.nct_id = facilities.nct_id  WHERE studies.phase IN ('Phase 1', 'Phase 2') AND facilities.country IN ('Italy') AND conditions.name IN ('Osteoarthritis') GROUP BY facilities.city, studies.phase, studies.nct_id")

    print(c.fetchall())

    #result = db.cur.fetchmany(150)
    #for line in result:
    #    print(line)
    #
    # # 1st question
    # result = db.count(disease='Hepatitis C', location=None, location_modifier='each country', phase='Phase 2',
    #                   status='active')
    # print(result)
    #
    # result = db.count(disease='Lung Cancer', status='recruiting', location_modifier='different regions',
    #                   location='France')
    # print(result)
    #
    #

    # may comment out, but don't delete
#
#     param = dict()
#     param["geo-country"] = "Germany"
#     #param["phase"] = "Recruiting"
#     param["disease"] = "Hepatitis C"
# #   param["date-period"] = str(datetime.date(2016, 6, 24))
#     param2 = dict()
#     param2["grouping"] = "Each Country"
#     #param2["phase"] = "Phase 1"
#     #param2["status"] = "Active, Not Recruiting"
#     param2["disease"] = "Hepatitis C"
# #   param2["date-period"] = str(datetime.date(2016, 6, 24))
#     # 1st question
#     test = db.count_grouping(param2)
#     for key in test:
#         print(key)
#         print(test[key])
#     # 2st question
#     test2 = db.count_place(param)
#     for key in test2:
#         print(key)
#         print(test2[key])

'''
    # TODO: the missing entries are not handled yet
    querr = db.cur.execute("select distinct mesh_term from browse_conditions")  # what about names from conditions?
    rows = db.cur.fetchall()

    file = "..\\resources\\disease_names.txt"
    with open(file) as f:
        diseases = f.readlines()
        diseases = list(map(lambda x: x.split('\"')[1], diseases))

    res = []
    not_contained = []
    for r in rows:
        value = r[0] in diseases
        res.append(value)
        if not value:
            not_contained.append(r[0])

    print("Contains {0} / {1}".format(sum(res), len(rows)))
    # TODO: see here
    for t in not_contained:
        print(t)
'''
