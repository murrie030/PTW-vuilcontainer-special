import psycopg2.extras

# Connectie maken met de database

try:
    conn = psycopg2.connect(dbname="Vuilcontainer", user="postgres", host="localhost")
except:
    print("Kan geen verbinding maken met de database.")

# Connectie maken met de python cursor en de tabel/kolommen selecteren uit databse

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
try:
    cur.execute("SELECT * from container")
except:
    print("Kan niet selecteren uit container.")

rows = cur.fetchall()
        #print("Resultaat van de statement:")
        #for row in rows:
        #    print("Meting: " + str(row[0]) + ". " + "Aantal cm van het vuil: " + str(row[1])+". ")


dag = [0]
print(len(dag))
def bereken(totaal, datum, i,oud):
    try:
        for row in rows:
            if datum == rows[i][2]:
                totaal = 250 - rows[i][1]
                i = i + 1
            elif rows[i][2] > datum:
                dag.append(totaal)
                break
            else:
                break
        gem = totaal / i
        print('Er is in totaal: '+str(totaal)+'cm af gegaan.')
        print('Per keer is er gemiddeld: '+str(gem)+'cm aan vuil bij gekomen.')
        gemiddelde = []
        gemiddelde.append(gem)
        print('er waren',i,'metingen')
        bereken(totaal,rows[i][2],i,totaal)

        return dag

    except IndexError:
            print('dat was alles')


dagen = bereken(250,rows[0][2],0,0)
print('hoeveel heid vuil aan het einde van die dag',dagen)

perdag = [dagen[i + 1] - dagen[i] for i in range(len(dagen) - 1)]
print('hoeveelheid vuil per dag', perdag)

gemperdag = sum(perdag)/len(perdag)
print('het gemiddelde per dag is:', gemperdag)

aantaldagen = (250-gemperdag/2)/gemperdag
print('(250 - gemperdag/2)/gemperdag =', aantaldagen)
print('dus het moet om de', round(aantaldagen),'geleegd worden')


# Cursor en connectie sluiten
cur.close()
conn.close()
