import psycopg2.extras

# Connectie maken met de database

try:
    conn = psycopg2.connect(dbname="Vuilcontainer", user="postgres", host="localhost")
except:
    print("Kan geen verbinding maken met de database.")

# Connectie maken met de python cursor en de tabel/kolommen selecteren uit databse

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
try:
    cur.execute("SELECT * FROM container")
except:
    print("Kan niet selecteren uit container.")

rows = cur.fetchall()
print("Resultaat van de statement:")
for row in rows:
    print("Afstand tot het vuil is " + str(row[1]) + " centimeter. " + "De datum en tijd van de meting vindt plaats op " + str(row[2]) + " om " + str(row[3]) + ".")

# Cursor en connectie sluiten
cur.close()
conn.close()