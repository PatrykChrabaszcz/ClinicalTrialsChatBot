import psycopg2
import datetime
from PyQt5.QtCore import QObject, pyqtSignal


# Hostname:  aact-prod.cr4nrslb1lw7.us-east-1.rds.amazonaws.com
# Port: 5432
# Database name:  aact
# User name:  aact
# Password:  aact


class DatabaseConnector(QObject):
    database_response = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        try:
            self.conn = psycopg2.connect("dbname='aact' "
                                         "user='aact' "
                                         "host='aact-prod.cr4nrslb1lw7.us-east-1.rds.amazonaws.com' "
                                         "password='aact' "
                                         "port=5432")
        except:
            self.conn = None
            print("I am unable to connect to the database")

        self.cur = self.conn.cursor()

    def count_place(self, parameters):

        select_part = ["SELECT COUNT(*)"]
        from_part = [" FROM studies"]
        where_part = [" WHERE"]
        add_and = False
        if "date-period" in parameters:
            value = parameters["date-period"]
            if add_and:
                where_part.append("AND studies.start_date <= '" + value + "'" + " AND studies.completion_date >= '" + value + "'")
            else:
                add_and = True
                where_part.append("studies.start_date <= '" + value + "'" + " AND studies.completion_date >= '" + value + "'")
        if "disease" in parameters:
            value = parameters["disease"]
            from_part.append("INNER JOIN conditions on studies.nct_id = conditions.nct_id")
            if add_and:
                where_part.append("AND conditions.name = '" + value + "'")
            else:
                add_and = True
                where_part.append("conditions.name = '" + value + "'")

        if "phase" in parameters:
            value = parameters["phase"]
            if add_and:
                where_part.append("AND studies.phase = '" + value + "'")
            else:
                add_and = True
                where_part.append("studies.phase = '" + value + "'")
        if "geo-country" in parameters:
            value = parameters["geo-country"]
            from_part.append("INNER JOIN facilities on studies.nct_id = facilities.nct_id")
            if "status" in parameters:
                value2 = parameters["status"]
                if add_and:
                    where_part.append("AND facilities.country = '" + value + "'" + " AND facilities.status = '" + value2 + "'")
                else:
                    add_and = True
                    where_part.append("facilities.country = '" + value + "'" + " AND facilities.status = '" + value2 + "'")
            else:
                if add_and:
                    where_part.append("AND facilities.country = '" + value + "'")
                else:
                    add_and = True
                    where_part.append("facilities.country = '" + value + "'")
        if "geo-city" in parameters:
            value = parameters["geo-city"]
            from_part.append("INNER JOIN facilities on studies.nct_id = facilities.nct_id")
            if "status" in parameters:
                value2 = parameters["status"]
                if add_and:
                    where_part.append("AND facilities.city = '" + value + "'" + " AND facilities.status = '" + value2 + "'")
                else:
                    where_part.append("facilities.city = '" + value + "'" + " AND facilities.status = '" + value2 + "'")
            else:
                if add_and:
                    where_part.append("AND facilities.city = '" + value + "'")
                else:
                    where_part.append("facilities.city = '" + value + "'")

        print("".join(select_part) + " ".join(from_part) + " ".join(where_part) + ";")
        self.cur.execute("".join(select_part) + " ".join(from_part) + " ".join(where_part) + ";")
        result = self.cur.fetchall()

        print(result)
        self.database_response.emit(result)

        for line in result:
            print(line)

    def count_grouping(self, parameters):

        select_part = ["SELECT COUNT(*)"]
        from_part = [" FROM studies"]
        where_part = [" WHERE"]
        add_and = False
        group_part = [" GROUP BY"]
        if "date-period" in parameters:
            value = parameters["date-period"]
            if add_and:
                where_part.append("AND studies.start_date <= '" + value + "'" + " AND studies.completion_date >= '" + value + "'")
            else:
                add_and = True
                where_part.append("studies.start_date <= '" + value + "'" + " AND studies.completion_date >= '" + value + "'")
        if "disease" in parameters:
            value = parameters["disease"]
            from_part.append("INNER JOIN conditions on studies.nct_id = conditions.nct_id")
            if add_and:
                where_part.append("AND conditions.name = '" + value + "'")
            else:
                add_and = True
                where_part.append("conditions.name = '" + value + "'")

        if "phase" in parameters:
            value = parameters["phase"]
            if add_and:
                where_part.append("AND studies.phase = '" + value + "'")
            else:
                add_and = True
                where_part.append("studies.phase = '" + value + "'")
        if "grouping" in parameters:
            select_part.append(",facilities.country")
            from_part.append("INNER JOIN facilities on studies.nct_id = facilities.nct_id")
            group_part.append("facilities.country")
            if "status" in parameters:
                value2 = parameters["status"]
                if add_and:
                    where_part.append("AND facilities.status = '" + value2 + "'")
                else:
                    where_part.append("facilities.status = '" + value2 + "'")
        print("".join(select_part) + " ".join(from_part) + " ".join(where_part) + " ".join(group_part) + ";")
        self.cur.execute("".join(select_part) + " ".join(from_part) + " ".join(where_part) + " ".join(group_part) + ";")
        result = self.cur.fetchall()

        print(result)
        self.database_response.emit(result)
        for line in result:
            print(line)

    # This slot is called when response is received from the DialogFlow bot
    def dialogflow_response(self, resolved_query, parameters, contexts, action):
        param = self.clear_empty_param(parameters)
        if action == "count_place":
            self.count_place(param)
        elif action == "count_grouping":
            self.count_grouping(param)


    def clear_empty_param(self, parameters):
        for key, value in list(parameters.items()):
            if value == "":
                del parameters[key]
        return parameters

if __name__ == '__main__':

    db = DatabaseConnector()
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
    param["phase"] = "Phase 2"
    param["status"] = "Active"
    param["disease"] = "Hepatitis C"
    #param["date-period"] = str(datetime.date(2016, 6, 24))
    param2 = dict()
    param2["grouping"] = "Each Country"
    param2["phase"] = "Phase 2"
    param2["status"] = "Active"
    param2["disease"] = "Hepatitis C"
    #param2["date-period"] = str(datetime.date(2016, 6, 24))
    db.count_grouping(param2)
    # 1st question
    db.count_place(param)

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