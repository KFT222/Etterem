class Rendeles:
    def __init__(self, asztal, termek_db=[], statusz="függőben"):
        self.asztal=asztal
        self.termek_db=termek_db
        self.statusz=statusz

    def hozzaad(self, termek, db):
        self.termek_db.append((termek, db))

    def zar(self):
        self.statusz="lezárt"



def menu_betolt():
    """Menü(lista) betöltése"""
    menu=[]
    with open("menu.csv", "r", encoding="utf-8") as sorok:
        for sor in sorok:
            sor=sor.strip().split(";")
            if len(sor)<3:
                continue
            sor[2]=int(sor[2])
            menu.append((sor[0], sor[1], sor[2]))
    return menu



def raktar_betolt():
    """raktár(lista) betöltése"""
    raktar=[]
    with open("raktar.csv", "r", encoding="utf-8") as sorok:
        for sor in sorok:
            sor=sor.strip().split(";")
            if len(sor)<2:
                continue
            sor[1]=int(sor[1])  
            raktar.append((sor[0], sor[1]))         
    return raktar



def vasarlasok_betolt():
    """ Vásárlások betöltése;Vásárló neve;Felszolgáló neve;függőben/pénz;termékek"""
    vasarlasok=[]
    with open("vasarlasok.csv", "r", encoding="utf-8") as sorok:
        for sor in sorok:
            sor=sor.strip().split(";")
            if len(sor)<4:
                continue
            if sor[2].isdigit():
                sor[2]=int(sor[2]) 
            vasarlasok.append((sor[0], sor[1], sor[2], sor[3]))         
    return vasarlasok


def raktar_ment(raktar):
     """Raktar mentése a Raktár.csv fájlba"""
    with open("raktar.csv", "w", encoding="utf-8") as sorok:
        for nev, db in raktar:
            sorok.write(f"{nev};{db}\n")


def raktar_csokkent(termek, db, raktar):
    """Raktár csokkentése a Raktar.csv"""
    with open("recept.csv", "r", encoding="utf-8") as f:
        for sor in f:
            etel, alapanyag, menny=sor.strip().split(";")
            menny=int(menny)
            
            if etel==termek:
                for i in range(len(raktar)):
                    if raktar[i][0]==alapanyag:
                        nev, jelenlegi_db=raktar[i]
                        raktar[i]=(nev, jelenlegi_db-menny*db)
                        break


menu=menu_betolt()
raktar=raktar_betolt()
rendelesek=vasarlasok_betolt()

muvelet=input("Mit szeretnél módosítani? (rendelés, menü) ")


# RENDELÉS 

if muvelet=="rendelés":
    felszolgalo_neve=input("Add meg a neved: ")
    vasarlo_neve=input("Vásárló neve: ")
    rendeles=input("Mit szeretnél csinálni (új/hozzáadás, vége) ")

    # ÚJ / HOZZÁADÁS
    if rendeles=="új" or rendeles=="hozzáadás":

        termekek_lista=[]

        # ital
        if input("Ital: (igen/nem) ")=="igen":
            while True:
                ital=input("Ital (0=kilépés): ")
                if ital=="0":
                    break
                db=int(input("Darab: "))
                if db>0:
                    termekek_lista.append(f"{ital}({db})")
                    raktar_csokkent(ital, db, raktar)

        # étel
        if input("Étel: (igen/nem) ")=="igen":
            while True:
                etel=input("Étel (0=kilépés): ")
                if etel=="0":
                    break
                db=int(input("Darab: "))
                if db>0:
                    termekek_lista.append(f"{etel}({db})")
                    raktar_csokkent(etel, db, raktar)

        # desszert
        if input("Desszert: (igen/nem) ")=="igen":
            while True:
                desszert=input("Desszert 0=kilépés: ")
                if desszert=="0":
                    break
                db=int(input("Darab: "))
                if db>0:
                    termekek_lista.append(f"{desszert}({db})")
                    raktar_csokkent(desszert, db, raktar)

        termekek_szoveg=",".join(termekek_lista)

        with open("vasarlasok.csv", "a", encoding="utf-8") as f:
            f.write(f"{vasarlo_neve};{felszolgalo_neve};függőben;{termekek_szoveg}\n")

        raktar_ment(raktar)

    #LEZÁRÁS
    elif rendeles=="vége":

        uj_lista=[]

        for sor in rendelesek:
            if sor[0]==vasarlo_neve and sor[2]=="függőben":

                osszeg=0
                print("\nFizetendő tételek:")

                termekek=sor[3].split(",")

                for t in termekek:
                    nev, db = t.replace(")", "").split("(")
                    db=int(db)

                    for m in menu:
                        if m[1]==nev:
                            resz=m[2]*db
                            osszeg+=resz
                            print(f"{nev} x{db} = {resz} Ft")

                print(f"Összesen: {osszeg} Ft")

                uj_lista.append((sor[0], sor[1], osszeg, sor[3]))
            else:
                uj_lista.append(sor)

        with open("vasarlasok.csv", "w", encoding="utf-8") as f:
            for sor in uj_lista:
                f.write(f"{sor[0]};{sor[1]};{sor[2]};{sor[3]}\n")


#MENÜ

elif muvelet=="menü":
    muv=input("Mit szeretnél csinálni? (új/törlés) ")

    if muv=="új":
        kat=input("Kategória (ital/fő/dessz): ")
        nev=input("Termék neve: ")

        letezik=False
        for sor in menu:
            if sor[1]==nev:
                letezik=True

        if letezik:
            print("Ilyen már van!")
        else:
            ar=input("Ár: ")
            if kat!="ital":
                while True:
                    hozz=input("Hozzávaló (0=kilép): ")
                    if hozz=="0":
                        break
                    menny=input("Mennyiség: ")
                    with open("recept.csv", "a", encoding="utf-8") as recept_fajl:
                        recept_fajl.write(f"{nev};{hozz};{menny}\n")

            with open("menu.csv", "a", encoding="utf-8") as menu_fajl:
                menu_fajl.write(f"{kat};{nev};{ar}\n")

    elif muv=="törlés":
        nev=input("Mit szeretnél törölni? ")

        with open("menu.csv", "r", encoding="utf-8") as fajl:
            sorok=fajl.readlines()

        with open("menu.csv", "w", encoding="utf-8") as fajl:
            for sor in sorok:
                if sor.split(";")[1]!=nev:
                    fajl.write(sor)

        with open("recept.csv", "r", encoding="utf-8") as fajl:
            sorok=fajl.readlines()
        
        with open("recept.csv", "w", encoding="utf-8") as fajl:
            for sor in sorok:
                if sor.split(";")[0]!=nev:
                    fajl.write(sor)
