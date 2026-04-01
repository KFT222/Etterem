class Rendeles:
    def __init__(self, vasarlo, felszolgalo, termek_db=[], statusz="függőben"):
        self.vasarlo=vasarlo
        self.felszolgalo=felszolgalo
        self.termek_db=termek_db  #(termék, darabszám)
        self.statusz=statusz

    #új termék hozzáadása a rendeléshez
    def hozzaad(self, termek, db):
        self.termek_db.append((termek, db))

    #rendelés lezárása
    def zar(self):
        self.statusz="lezárt"


#menüt betöltésére szolgáló függvény
def menu_betolt():
    """Menü lista betöltése"""
    menu=[]
    with open("menu.csv", "r", encoding="utf-8") as sorok:
        for sor in sorok:
            sor=sor.strip().split(";")
            if len(sor)<3:
                continue
            sor[2]=int(sor[2])
            menu.append((sor[0], sor[1], sor[2]))
    return menu


#raktár betöltésére szolgáló függvény
def raktar_betolt():
    """Raktár lista betöltése"""
    raktar=[]
    with open("raktar.csv", "r", encoding="utf-8") as sorok:
        for sor in sorok:
            sor=sor.strip().split(";")
            if len(sor)<2:
                continue
            sor[1]=int(sor[1])
            raktar.append((sor[0], sor[1]))
    return raktar


#vásárlások betöltésére szolgáló függvény
def vasarlasok_betolt():
    """Vásárlások betöltése"""
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


#raktár mentése
def raktar_ment(raktar):
    with open("raktar.csv", "w", encoding="utf-8") as sorok:
        for nev, db in raktar:
            sorok.write(f"{nev};{db}\n")


#raktár csökkentése
def raktar_csokkent(termek, db, raktar):
    with open("recept.csv", "r", encoding="utf-8") as fajl:
        for sor in fajl:
            etel, alapanyag, menny = sor.strip().split(";")
            menny=int(menny)
            if etel==termek:
                for i in range(len(raktar)):
                    if raktar[i][0]==alapanyag:
                        nev, jelenlegi_db=raktar[i]
                        szukseges = menny * db
                        if jelenlegi_db >= szukseges:
                            raktar[i] = (nev, jelenlegi_db - szukseges)
                        else:
                            print(f"Nincs elég alapanyag a raktárban!")
                        break


#betöltések
menu=menu_betolt()
raktar=raktar_betolt()
rendelesek=vasarlasok_betolt()

muvelet=input("Mit szeretnél módosítani? (rendelés, menü) ")

if muvelet=="rendelés":
    felszolgalo_neve=input("Add meg a neved: ")
    vasarlo_neve=input("Vásárló neve: ")
    rendeles=input("Mit szeretnél csinálni (új/hozzáadás, vége) ")

    if rendeles in ["új", "hozzáadás"]:
        rend=Rendeles(vasarlo_neve, felszolgalo_neve)
        termekek_lista=[]

        #ital hozzáadása
        if input("Ital: (igen/nem) ")=="igen":
            while True:
                ital=input("Ital (0=kilépés): ")
                if ital=="0":
                    break
                db=int(input("Darab: "))
                if db>0:
                    rend.hozzaad(ital, db)
                    raktar_csokkent(ital, db, raktar)

        #étel hozzáadása
        if input("Étel: (igen/nem) ")=="igen":
            while True:
                etel=input("Étel (0=kilépés): ")
                if etel=="0":
                    break
                db=int(input("Darab: "))
                if db>0:
                    rend.hozzaad(etel, db)
                    raktar_csokkent(etel, db, raktar)

        #desszert hozzáadása
        if input("Desszert: (igen/nem) ")=="igen":
            while True:
                desszert=input("Desszert 0=kilépés: ")
                if desszert=="0":
                    break
                db=int(input("Darab: "))
                if db>0:
                    rend.hozzaad(desszert, db)
                    raktar_csokkent(desszert, db, raktar)

        #rendelés frissítése/hozzáadása
        termekek_szoveg=""  
        for t in rend.termek_db:
            termek_neve=t[0]  
            darabszam=t[1]
            if termekek_szoveg!="":
                termekek_szoveg+=","
            termekek_szoveg+=termek_neve+"("+str(darabszam)+")"
            
        talalt=False
        uj_lista=[]
        for sor in rendelesek:
            if sor[0]==vasarlo_neve and sor[2]=="függőben":
                regi_termekek=sor[3]
                uj_termekek=regi_termekek+","+termekek_szoveg
                uj_lista.append((sor[0], sor[1], sor[2], uj_termekek))
                talalt=True
            else:
                uj_lista.append(sor)

        if not talalt:
            uj_lista.append((vasarlo_neve, felszolgalo_neve, "függőben", termekek_szoveg))

        #fájl újraírása
        with open("vasarlasok.csv", "w", encoding="utf-8") as f:
            for sor in uj_lista:
                f.write(f"{sor[0]};{sor[1]};{sor[2]};{sor[3]}\n")

        raktar_ment(raktar)

    #rendelés lezárása
    elif rendeles=="vége":
        rend=Rendeles(vasarlo_neve, felszolgalo_neve)
    
        for sor in rendelesek:
            if sor[0]==vasarlo_neve and sor[2]=="függőben":
                termekek=sor[3].split(",")
                for t in termekek:
                    nev, db=t.replace(")", "").split("(")
                    rend.hozzaad(nev, db)

        rend.zar()

        #fizetés és összeg számítása
        osszeg=0
        print("\nFizetendő tételek:")
        for nev, db in rend.termek_db:
            for m in menu:
                if m[1]==nev:
                    ar=int(m[2])
                    resz=ar*int(db)
                    osszeg+=resz
            print(f"{nev} x{db} = {resz} Ft")
        print(f"Összesen: {osszeg} Ft")

        #adatok fájlba írása
        uj_lista=[]
        for sor in rendelesek:
                if sor[0]==vasarlo_neve and sor[2]=="függőben":
                    uj_lista.append((sor[0], sor[1], osszeg, sor[3])) 
                else:
                    uj_lista.append(sor)

        with open("vasarlasok.csv", "w", encoding="utf-8") as fajl:
            for sor in uj_lista:
                fajl.write(f"{sor[0]};{sor[1]};{sor[2]};{sor[3]}\n")

#menü kezelése
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
