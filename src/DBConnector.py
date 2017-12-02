import psycopg2
import datetime
from PyQt5.QtCore import QObject, pyqtSignal
from src.LogWindow import logger

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
        'status': location_join
    }
    groups = {
        'geo-city': "facilities.city",
        'geo-country': "facilities.country",
        'disease': "conditions.name",
        'date-period': "EXTRACT(YEAR from studies.start_date)"
    }
    filters = {
        'phase': "studies.phase IN %(phase)s",
        'disease': "conditions.name IN %(disease)s",
        'geo-country': "facilities.country IN %(geo-country)s",
        'geo-city': "facilities.city IN %(geo-city)s",
        'status': "facilities.status IN %(status)s"
    }

    @staticmethod
    def generate_query(parameters, group=['geo-country']):

        join_sqls = set([SQLGenerator.joins[key] for key in list(parameters.keys()) + group if key in SQLGenerator.joins])
        where_sqls = [SQLGenerator.filters[key] for key in parameters.keys() if key in SQLGenerator.filters]

        print(parameters.keys())
        print(where_sqls)
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

        if group is not None:
            sql.extend([
                " GROUP BY ",
            ])
            sql.append(', '.join([SQLGenerator.groups[g] for g in group]))

        print(''.join(sql))
        return ''.join(sql)

    # Will simply convert each param value to a tuple
    @staticmethod
    def convert_params(params):
        new_params = {}
        for k, v in params.items():
            if isinstance(v, tuple):
                new_params[k] = v
            elif isinstance(v, list):
                new_params[k] = tuple(v)
            else:
                new_params[k] = (v,)

        print('NEW_PARAMS')
        print(new_params)
        return new_params

    # Will remove empty lists
    @staticmethod
    def clear_params(params):
        new_params = {}
        for k, v in params.items():
            if isinstance(v, list):
                if len(v) != 0:
                    new_params[k] = v
            else:
                new_params[k] = v

        return new_params


class DBConnector(QObject):
    # Emits a signal whenever database query based on the bot request was successful
    bot_request_processed_signal = pyqtSignal(dict)

    connection_info = "dbname='aact' " \
                      "user='aact' " \
                      "host='aact-prod.cr4nrslb1lw7.us-east-1.rds.amazonaws.com' "\
                      "password='aact' "\
                      "port=5432"

    def __init__(self, parent=None):
        super().__init__(parent)
        self._conn = None

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
    def run_query(self, parameters, group=['geo-country']):
        print(parameters)
        logger.log('Requested to compare countries, query the database')

        query = SQLGenerator.generate_query(parameters, group=group)

        cursor = self.get_cursor()

        cursor.execute(query, SQLGenerator.convert_params(parameters))
        print(cursor.query)
        result = cursor.fetchall()

        print('HELLO')
        print(result)
        parameters["result"] = result


        self.bot_request_processed_signal.emit(parameters)

    # This slot is called when response is received from the DialogFlow bot
    def process_bot_request(self, resolved_query, parameters, contexts, action):
        parameters = SQLGenerator.clear_params(parameters)
        print(action)
        param = self.clear_empty_param(parameters)
        param["action"] = action

        if action == 'compare':
            group_by = []
            for k, v in param.items():
                if isinstance(v, list):
                    group_by.append(k)
            self.run_query(param, group=group_by)

        if action == "count_place":
            self.run_query(param)
        elif action == "count_grouping_country":
            self.run_query(param, group=['geo-country'])
        elif action == "count_grouping_city":
            self.run_query(param, group=['geo-city'])
        elif action == "compare_countries":
            param['geo-country'] = (param['country_first'], param['country_second'])
            self.run_query(param, group='geo-country')
        elif action == "compare_cities":
            print(param['city_first'])
            print(param['city_second'])
            param['geo-city'] = (param['city_first'], param['city_second'])
            self.run_query(param, group='geo-city')

    def clear_empty_param(self, parameters):
        for key, value in list(parameters.items()):
            if value == "":
                del parameters[key]
        return parameters

if __name__ == '__main__':

    #db = DatabaseConnector()
    #db.cur.execute("SELECT facilities.status FROM studies INNER JOIN facilities on studies.nct_id = facilities.nct_id")
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

    param = dict()
    param["geo-country"] = "Germany"
    #param["phase"] = "Recruiting"
    param["disease"] = "Hepatitis C"
#   param["date-period"] = str(datetime.date(2016, 6, 24))
    param2 = dict()
    param2["grouping"] = "Each Country"
    #param2["phase"] = "Phase 1"
    #param2["status"] = "Active, Not Recruiting"
    param2["disease"] = "Hepatitis C"
#   param2["date-period"] = str(datetime.date(2016, 6, 24))
    # 1st question
    test = db.count_grouping(param2)
    for key in test:
        print(key)
        print(test[key])
    # 2st question
    test2 = db.count_place(param)
    for key in test2:
        print(key)
        print(test2[key])

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
