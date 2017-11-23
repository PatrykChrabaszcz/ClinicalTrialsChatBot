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


if __name__ == '__main__':
    db = DatabaseConenctor()
    querr = db.cur.execute("select distinct nct_id from studies")
    rows = db.cur.fetchall()
    for r in rows:
        print(r)
    print(len(rows))
