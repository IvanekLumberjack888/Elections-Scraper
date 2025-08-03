from __future__ import annotations
import requests  # pro requests.get stahování
from bs4 import BeautifulSoup  # parsovní stránek
from urllib.parse import urljoin  # spojování adres URL

import csv  # pro CSV
import sys  # z přikázové řádky
from typing import List, Dict, Tuple  # pro typování
import time  # pro časové pauzy mezi requesty

# import os                                   # pro např. clearování

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
    VOLBY.CZ v příkazové řádce:
        -> Obecné použití:
        python main.py <URL_okresu> <vystupni_soubor.csv>
        -> 👉 Můj příklad – Volby 2017 konkrétní výběr z okresu a obcí 👈
        python main.py 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6203' 'vystup.csv'
"""

# kONSTANTY
HEADERS = (
    "User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
)
# --- IGNORE --- Základní maskování prohlížeče #NEJSME_ROBOTI 🤖🤖🤖
# --- IGNORE --- NA WEBU VOLBY.CZ/ROBOTS.TXT je pouze:
# --- IGNORE --- User-agent: * a taky "Disallow: /pls/" -> takže pohoda 😉
SLEEP = 0.8  # PAUZA mezi jednotlivými voláními get. Aby server nezkolaboval. Je to v sekundách
# --- IGNORE --- Pro jistotu

# Odkaz na hlavní stránku s výsledky voleb do Poslanecké sněmovny ČR 2017
url = "https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"

# Můj vybraný okres
district_name = "Brno-venkov"

# Odkaz na okres
district_url = (
    "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6203"
)

# Výpis základních informací o programu
print(
    f""" ...🔪+🥔 = 🍟\nSkrejpujeme volební data z vybraného okresu, který je na stránce:
    {url}
    A to konkrétně z okresu {district_name}
    Adresa je:
    {district_url}"""
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
            return nazev.replace("–", "").strip(), kod.strip()
        else:
            return text, ""
    else:
        return "", ""


# Obce z okresu
def get_municipality_links(district_url: str) -> List[str]:
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


def get_municipality_name(soup: BeautifulSoup) -> str:
    """
    Vrací název obce
    """
    nazev, _ = parse_h3_title(soup)
    return nazev


def get_municipality_stats(soup: BeautifulSoup) -> Dict[str, str | int]:
    """
    Vrací statistiky obce (voliči v seznamu, vydané obálky, platné hlasy)
    """
    stats = soup.select("td:has(span.number)")

    vysledek = {"voliči v seznamu": 0, "vydané obálky": 0, "platné hlasy": 0}

    if len(stats) >= 3:
        try:
            vysledek["voliči v seznamu"] = int(stats[0].get_text().replace("\xa0", ""))
            vysledek["vydané obálky"] = int(stats[1].get_text().replace("\xa0", ""))
            vysledek["platné hlasy"] = int(stats[2].get_text().replace("\xa0", ""))
        except ValueError:
            # Pokud dojde k chybě, budou nuly
            pass

    return vysledek


def get_municipality_parties(soup: BeautifulSoup) -> Dict[str, str | int]:
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


def parse_municipality_data(municipality_url: str) -> Dict[str, str | int]:
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


def save_to_csv(data: List[Dict[str, int | str]], filename: str) -> None:
    """Uloží data do CSV souboru."""
    if not data:
        print("Žádná data k uložení.")
        return

    zahlavi = [
        "kód obce",
        "název obce",
        "voliči v seznamu",
        "vydané obálky",
        "platné hlasy",
    ]

    parties = set()
    for obec in data:
        for nazev_sloupce in obec.keys():
            if nazev_sloupce not in zahlavi:
                parties.add(nazev_sloupce)
    parties = sorted(parties)
    fieldnames = zahlavi + parties

    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect="excel-tab")
            writer.writeheader()
            writer.writerows(data)

    except IOError as e:
        print(f"Chyba při ukládání do CSV souboru {filename}: {e}")
        sys.exit(1)

    print(
        f"CSV uloženo: {filename} ({len(data)} záznamů, {len(data)} obce/obcí, {len(parties)} strany/stran)"
    )


# =====================================================
# ====================== MAIN =========================
# =====================================================


def main(argv: List[str] = None) -> None:
    """Hlavní funkce programu."""
    print("Election Scraper - Volby.cz 2017")
    print("=================================")

    district_url, outputfile = validate_args()

    print(f"Okres: {district_url}")
    print(f"Výstup: {outputfile}\n")

    municipality_links = get_municipality_links(district_url)
    if not municipality_links:
        print("Žádné obce - nenalezeno.")
        sys.exit(1)

    all_municipality_data = []
    for i, link in enumerate(municipality_links, 1):
        print(f"[{i} z {len(municipality_links)}] Zpracovávám..")
        municipality_data = parse_municipality_data(link)
        all_municipality_data.append(municipality_data)

        print(f"Zpracováno: {municipality_data['název obce']}, ukládám do csv.")
        time.sleep(SLEEP)

    print("Hotovo.")
    save_to_csv(all_municipality_data, outputfile)


if __name__ == "__main__":
    main()
