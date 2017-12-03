import psycopg2
import datetime
from PyQt5.QtCore import QObject, pyqtSignal


# Hostname:  aact-prod.cr4nrslb1lw7.us-east-1.rds.amazonaws.com
# Port: 5432
# Database name:  aact
# User name:  aact
# Password:  aact


class DatabaseConnector(QObject):

    # Emits a signal whenever database query based on the bot request was successful
    bot_request_processed_signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
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

        select_part = ["SELECT COUNT(DISTINCT studies.nct_id)"]
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
        elif "geo-city" in parameters:
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
        result = self.cur.fetchone()
        print(result)
        count = result[0]
        parameters["result"] = count
        self.bot_request_processed_signal.emit(parameters)
        return parameters

    def count_grouping_country(self, parameters):

        select_part = ["SELECT COUNT(DISTINCT studies.nct_id)"]
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
        count_results = {}
        for value, location in result:
            count_results[location] = value

        parameters["result"] = count_results
        self.bot_request_processed_signal.emit(parameters)
        return parameters

    def count_grouping_city(self, parameters):

        select_part = ["SELECT COUNT(DISTINCT studies.nct_id)"]
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
        if "grouping_local" in parameters:
            select_part.append(",facilities.city")
            from_part.append("INNER JOIN facilities on studies.nct_id = facilities.nct_id")
            group_part.append("facilities.city")
            value = parameters["geo-country"]
            if add_and:
                where_part.append("And facilities.country = '" + value + "'")
            else:
                where_part.append("facilities.country = '" + value + "'")
            if "status" in parameters:
                value2 = parameters["status"]
                where_part.append("AND facilities.status = '" + value2 + "'")


        print("".join(select_part) + " ".join(from_part) + " ".join(where_part) + " ".join(group_part) + ";")
        self.cur.execute("".join(select_part) + " ".join(from_part) + " ".join(where_part) + " ".join(group_part) + ";")
        result = self.cur.fetchall()
        print(result)
        count_results = {}
        for value, location in result:
            count_results[location] = value

        parameters["result"] = count_results
        self.bot_request_processed_signal.emit(parameters)
        return parameters

    def compare_cities(self, parameters):

        select_part = ["SELECT COUNT(DISTINCT studies.nct_id)"]
        from_part = [" FROM studies"]
        where_part = [" WHERE"]
        group_part = [" GROUP BY"]
        value = parameters["city_first"]
        value2 = parameters["city_second"]
        select_part.append(", facilities.city")
        from_part.append("INNER JOIN facilities on studies.nct_id = facilities.nct_id")
        group_part.append("facilities.city")
        where_part.append("(facilities.city = '" + value + "'" + " Or facilities.city = '" + value2 + "')")
        value = parameters["disease"]
        from_part.append("INNER JOIN conditions on studies.nct_id = conditions.nct_id")
        where_part.append("AND conditions.name = '" + value + "'")
        if "status" in parameters:
            value = parameters["status"]
            where_part.append("AND facilities.status = '" + value + "'")
        if "date-period" in parameters:
            value = parameters["date-period"]
            where_part.append("AND studies.start_date <= '" + value + "'" + " AND studies.completion_date >= '" + value + "'")
        if "phase" in parameters:
            value = parameters["phase"]
            where_part.append("AND studies.phase = '" + value + "'")

        print("".join(select_part) + " ".join(from_part) + " ".join(where_part) + " ".join(group_part) + ";")
        self.cur.execute("".join(select_part) + " ".join(from_part) + " ".join(where_part) + " ".join(group_part) + ";")
        result = self.cur.fetchall()
        print(result)
        count_results = {}
        for value, location in result:
            count_results[location] = value
        parameters["result"] = count_results
        self.bot_request_processed_signal.emit(parameters)
        return parameters

    def compare_countries(self, parameters):

        select_part = ["SELECT COUNT(DISTINCT studies.nct_id)"]
        from_part = [" FROM studies"]
        where_part = [" WHERE"]
        group_part = [" GROUP BY"]
        value = parameters["country_first"]
        value2 = parameters["country_second"]
        select_part.append(", facilities.country")
        from_part.append("INNER JOIN facilities on studies.nct_id = facilities.nct_id")
        group_part.append("facilities.country")
        where_part.append("(facilities.country = '" + value + "'" + " Or facilities.country = '" + value2 + "')")
        value = parameters["disease"]
        from_part.append("INNER JOIN conditions on studies.nct_id = conditions.nct_id")
        where_part.append("AND conditions.name = '" + value + "'")
        if "status" in parameters:
            value = parameters["status"]
            where_part.append("AND facilities.status = '" + value + "'")
        if "date-period" in parameters:
            value = parameters["date-period"]
            where_part.append("AND studies.start_date <= '" + value + "'" + " AND studies.completion_date >= '" + value + "'")
        if "phase" in parameters:
            value = parameters["phase"]
            where_part.append("AND studies.phase = '" + value + "'")

        print("".join(select_part) + " ".join(from_part) + " ".join(where_part) + " ".join(group_part) + ";")
        self.cur.execute("".join(select_part) + " ".join(from_part) + " ".join(where_part) + " ".join(group_part) + ";")
        result = self.cur.fetchall()
        print(result)
        count_results = {}
        for value, location in result:
            count_results[location] = value
        parameters["result"] = count_results
        self.bot_request_processed_signal.emit(parameters)
        return parameters

    def compare_diseases(self, parameters):

        select_part = ["SELECT COUNT(DISTINCT studies.nct_id)"]
        from_part = [" FROM studies"]
        where_part = [" WHERE"]
        group_part = [" GROUP BY"]
        value = parameters["disease_first"]
        value2 = parameters["disease_second"]
        select_part.append(", conditions.name")
        from_part.append("INNER JOIN conditions on studies.nct_id = conditions.nct_id")
        where_part.append("(conditions.name = '" + value + "'" + " Or conditions.name = '" + value2 + "')")
        group_part.append(" conditions.name")
        if "geo-country" in parameters:
            value = parameters["geo-country"]
            from_part.append("INNER JOIN facilities on studies.nct_id = facilities.nct_id")
            if "status" in parameters:
                value2 = parameters["status"]
                where_part.append("AND facilities.country = '" + value + "'" + " AND facilities.status = '" + value2 + "'")
            else:
                where_part.append("AND facilities.country = '" + value + "'")
        if "geo-city" in parameters:
            value = parameters["geo-city"]
            from_part.append("INNER JOIN facilities on studies.nct_id = facilities.nct_id")
            if "status" in parameters:
                value2 = parameters["status"]
                where_part.append("AND facilities.city = '" + value + "'" + " AND facilities.status = '" + value2 + "'")
            else:
                where_part.append("AND facilities.city = '" + value + "'")
        if "date-period" in parameters:
            value = parameters["date-period"]
            where_part.append("AND studies.start_date <= '" + value + "'" + " AND studies.completion_date >= '" + value + "'")
        if "phase" in parameters:
            value = parameters["phase"]
            where_part.append("AND studies.phase = '" + value + "'")
        print("".join(select_part) + " ".join(from_part) + " ".join(where_part) + " ".join(group_part) + ";")
        self.cur.execute("".join(select_part) + " ".join(from_part) + " ".join(where_part) + " ".join(group_part) + ";")
        result = self.cur.fetchall()
        print(result)
        count_results = {}
        for value, location in result:
            count_results[location] = value
        parameters["result"] = count_results
        self.bot_request_processed_signal.emit(parameters)
        return parameters

    def compare_phases(self, parameters):
        select_part = ["SELECT COUNT(DISTINCT studies.nct_id)"]
        from_part = [" FROM studies"]
        where_part = [" WHERE"]
        group_part = [" GROUP BY"]
        value = parameters["phase_first"]
        value2 = parameters["phase_second"]
        select_part.append(", studies.phase")
        where_part.append("(studies.phase = '" + value + "'" + " Or studies.phase = '" + value2 + "')")
        group_part.append(" studies.phase")
        value = parameters["disease"]
        from_part.append("INNER JOIN conditions on studies.nct_id = conditions.nct_id")
        where_part.append("AND conditions.name = '" + value + "'")
        if "geo-country" in parameters:
            value = parameters["geo-country"]
            from_part.append("INNER JOIN facilities on studies.nct_id = facilities.nct_id")
            if "status" in parameters:
                value2 = parameters["status"]
                where_part.append(
                    "AND facilities.country = '" + value + "'" + " AND facilities.status = '" + value2 + "'")
            else:
                where_part.append("AND facilities.country = '" + value + "'")
        if "geo-city" in parameters:
            value = parameters["geo-city"]
            from_part.append("INNER JOIN facilities on studies.nct_id = facilities.nct_id")
            if "status" in parameters:
                value2 = parameters["status"]
                where_part.append("AND facilities.city = '" + value + "'" + " AND facilities.status = '" + value2 + "'")
            else:
                where_part.append("AND facilities.city = '" + value + "'")
        if "date-period" in parameters:
            value = parameters["date-period"]
            where_part.append("AND studies.start_date <= '" + value + "'" + " AND studies.completion_date >= '" + value + "'")
        print("".join(select_part) + " ".join(from_part) + " ".join(where_part) + " ".join(group_part) + ";")
        self.cur.execute("".join(select_part) + " ".join(from_part) + " ".join(where_part) + " ".join(group_part) + ";")
        result = self.cur.fetchall()
        print(result)
        count_results = {}
        for value, location in result:
            count_results[location] = value
        parameters["result"] = count_results
        self.bot_request_processed_signal.emit(parameters)
        return parameters
    # This slot is called when response is received from the DialogFlow bot
    def process_bot_request(self, resolved_query, parameters, contexts, action):
        print(action)
        param = self.clear_empty_param(parameters)
        param["action"] = action
        if action == "count_place":
            self.count_place(param)
        elif action == "count_grouping_country":
            self.count_grouping_country(param)
        elif action == "count_grouping_city":
            self.count_grouping_city(param)
        elif action == "compare_cities":
            self.compare_cities(param)
        elif action == "compare_countries":
            self.compare_cities(param)
        elif action == "compare_diseases":
            self.compare_diseases(param)
        elif action == "compare_phases":
            self.compare_phases(param)

    def clear_empty_param(self, parameters):
        for key, value in list(parameters.items()):
            if value == "":
                del parameters[key]
        return parameters

if __name__ == '__main__':



    db = DatabaseConnector()
    db.cur.execute("SELECT outcomes.population from outcomes")
    result = db.cur.fetchall()
    dict = {}
    print(len(result))
    for line in result:
        dict[line[0]] = True
    print(len(dict))
    for key in dict:
        print(key)
    '''
    db.cur.execute("SELECT * FROM studies WHERE studies.nct_id = 'NCT03144440'")
    result = db.cur.fetchone()
    print(2)
    print(result)
    '''
    """
    db.cur.execute("SELECT facilities.status FROM studies INNER JOIN facilities on studies.nct_id = facilities.nct_id")
    result = db.cur.fetchall()
    test_values = {}
    for line in result:
        test_values[line] = True
    for key in test_values:
        print(key)
    """
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

'''
    param = dict()
    param["disease"] = "Melanoma"
    param["phase_first"] = "Phase 1"
    param["phase_second"] = "Phase 2"
    param["status"] = ""
    param["geo-city"] = "London"
    param["date-period"] = str(datetime.date(2016, 6, 24))
    # 1st question
    test2 = db.compare_phases(param)
    for key in test2:
        print(key)
        print(test2[key])
'''
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
