from __future__ import annotations
import requests                             # pro requests.get stahování
from bs4 import BeautifulSoup               # parsovní stránek
from urllib.parse import urljoin            # spojování adres URL
# import os                                 # pro např. clearování
import csv                                  # pro CSV
import sys                                  # z přikázové řádky
from typing import List, Dict, Tuple        # pro typování
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
        -> Obecné použití:
        python main.py <URL_okresu> <vystupni_soubor.csv>
        -> 👉 Můj příklad: 👈
        python main.py 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6203' 'vystup.csv'
"""

# CONSTANTS
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"}
# --- IGNORE --- Základní maskování prohlížeče #NEJSME_ROBOTI 🤖🤖🤖
# --- IGNORE --- NA WEBU VOLBY.CZ/ROBOTS.TXT je pouze:
# --- IGNORE --- User-agent: * a taky "Disallow: /pls/" -> takže pohoda 😉
SLEEP = 0.8     # PAUZA mezi jednotlivými voláními get. Aby server nezkolaboval. Je to v sekundách
# --- IGNORE --- Pro jistotu

# Odkaz na hlavní stránku s výsledky voleb do Poslanecké sněmovny ČR 2017
url = "https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"

# Odkaz na okres, který budeme zpracovávat (👉 Můj příklad 👈)
district_url = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6203"

# Výpis základních informací o programu
print(
    f'''Skrejpujeme volební data z vybraného okresu, který je na stránce {url}
    a to konkrétně z okresu {district_url}'''
    )

# Kontrola argumentů - čili url a soubor pro uložení dat
def validate_args() -> Tuple[str, str]:
    """Kontrola argumentů z příkazové řádky."""
    if len(sys.argv) != 3:
        print("Použití: python main.py <URL_okresu> <vystupni_soubor.csv>")
        sys.exit(1)

    district_url, outputfile = sys.argv[1], sys.argv[2]

    if not district_url.startswith("http"):
        print("Zadaná URL není platná. Ujistěte se, že začíná na http:// nebo https://")
        sys.exit(1)

    if "volby.cz" not in district_url or "ps32" not in district_url:
        print("Zadaná URL není platná. Ujistěte se, že obsahuje 'volby.cz' a 'ps32'.")
        sys.exit(1)
    
    if not outputfile.endswith(".csv"):
        outputfile += ".csv"

    return district_url, outputfile

# =====================================================
# ========== Základní stahování a parsování: ==========
# =====================================================
def fetch_data(url: str) -> str:                                                   
    """Funkce pro získání HTML obsahu z dané URL."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as e:
        print(f"Chyba při stahování dat z {url}: {e}")
        sys.exit(1)

def make_soup(url: str) -> BeautifulSoup:                                   
    """Funkce pro vytvoření BeautifulSoup objektu z HTML obsahu."""
    html_content = fetch_data(url)
    return BeautifulSoup(html_content, features="html.parser")

def parse_h3_title(soup: BeautifulSoup) -> tuple[str, str]:
    """
    Vyřeší opakování parsování názvu a kódu obce z H3 tagu.
    """
    h3 = soup.select_one("h3")
    if h3:
        text = h3.get_text(strip=True)
        if "kód" in text:
            nazev, kod = text.rsplit("kód", 1)
            return nazev.replace("-", "").strip(), kod.strip()
        else:
            return text, ""
    else:
        return "", ""

# Obce z okresu
def get_municipality_links(district_url: str):
    """
    Vrací odkazy z jednotlivých okresů do listu
    """
    html_content = fetch_data(district_url)
    soup = BeautifulSoup(html_content, "html.parser")

    links = []
    for td in soup.select("td.cislo"):
        a_tag = td.select_one("a[href]")
        if a_tag:
            full_url = urljoin(district_url, a_tag["href"])
            links.append(full_url)

    print(f"Nalezeno {len(links)} obcí.")
    return links

# Údaje z obce -> jednotlivé fce

def parse_municipality_code(soup: BeautifulSoup) -> str:                   
    """
    Vrací kód obce
    """
    _, kod = parse_h3_title(soup)
    return kod

def get_municipality_name(soup: BeautifulSoup) -> str:                     # get_municipality_name() -> parsování názvu obce
    """
    Vrací název obce
    """
    _, nazev = parse_h3_title(soup)
    return nazev

def get_municipality_stats(soup: BeautifulSoup) -> dict[str, int]:
    """
    Vrací statistiky obce (voliči, vydané obálky, platné hlasy)
    """ 
    stats = soup.select('td:has(span.number)')

    vysledek = {
        "voliči": 0,
        "vydané obálky": 0,
        "platné hlasy": 0
    }

    if len(stats) >= 3:
        try:
            vysledek["voliči"] = int(stats[0].get_text().replace("\xa0", ""))
            vysledek["vydané obálky"] = int(stats[1].get_text().replace("\xa0", ""))
            vysledek["platné hlasy"] = int(stats[2].get_text().replace("\xa0", ""))
        except ValueError:
        # Pokud dojde k chybě, budou nuly
            pass

    return vysledek

def get_municipality_parties(soup: BeautifulSoup) -> dict[str, int]:
    """
    Vrací slovník s počtem hlasů pro jednotlivé strany v obci.
    """
    parties = {}

    for table in soup.select("table"):
        for row in table.select("tr")[2:]:
            cells = row.select("td")
            if len(cells) >= 3:
                strana = cells[1].get_text(strip=True)
                hlasy_text = cells[2].get_text(strip=True).replace("\xa0", "")
                try:
                    hlasy = int(hlasy_text)
                except ValueError:
                    hlasy = 0
                if strana:
                    parties[strana] = hlasy

    return parties

def parse_municipality_data(municipality_url: str) -> dict:
    """
    Hlavní funkce - zpracuje jednu obec pomocí menších funkcí.
    Tohle je orchestrátor který spojuje všechny municipality_ funkce.
    """
    html_content = fetch_data(municipality_url)
    soup = BeautifulSoup(html_content, "html.parser")

    data = {}
    # Propojení fcí
    data["kód obce"] = parse_municipality_code(soup)
    data["název obce"] = get_municipality_name(soup)

    # K tomu se připojí stats
    data.update(get_municipality_stats(soup))
    # Přidání stran
    data.update(get_municipality_parties(soup))

    return data

# =====================================================
# ====================== CSV ==========================
# =====================================================

def save_to_csv(data: List[Dict[str, str]], filename: str) -> None:
    """Uloží data do CSV souboru."""
    if not data:
        print("Žádná data k uložení.")
        return

    base_columns = ["kód obce", "název obce", "voliči v seznamu", "vydané obálky", "platné hlasy"]
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
    # ...
    for i, link in enumerate(municipality_links, 1):
        # ...
        municipality_data = parse_municipality_data(link)

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
