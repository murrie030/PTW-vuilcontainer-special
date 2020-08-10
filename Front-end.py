from tkinter import *

root = Tk()                     # Creëer het hoofdschermroot
root.title("Vuilcontainer")
root.geometry("900x800")
root.configure(background="forest green")


def toon_welkomst_frame():
    """Toont het welkomstframe, vergeet de andere frames"""
    welkomst_frame.pack()
    #informatie_fram.forget()


############Welkomstframe##############
welkomst_frame = Frame(master=root, background="forest green")
welkomst_frame.pack(fill=BOTH, expand=True)

welkomst_label = Label(master=welkomst_frame,
                       text="Welkom bij de Vuilcontainer-Special!",
                       background="forest green",
                       foreground="snow",
                       font=("Helvetica", 23, "bold italic"),
                       width=210,
                       height=4)
welkomst_label.pack(fill=BOTH)
button1 = Button(master=welkomst_frame,
                    text="Informatie",
                    font="helvetica 24",
                    foreground="forest green",
                    background="snow",
                    bd=2,
                    relief="raised",
                    command=toon_welkomst_frame)
button1.pack(pady=20, padx=20)


toon_welkomst_frame()
root.mainloop()