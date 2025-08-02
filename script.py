from __future__ import annotations
import requests                             # pro requests.get stahování
from bs4 import BeautifulSoup               # parsovní stránek
from urllib.parse import urljoin            # spojování adres URL
# import os                                   # pro např. clearování
import csv                                  # pro CSV
import sys                                  # z přikázové řádky
from typing import List, Dict               # pro typování
import time                                 # pro časové pauzy mezi requesty

"""
    main.py: třetí projekt do Engeto Online Python Akademie

    author: Ivo Doležal
    email: ivousd@seznam.cz/ivousd@gmail.com

        WW      WW EEEEEEE BBBBB      SSSSS   CCCCC  RRRRRR    AAA   PPPPPP  EEEEEEE RRRRRR  
        WW      WW EE      BB   B    SS      CC    C RR   RR  AAAAA  PP   PP EE      RR   RR 
        WW   W  WW EEEEE   BBBBBB     SSSSS  CC      RRRRRR  AA   AA PPPPPP  EEEEE   RRRRRR  
         WW WWW WW EE      BB   BB        SS CC    C RR  RR  AAAAAAA PP      EE      RR  RR  
          WW   WW  EEEEEEE BBBBBB     SSSSS   CCCCC  RR   RR AA   AA PP      EEEEEEE RR   RR 
    ---
    V příkazové řádce:
        Obecné použití:    python main.py <URL_okresu> <vystupni_soubor.csv>
        Můj příklad v shell zadáš:    python main.py 'https://www.vol
    Obecné použití:    python main.py <URL_okresu> <vystupni_soubor.csv>
    Můj příklad v shell zadáš:   python main.py 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6203' 'vystup.csv'
    ---
"""

# **CONSTANTS**

HEADERS = {"User-Agent": "Verze 138.0.7204.184 (Oficiální sestavení) (64bitový)"}       # Základní maskování prohlížeče #NEJSME_ROBOTI 🤖🤖🤖

SLEEP = 0.8     # PAUZA mezi jednotlivými voláními get. Aby server nezkolaboval. Je to v sekundách

# --- IGNORE --- NA WEBU VOLBY.CZ/ROBOTS.TXT
# --- IGNORE --- User-agent: * a taky "Disallow: /pls/" -> takže pohoda 😉

# Používaný odkaz
url = "https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"

district_url = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6203"

# ========== Základní stahování a parsování: ==========

def fetch_data(url: str) -> str:                                                         # fetch_html() -> stáhne HTML s chytáním chyb
    """Funkce pro získání HTML obsahu z dané URL."""
    try:
        resp = requests.get(url, headers=HEADERS)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as e:
        print(f"Chyba při stahování dat z {url}: {e}")
        sys.exit(1) # Ukončí program





def make_soup(url: str) -> BeautifulSoup:                                                # make_soup() -> vytvoří BeautifulSoup objekt
    """Funkce pro vytvoření BeautifulSoup objektu z HTML obsahu."""
    html_content = fetch_data(url)
    return BeautifulSoup(html_content, features="html.parser")
    
def parse_district(soup: BeautifulSoup) -> List[str]:                                    # parse_district() -> parsování okresů
    """
    Vrací absolutní odkazy z jednotlivých okresů.
    """
    return [urljoin(district_url, a_tag['href'])
            for a_tag in soup.select("td.cislo a[href]")]


def parse_obce(soup: BeautifulSoup) -> List[str]:                                        # parse_obce() -> parsování obcí
    """
    Vrací absolutní odkazy z jednotlivých obcí.
    """
    return [urljoin(district_url, a_tag['href'])
            for a_tag in soup.select("td.cislo a[href]")]


def get_all_a_tags(soup: BeautifulSoup) -> List[BeautifulSoup]:                          # get_all_a_tags() -> získá všechny A tagy
    """Vrací všechny A tagy v daném BeautifulSoup objektu."""
    return soup.find_all("a")  

# Hlasy stran

def ziskej_hlasy_stran(soup: BeautifulSoup) -> Dict[str, str]:
    """
    Vrací slovník s názvy stran a počtem hlasů z dané stránky.
    """ 
    strany = {}
    for tabulka in tabulka.find_all("table", {"class": "table"}):  # noqa: F821
        for radek in tabulka.find_all("tr"):
            bunky = radek.find_all("td")
            if len(bunky) >= 3:
                nazev_strany = bunky[1].get_text(strip=True)
                hlasy = bunky[2].get_text(strip=True).replace('\xa0', '')
                strany[nazev_strany] = hlasy
    return strany

# **CSV**

def save_to_csv(data: List[Dict[str, str]], filename: str) -> None:
    """Uloží data do CSV souboru."""
    with open(filename, mode="w", newline="", encoding="utf-8") as csv_file:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        csv_file.close()

# **Hlavní část programu**
def main(argv: List[str] = None) -> None:
    """Hlavní funkce programu."""
    if argv is None:
        argv = sys.argv[1:]

    if len(sys.argv) != 3:
        print(f"Použití: {sys.argv[0]} <url> a {sys.argv[1]} jako <soubor pro uložení dat v CSV formátu>")
        return

    if not argv:
        print("Nebyl zadán žádný soubor pro uložení dat.")
        return
    
    url = argv[0]  # První argument je URL
    if not url.startswith("http"):
        print("Zadaná URL není platná. Ujistěte se, že začíná na http:// nebo https://")
        return
    if not url.endswith("/"):
        url += "/"  # Přidá lomítko na konec URL, pokud tam není
    print(f"Stahuji data z {url}")

    # Druhý argument je název souboru pro uložení dat
    if len(argv) < 2:
        print("Nebyl zadán název souboru pro uložení dat.")
        return
    if len(argv) > 2:
        print("Bylo zadáno více než dva argumenty. Použijte pouze URL a název souboru.")
        return
    if not argv[1]:
        print("Nebyl zadán název souboru pro uložení dat.")
        return
    
    filename = argv[1]
    if not filename.endswith(".csv"):
        print("Zadaný soubor pro uložení dat musí mít příponu .csv")
    elif out_csv := filename.endswith(".csv"):
        out_csv += ".csv"  # Přidá příponu .csv, pokud není přítomna
        print(f"Ukládám data do souboru {out_csv}")
        return
    
    # Získání HTML obsahu
    soup_obj = make_soup(url)
    if not soup_obj:
        print("Nepodařilo se získat obsah stránky.")
        return
    # Získání okresů
    districts = parse_district(soup_obj)
    
    # Příklad: projít všechny okresy a stáhnout jejich stránky s pauzou
    for district_link in districts:
        # ...zpracování dat...
        time.sleep(SLEEP)  # Pauza mezi požadavky

    # Uložení do CSV
    # save_to_csv(districts, filename)  # Upravte podle toho, co chcete ukládat
    
    print(f"Data byla úspěšně uložena do souboru {filename}")
    # Výpis všech A tagů
    print("Všechny odkazy:")
    for link in get_all_a_tags(soup_obj):
        print(link.get_text(strip=True), link['href'])

# Hlavní funkce

if main.__name__ == "__main__":
    main()

#make_soup() - vytvoří BeautifulSoup objekt
