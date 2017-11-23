import psycopg2


# Hostname:  aact-prod.cr4nrslb1lw7.us-east-1.rds.amazonaws.com
# Port: 5432
# Database name:  aact
# User name:  aact
# Password:  aact

def save_mesh_term(cur):
    querr = cur.execute("select distinct mesh_term from browse_conditions")
    rows = cur.fetchall()

    file = 'entity_files/mesh_term.csv'
    with open(file, 'w') as f:
        for r in rows:
            f.write("\"%s\", \"%s\"" % (r[0], r[0]))
            f.write('\n')


def save_mesh_interventions(cur):
    querr = cur.execute("select distinct mesh_term from browse_interventions")
    rows = cur.fetchall()

    file = 'entity_files/mesh_term_intervention.csv'
    with open(file, 'w') as f:
        for r in rows:
            f.write("\"%s\", \"%s\"" % (r[0], r[0]))
            f.write('\n')


def save_disease_name(cur):
    querr = cur.execute("select distinct name from conditions")
    rows = cur.fetchall()

    file = 'entity_files/disease_name.csv'
    with open(file, 'w') as f:
        for r in rows:
            f.write("\"%s\", \"%s\"" % (r[0], r[0]))
            f.write('\n')


def save_keywords_name(cur):
    querr = cur.execute("select distinct name from keywords")
    rows = cur.fetchall()

    file = 'entity_files/keywords.csv'
    with open(file, 'w') as f:
        for r in rows:
            f.write("\"%s\", \"%s\"" % (r[0], r[0]))
            f.write('\n')

if __name__ == '__main__':
    conn = psycopg2.connect("dbname='aact' "
                            "user='aact' "
                            "host='aact-prod.cr4nrslb1lw7.us-east-1.rds.amazonaws.com' "
                            "password='aact' "
                            "port=5432")

    cursor = conn.cursor()

    # save_disease_name(cursor)
    # save_mesh_term(cursor)
    # save_keywords_name(cursor)
    save_mesh_interventions(cursor)


