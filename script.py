"""
    main.py: třetí projekt do Engeto Online Python Akademie

    author: Ivo Doležal
    email: ivousd@seznam.cz/ivousd@gmail.com
"""

from __future__ import annotations
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import csv
import sys
from typing import List, Dict
import time

"""
    main.py: třetí projekt do Engeto Online Python Akademie

    author: Ivo Doležal
    email: ivousd@seznam.cz/ivousd@gmail.com
"""

HEADERS = {"User-Agent": "Verze 138.0.7204.184 (Oficiální sestavení) (64bitový)"} # Základní maskování prohlížeče
# Pokud bys chtěl použít jiný User-Agent, můžeš si ho najít

SLEEP = 0.8 # PAUZA mezi jednotlivými voláními get # Aby server nezkolaboval # Je to v sekudnách

# Používáný odkaz
url = "https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"

district_url = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6203"

# **Základní kostra:**
def fetch_data(url: str) -> str:
    """Funkce pro získání HTML obsahu z dané URL."""
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.text

# odeslání požadavku GET


def soup(url: str) -> BeautifulSoup:
    """Funkce pro vytvoření BeautifulSoup objektu z HTML obsahu."""
    html_content = fetch_data(url)
    return BeautifulSoup(html_content, features="html.parser"
                         
                         )
    
# parsování vráceného HTML dle Okresu
def parse_district(soup: BeautifulSoup) -> List[str]:
    """
    Vrací absolutní odkazy z jednotlivých okresů.
    """
    return [urljoin(district_url, a_tag['href'])
            for a_tag in soup.select("td.cislo a[href]")]

# parsování vráceného HTML dle Obcí
def parse_obce(soup: BeautifulSoup) -> List[str]:
    """
    Vrací absolutní odkazy z jednotlivých obcí.
    """
    return [urljoin(district_url, a_tag['href'])
            for a_tag in soup.select("td.cislo a[href]")]

    # Statická metoda pro získání všech A tagů
def get_all_a_tags(soup: BeautifulSoup) -> List[BeautifulSoup]:
    """Vrací všechny A tagy v daném BeautifulSoup objektu."""
    return soup.find_all("a")  

# Hlasy stran
# Funkce pro získání hlasů stran z dané stránky obce
def ziskej_hlasy_stran(soup: BeautifulSoup) -> Dict[str, str]:
    """
    Vrací slovník s názvy stran a počtem hlasů z dané stránky.
    """ 
    vysledky = {}
    tabulka = soup.find("table", {"class": "table"})  # Najdi tabulku s výsledky
    if not tabulka:
        return vysledky
    for radek in tabulka.find_all("tr"):
        bunky = radek.find_all("td")
        if len(bunky) >= 3:
            nazev_strany = bunky[1].get_text(strip=True)
            hlasy = bunky[2].get_text(strip=True).replace('\xa0', '')
            vysledky[nazev_strany] = hlasy
    return vysledky

# **CSV**

def save_to_csv(data: List[Dict[str, str]], filename: str) -> None:
    """Uloží data do CSV souboru."""
    with open(filename, mode="w", newline="", encoding="utf-8") as csv_file:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        writer.flush()
        os.fsync(csv_file.fileno())
        csv_file.close()

# **Hlavní část programu**
def main(argv: List[str] = None) -> None:
    """Hlavní funkce programu."""
    if argv is None:
        argv = sys.argv[1:]  # Pokud není předán žádný argument, použije se sys.argv

    if not argv:
        print("Nebyl zadán žádný soubor pro uložení dat.")
        return

    filename = argv[0]
    
    # Získání HTML obsahu
    soup_obj = soup(url)
    
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
