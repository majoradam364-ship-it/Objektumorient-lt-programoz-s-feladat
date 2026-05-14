from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class Auto(ABC):
    def __init__(self, rendszam: str, tipus: str, berleti_dij: int):
        self._rendszam = rendszam
        self._tipus = tipus
        self._berleti_dij = berleti_dij

    @property
    def rendszam(self):
        return self._rendszam
    
    @property
    def tipus(self):
        return self._tipus
    
    @property
    def berleti_dij(self):
        return self._berleti_dij

class Szemelyauto(Auto):
    def __init__(self, rendszam: str, tipus: str, berleti_dij: int, utasok_szama: int):
        super().__init__(rendszam, tipus, berleti_dij)
        self._utasok_szama = utasok_szama
        
    @property
    def utasok_szama(self):
        return self._utasok_szama

class Teherauto(Auto):
    def __init__(self, rendszam: str, tipus: str, berleti_dij: int, teherbiras_kg: int):
        super().__init__(rendszam, tipus, berleti_dij)
        self._teherbiras_kg = teherbiras_kg
        
    @property
    def teherbiras_kg(self):
        return self._teherbiras_kg

class Berles:
    def __init__(self, auto: Auto, datum: datetime.date):
        self._auto = auto
        self._datum = datum
        
    @property
    def auto(self):
        return self._auto
        
    @property
    def datum(self):
        return self._datum

class Autokolcsonzo:
    def __init__(self, nev: str):
        self._nev = nev
        self._autok = []
        self._berlesek = []
        
    @property
    def nev(self):
        return self._nev
        
    @property
    def autok(self):
        return self._autok
        
    @property
    def berlesek(self):
        return self._berlesek
        
    def auto_hozzaadasa(self, auto: Auto):
        self._autok.append(auto)
        
    def berles(self, rendszam: str, datum: datetime.date):
        # Hibakezelés: van ilyen autó?
        auto = next((a for a in self._autok if a.rendszam == rendszam), None)
        if not auto:
            raise ValueError(f"Nincs ilyen rendszámú autó a kölcsönzőben: {rendszam}")
        
        # Hibakezelés: visszamenőleg nem bérelhetünk
        if datum < datetime.today().date():
            raise ValueError("Visszamenőleg nem lehet autót bérelni. Kérem adjon meg jövőbeli vagy mai dátumot.")
            
        # Hibakezelés: adott napon már ki van bérelve?
        for b in self._berlesek:
            if b.auto.rendszam == rendszam and b.datum == datum:
                raise ValueError(f"Az autó ({rendszam}) a megadott napon ({datum}) már ki van bérelve.")
                
        uj_berles = Berles(auto, datum)
        self._berlesek.append(uj_berles)
        return auto.berleti_dij
        
    def berles_lemondasa(self, rendszam: str, datum: datetime.date):
        for b in self._berlesek:
            if b.auto.rendszam == rendszam and b.datum == datum:
                self._berlesek.remove(b)
                return True
        raise ValueError("Nem található ilyen bérlés a megadott adatokkal. Nem lehetséges a lemondás.")
        
    def berlesek_listazasa(self):
        if not self._berlesek:
            print("Jelenleg nincs aktív bérlés rendszerben.")
            return
            
        # Rendezzük dátum szerint a szebb megjelenítésért
        rendezett_berlesek = sorted(self._berlesek, key=lambda b: b.datum)
        for b in rendezett_berlesek:
            print(f"Dátum: {b.datum} | Autó: {b.auto.tipus} ({b.auto.rendszam}) | Ár: {b.auto.berleti_dij} Ft/nap")


def main():
    kolcsonzo = Autokolcsonzo("Kiváló Autókölcsönző")
    
    # 3 autó előkészítése
    a1 = Szemelyauto("AAA-111", "Toyota Corolla", 15000, 5)
    a2 = Szemelyauto("BBB-222", "Suzuki Swift", 10000, 5)
    a3 = Teherauto("CCC-333", "Ford Transit", 25000, 1500)
    
    kolcsonzo.auto_hozzaadasa(a1)
    kolcsonzo.auto_hozzaadasa(a2)
    kolcsonzo.auto_hozzaadasa(a3)
    
    # 4 bérlés előkészítése
    ma = datetime.today().date()
    holnap = ma + timedelta(days=1)
    holnaputan = ma + timedelta(days=2)
    
    try:
        kolcsonzo.berles("AAA-111", holnap)
        kolcsonzo.berles("AAA-111", holnaputan)
        kolcsonzo.berles("BBB-222", holnap)
        kolcsonzo.berles("CCC-333", holnaputan)
    except Exception as e:
        print("Hiba az előkészítés során:", e)

    # CLI interfész
    while True:
        print(f"\n--- {kolcsonzo.nev} Rendszer ---")
        print("1. Autó bérlése")
        print("2. Bérlés lemondása")
        print("3. Bérlések listázása")
        print("0. Kilépés")
        
        valasztas = input("Válasszon egy opciót: ")
        
        if valasztas == "1":
            print("\nElérhető autók:")
            for a in kolcsonzo.autok:
                print(f"- {a.tipus} ({a.rendszam}) - {a.berleti_dij} Ft/nap")
                
            rendszam = input("\nKérem a bérelni kívánt autó rendszámát: ")
            datum_str = input("Kérem a dátumot (ÉÉÉÉ-HH-NN formátumban): ")
            try:
                datum = datetime.strptime(datum_str, "%Y-%m-%d").date()
                ar = kolcsonzo.berles(rendszam, datum)
                print(f"\nSikeres bérlés! A bérleti díj: {ar} Ft.")
            except ValueError as e:
                print(f"\nHiba: {e}")
                
        elif valasztas == "2":
            rendszam = input("\nKérem a lemondandó autó rendszámát: ")
            datum_str = input("Kérem a lemondandó bérlés dátumát (ÉÉÉÉ-HH-NN formátumban): ")
            try:
                datum = datetime.strptime(datum_str, "%Y-%m-%d").date()
                kolcsonzo.berles_lemondasa(rendszam, datum)
                print("\nA bérlés sikeresen lemondva.")
            except ValueError as e:
                print(f"\nHiba: {e}")
                
        elif valasztas == "3":
            print("\nAktuális bérlések:")
            kolcsonzo.berlesek_listazasa()
            
        elif valasztas == "0":
            print("Kilépés a rendszerből...")
            break
            
        else:
            print("\nÉrvénytelen választás. Kérem próbálja újra.")

if __name__ == "__main__":
    main()
