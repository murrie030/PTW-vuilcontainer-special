from tkinter import *
from tkinter.messagebox import showinfo
import psycopg2.extras
import datetime
import time

# Tkinter root settings

root = Tk()
root.title("Vuilcontainer")
root.configure(background="gray20")
root.iconbitmap("r", "image.ico")

# Schermsettings

window_height = 800
window_width = 800
screen_height = int(root.winfo_screenheight()/2-window_height/2)
screen_width = int(root.winfo_screenwidth()/2-window_width/2)
root.geometry(str(window_width) + "x" + str(window_height) + "+" + str(screen_width) + "+" + str(screen_height))

# Connectie maken met de database

try:
    conn = psycopg2.connect(dbname="Vuilcontainer", user="postgres", host="localhost")
except:
    bericht = "Kan geen verbinding maken met de database."
    showinfo(title="Bericht", message=bericht)

# Connectie maken met de python cursor en de tabel/kolommen selecteren uit database

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
try:
    cur.execute("SELECT * FROM container")
except:
    bericht = "Kan gegevens niet ophalen uit de database."
    showinfo(title="Bericht", message=bericht)

rows = cur.fetchall()

# Functies


def vol_container():
    """"Laat zien wanneer de container voor het laatst is geleegd"""
    container_geleegd = []
    for row in rows:
        if row[1] == 250:
            container_geleegd.append(row[2])

    laats_geleegd = str(container_geleegd[-1]+datetime.timedelta(days=round(aantaldagen)))
    laatste_leging_statement = laats_geleegd[-2] + laats_geleegd[-1] + "-" +\
                               laats_geleegd[5] + laats_geleegd[6] + "-" + laats_geleegd[0] +\
                               laats_geleegd[1] + laats_geleegd[2] + laats_geleegd[3]
    return laatste_leging_statement


def toon_welkoms_frame():
    """Toont het welkomstframe, vergeet de andere frames"""
    welkoms_frame.pack()
    informatie_frame.forget()


def toon_informatie_frame():
    """Toont het informatieframe, vergeet het welkomstframe"""
    welkoms_frame.forget()
    informatie_frame.pack()


def disco_label():
    """Label verandert van kleur naarmate de container voller zit"""
    capaciteit = 100-(laatste_meting[1]/(250/100))
    if capaciteit <= 33:
        return Label(master=outline_capaciteit,
                     text=str(capaciteit) + "%" + " capaciteit bereikt",
                     background="green",
                     foreground="snow",
                     font=("Helvatica", 18, "bold italic"),
                     width="40",
                     height="5")
    elif capaciteit < 66:
        return Label(master=outline_capaciteit,
                     text=str(capaciteit) + "%" + " capaciteit bereikt",
                     background="orange",
                     foreground="snow",
                     font=("Helvatica", 18, "bold italic"),
                     width="40",
                     height="5")
    else:
        return Label(master=outline_capaciteit,
                     text=str(capaciteit) + "%" + " capaciteit bereikt",
                     background="red",
                     foreground="snow",
                     font=("Helvatica", 18, "bold italic"),
                     width="40",
                     height="5")


def tick():
    """Toont de actuele tijd"""
    global time1
    # haalt actuele tijd op van je PC
    time2 = time.strftime("%H:%M:%S")
    # update de tijdsstring als het is veranderd
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)
    # roept zichzelf elke 200 milliseconden aan
    clock.after(200, tick)


dag = [0]


def bereken(totaal, datum, i, oud):
    """Berekent hoeveel vuilnis er gemiddeld bijkomt in de vuilcontainer"""
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
        if rows[i+1][1] > rows[i][1]:
            bereken(250, rows[i][2], i, totaal)
        else:
            bereken(rows[i+1][1], rows[i][2], i, totaal)
        return dag

    except IndexError:
        x = 1+1


dagen = bereken(250, rows[0][2], 0, 0)
perdag = []

for i in range(len(dagen)-1):
    if dagen[i + 1] < dagen[i]:
        i = i+1
    else:

        perdag.append(dagen[i+1]-dagen[i])

gemperdag = sum(perdag)/len(perdag)

aantaldagen = (250-gemperdag/2)/gemperdag
output_algoritme = "De vuilcontainer doet er " + str(round(aantaldagen)) +" dagen over om vol te raken"
output_algoritme_2 = "De eerstvolgende "


# Connectie maken met de python cursor en de tabel/kolommen selecteren uit databse

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
try:
    cur.execute("SELECT * FROM container ORDER BY meting_id ASC")
except:
    bericht = "Kan gegevens niet ophalen uit de database."
    showinfo(title="Bericht", message=bericht)

rows = cur.fetchall()
laatste_meting = (rows[-1])


# Cursor en connectie sluiten

cur.close()
conn.close()


############DIT IS HET WELKOMSFRAME##############
welkoms_frame = Frame(master=root, background="gray20")
welkoms_frame.pack(fill=BOTH, expand=True)

welkomst_label = Label(master=welkoms_frame,
                       text="Welkom bij de Vuilcontainer-Special!",
                       background="gray20",
                       foreground="snow",
                       font=("Helvatica", 23, "bold italic"),
                       width=210,
                       height=4)
welkomst_label.pack(fill=BOTH)
time1 = ""
clock = Label(root, font=("times", 20, "bold"),
              background="gray20",
              foreground="snow")
clock.pack(side=BOTTOM)
welkomst_tekst = Label(master=welkoms_frame,
                       text="Wij zijn de Vuilcontainer-Special en wij zijn professionele ICT'ers.\n "
                            "Onze opdracht is om u informatie te verstrekken over het op \n"
                            " tijd legen van de vuilcontainer.\n"
                            "Wilt u de laatste meting en de uitkomst \n "
                            "van het algoritme zien? Klik dan op de informatieknop.",
                       background="gray20",
                       foreground="snow",
                       font=("Arial", 18),
                       width=210,
                       height=6)
welkomst_tekst.pack()
button1 = Button(master=welkoms_frame,
                 text="Informatie",
                 background="snow",
                 foreground="gray20",
                 bd=2,
                 font=("Arial", 18),
                 relief="raised",
                 command=toon_informatie_frame)
button1.pack(pady=150, padx=20)

############DIT IS HET INFORMATIESFRAME##############
vol = vol_container()
datum = str(laatste_meting[2])
informatie_frame = Frame(master=root, background="gray20")
informatie_frame.pack(fill="both", expand=True)
laatste_meting_label = Label(master=informatie_frame,
                             text="De laatste meting was op " + (datum[-2] + datum[-1] + "-" + datum[-5] + datum[-4] +
                                                                 "-" + datum[:4]) + " om " + str(laatste_meting[3]),
                             background="gray20",
                             foreground="snow",
                             font=("Arial", 18))
laatste_meting_label.pack(pady=20, padx=20)

uitkomst_laatste_meting = Label(master=informatie_frame,
                                text="De gemeten waarde was: " + str(laatste_meting[1]) + " cm.",
                                background="gray20",
                                foreground="snow",
                                font=("Arial", 18))
uitkomst_laatste_meting.pack(pady=40, padx=20)

outline_capaciteit = Label(master=informatie_frame,
                           bd=2,
                           relief="raised")
outline_capaciteit.pack()

capaciteit_vuilcontainer = disco_label()
capaciteit_vuilcontainer.pack()

berekening_algoritme_frame = Label(master=informatie_frame,
                                   text=output_algoritme+"." + "\n "+"\n" + "De container moet geleegd worden op " + vol + ".",
                                   background="gray20",
                                   foreground="snow",
                                   font=("Arial", 18))
berekening_algoritme_frame.pack(pady=60, padx=20)
time1 = ""
clock = Label(root, font=("times", 20, "bold"),
              background="gray20",
              foreground="snow")
clock.pack(side=BOTTOM)
terug_knop = Button(master=informatie_frame,
                    text="Terug",
                    background="snow",
                    foreground="gray20",
                    bd=2,
                    font=("Arial", 18),
                    relief="raised",
                    command=toon_welkoms_frame)
terug_knop.pack(pady=70, padx=20)

tick()
toon_welkoms_frame()
root.mainloop()
