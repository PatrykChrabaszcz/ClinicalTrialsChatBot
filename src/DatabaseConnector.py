import psycopg2

# Hostname:  aact-prod.cr4nrslb1lw7.us-east-1.rds.amazonaws.com
# Port: 5432
# Database name:  aact
# User name:  aact
# Password:  aact


class DatabaseConenctor:
    def __init__(self):
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

    def count(self, disease=None, location=None, location_modifier=None, phase=None,
              status=None, time=None, time_modifier=None, drug=None):

        pass

if __name__ == '__main__':
    db = DatabaseConenctor()

    # 1st question
    result = db.count(disease='Hepatitis C', location=None, location_modifier='each country', phase='Phase 2',
                      status='active')
    print(result)

    result = db.count(disease='Lung Cancer', status='recruiting', location_modifier='different regions',
                      location='France')
    print(result)




    # querr = db.cur.execute("select distinct mesh_term from browse_conditions")
    # rows = db.cur.fetchall()
    #
    # file = 'dis'
    # for r in rows:
    #     print(r)
    # print(len(rows))
