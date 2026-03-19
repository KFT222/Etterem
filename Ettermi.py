class Rendeles:
    def __init__(self, asztal, termek, db, statusz="függőben"):
        self.asztal = asztal
        self.termek = termek
        self.db = db
        self.statusz = statusz

    def kiir(self, fajl):
        fajl.write(f"{self.asztal};{self.termek};{self.db};{self.statusz}\n")


# Menü betöltése
menu = []
with open("menu.csv", "r", encoding="utf-8") as menu_ki:
    for sor in menu_ki:
        menu.append(sor.strip().split(";"))


# Vásárlások fájl
with open("vasarlasok.csv", "w", encoding="utf-8") as f:
    f.write("asztal;termék;db;státusz\n")

vasarlasok_kiiratas = open("vasarlasok.csv", "a", encoding="utf-8")


muvelet = input("Mit szeretnél módosítani? (rendelés, menü) ")

# RENDELÉS

if muvelet == "rendelés":
    rendeles = input("Mit szeretnél csinálni (új, vége) ")

    if rendeles == "új":
        szam = int(input("Melyik asztal? "))
        while not 1 <= szam <= 12:
            szam = int(input("Melyik asztal? (1-12) "))

        # ital
        if input("Szeretnél italt? (igen/nem) ") == "igen":
            while True:
                ital = input("Ital (víz, fanta, cola) 0=kilépés: ")
                if ital == "0":
                    break
                db = int(input("Darab: "))
                if db > 0:
                    Rendeles(szam, ital, db).kiir(vasarlasok_kiiratas)

        # étel
        if input("Szeretnél ételt? (igen/nem) ") == "igen":
            while True:
                etel = input("Étel (pizza, hamburger, gyros, saláta) 0=kilépés: ")
                if etel == "0":
                    break
                db = int(input("Darab: "))
                if db > 0:
                    Rendeles(szam, etel, db).kiir(vasarlasok_kiiratas)

        # desszert
        if input("Szeretnél desszertet? (igen/nem) ") == "igen":
            while True:
                desszert = input("Desszert 0=kilépés: ")
                if desszert == "0":
                    break
                db = int(input("Darab: "))
                if db > 0:
                    Rendeles(szam, desszert, db).kiir(vasarlasok_kiiratas)

    elif rendeles == "vége":
        asztal = int(input("Melyik asztal fizet? "))

        with open("vasarlasok.csv", "r", encoding="utf-8") as f:
            sorok = f.readlines()

        osszeg = 0
        print("\nFizetendő tételek:")

        for sor in sorok[1:]:
            adat = sor.strip().split(";")

            if int(adat[0]) == asztal:
                termek = adat[1]
                db = int(adat[2])

                for m in menu:
                    if m[1] == termek:  
                        ar = int(m[2])   
                        resz = ar * db
                        osszeg += resz
                        print(f"{termek} x{db} = {resz} Ft")

        print(f"Összesen: {osszeg} Ft")



# MENÜ

elif muvelet == "menü":
    muv = input("Mit szeretnél csinálni? (új, törlés) ")

    if muv == "új":
        kat = input("Kategória (ital, fő, dessz): ")
        nev = input("Termék neve: ")

        # ellenőrzés hogy létezik-e
        letezik = False
        for sor in menu:
            if sor[1] == nev:
                letezik = True

        if letezik:
            print("Ilyen már van!")
        else:
            ar = input("Ár: ")

            # recept ha nem ital
            if kat != "ital":
                alapanyagok = ["paradicsom", "olíviabogyó", "szósz", "hús", "vegyessaláta", "liszt"]

                while True:
                    hozz = input("Hozzávaló (0=kilépés): ")
                    if hozz == "0":
                        break
                    if hozz not in alapanyagok:
                        print("Csak a listából válassz!")
                        continue

                    menny = input("Mennyiség: ")

                    with open("recept.csv", "a", encoding="utf-8") as r:
                        r.write(f"{nev};{hozz};{menny}\n")

            # menübe írás
            with open("menu.csv", "a", encoding="utf-8") as f:
                f.write(f"\n{kat};{nev};{ar}")

    elif muv == "törlés":
        nev = input("Mit szeretnél törölni? ")

        with open("menu.csv", "r", encoding="utf-8") as f:
            sorok = f.readlines()

        with open("menu.csv", "w", encoding="utf-8") as f:
            for sor in sorok:
                if sor.split(";")[1] != nev:
                    f.write(sor)


vasarlasok_kiiratas.close()
