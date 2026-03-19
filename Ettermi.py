class Rendeles:
    def __init__(self, asztal, termek, db, statusz="függőben"):
        self.asztal=asztal
        self.termek=termek
        self.db=db
        self.statusz=statusz
 
    def kiir(self, fajl):
        fajl.write(f"{self.asztal};{self.termek};{self.db};{self.statusz}\n")
 
 
menu_ki=open("menu.csv", "r", encoding="utf-8")
menu=[]
for sor in menu_ki:
    sor=sor.strip().split(";")
    menu.append(sor)
menu_ki.close()
 
 
'''raktar_ki=open("raktar.csv", "r", encoding="utf-8")
raktar=[]
for sor in raktar_ki:
    sor=sor.strip().split(";")
    raktar.append(sor)
raktar_ki.close()
 
 
 
recept_ki=open("recept.csv", "r", encoding="utf-8")
recept=[]
for sor in recept_ki:
    sor=sor.strip().split(";")
    recept.append(sor)
recept_ki.close()'''
 
 
 
vasarlasok_kiiratas=open("vasarlasok.csv", "a", encoding="utf-8")
vasarlasok_kiiratas.write("asztal;termék;db;státusz\n")
 
muvelet=input("Mit szeretnél módosítani? (rendeles, menu)")
if muvelet=="rendeles":
    rendeles=input("Mit szeretnél csinálni (új, hozzáadás, vége) ")
    if rendeles=="új":
        szam=int(input("Melyik asztalhoz akarsz rendelést hozzárendelni? "))
        while not 1<=szam<=12:
            szam=int(input("Melyik asztalhoz akarsz rendelést hozzárendelni? "))
        ital=input("Szeretnél italt hozzáadni? (igen/nem) ")
        if ital=="igen":
            while True:
                ital2=input("Mit szeretnél hozzáadni? (víz, fanta, cola) (ha mégsem 0) ")
                if ital2=="0":
                    break
                db=int(input("Hány darabot? "))
                Rendeles(szam, ital2, db).kiir(vasarlasok_kiiratas)
 
 
        etel=input("Szeretnél ételt hozzáadni? (igen/nem) ")
        if etel=="igen":
            while True:
                etel2=input("Mit szeretnél hozzáadni? (pizza, hamburger, gyros, saláta) (ha mégsem 0) ")
                if etel2=="0":
                    break
                db=int(input("Hány darabot? "))
                Rendeles(szam, etel2, db).kiir(vasarlasok_kiiratas)
 
 
        desszert=input("Szeretnél desszertet hozzáadni? (igen/nem) ")
        if desszert=="igen":
            while True:
                desszert2=input("Mit szeretnél hozzáadni? (ha mégsem 0) ")
                if desszert2=="0":
                    break
                db=int(input("Hány darabot? "))
                Rendeles(szam, desszert2, db).kiir(vasarlasok_kiiratas)
   
    elif rendeles=="hozzáadás":
        szam=int(input("Melyik asztalhoz akarsz rendelést hozzárendelni? "))
        while not 1<=szam<=12:
            szam=int(input("Melyik asztalhoz akarsz rendelést hozzárendelni? "))
        ital=input("Szeretnél italt hozzáadni? (igen/nem) ")
        if ital=="igen":
            while True:
                ital2=input("Mit szeretnél hozzáadni? (víz, fanta, cola) (ha mégsem 0) ")
                if ital2=="0":
                    break
                db=int(input("Hány darabot? "))
                Rendeles(szam, ital2, db).kiir(vasarlasok_kiiratas)
 
    elif rendeles=="vége":
 
        asztal=int(input("Melyik asztal fizet? "))
 
        with open("vasarlasok.csv", "r", encoding="utf-8") as vasarlasok_be:
            sorok=vasarlasok_be.readlines()
 
        osszeg=0
 
        print("\nFizetendő tételek:")
 
        for sor in sorok:
            adat=sor.strip().split(";")
 
            if int(adat[0])==asztal:
 
                termek=adat[1]
                db=int(adat[2])
 
                for m in menu:
                    if m[0]==termek:
                        ar=int(m[1])
                        resz=ar*db
                        osszeg+=resz
 
                        print(f"{termek} x{db} = {resz} Ft")
 
        print(f"Összesen fizetendő: {osszeg} Ft")
elif muvelet=="menu":
    muv=input("Mit szeretnél csinálni? (új, törlés) ")
    if muv=="új":
        plusz=input("Termék neve: ")
        ár=input("Ára: ")
        x=["paradicsom","olíviabogyó","szósz","hús","vegyessaláta","liszt"]
        while True:
            hozzavalok=input("Miből álljon a hozzavalok?: (paradicsom/olíviabogyó/szosz/hus/vegyessalata/liszt) 0=kilepes")
            if hozzavalok==0:
                break
            if hozzavalok not in x:
                hozzavalok=input("Csak a listabol válassz: (paradicsom/olíviabogyó/szosz/hus/vegyessalata/liszt)")
                continue
            mennyiseg=input(f"Mennyi  legyen a(z){hozzavalok}?pl:(100): ")
            with open("recept.csv", "a", encoding="utf-8") as recept:
                recept.write(hozzavalok +(";") + mennyiseg+ "\n")
        
        with open("menu.csv", "a", encoding="utf-8") as hozz:
            hozz.write("\n" + plusz + ";" + ár)

    elif muv=="törlés":
        nev=input("Mit szeretnél törölni? ")
 
        with open("menu.csv", "r", encoding="utf-8") as beolvas:
            sorok=beolvas.readlines()
 
        with open("menu.csv", "w", encoding="utf-8") as f:
            for sor in sorok:
                if sor.split(";")[0] != nev:
                    f.write(sor)
                   
vasarlasok_kiiratas.close()
