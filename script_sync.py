#!.venv/bin/python3
import re, datetime, sqlite3, time, mysql
from mysql import connector

# Variables
domains = []
mxhero_name = "MxHero" # The name of MxHero on the AdSync

# Connect Mysql
try:
    cnx = mysql.connector.connect(
        user='user_mxhero',
        password='password_mxhero',
        host='mxhero_hostname.domain.com.br',
        database='mxhero'
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

cursor_mysql = cnx.cursor()
query = ("SELECT domain FROM domain")
cursor_mysql.execute(query)

for ( domain ) in cursor_mysql:
    domains.append(domain)

for domain in domains:
    str_domain = ''.join(domain)
    print(re.sub('[(),]', '', str_domain))

cursor_mysql.close()
cnx.close()


# Connect SQLITE3
conn = sqlite3.connect('db.sqlite3')
cursor_sqlite = conn.cursor()

# Query Base
# SELECT DISTINCT * FROM django_celery_beat_periodictask WHERE args LIKE '["Labinova", "testelite.velop.com"]';

for domain in domains:
    date_now = datetime.datetime.now()
    str_domain = ''.join(domain)
    styled_domain = re.sub('[(),]', '', str_domain)
    cursor_sqlite.execute("SELECT DISTINCT * FROM django_celery_beat_periodictask WHERE args LIKE '[\"Labinova\", \"{domain}\"]';".format(domain=styled_domain))
    results = cursor_sqlite.fetchall()
    if results != []:
        print(results)
    else:
        try:
            print("Domain {domain} not sincronized".format(domain=styled_domain))
            print("Synchronizing domain {domain} in the Adsync".format(domain=styled_domain))
            cursor_sqlite.execute("INSERT INTO django_celery_beat_periodictask (name, task, args, kwargs, enabled, interval_id, start_time, total_run_count, date_changed, description, one_off) VALUES(\"%(d)s\", 'db_instances.tasks.adsync_task', '[\"%(m)s\", \"%(d)s\"]', '{}', 1, 1, \"%(s)s\", 1, \"%(s)s\", \"\", 0);" % {'d': styled_domain, 's': date_now, 'm': mxhero_name})
            time.sleep(3)
        except:
            print("Domain registered in Django.")

conn.commit()
cursor_sqlite.close()
conn.close()
