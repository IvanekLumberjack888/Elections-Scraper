from __future__ import annotations
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import random
import csv
import sys
from typing import List, Dict, Tuple
import time
import pandas as pd


"""
    main.py: třetí projekt do Engeto Online Python Akademie

    author: Ivo Doležal
    email: ivousd@seznam.cz/ivousd@gmail.com

    Program scrape výsledky voleb z okresu na volby.cz a uloží do CSV i Excelu.

 
   WW      WW EEEEEEE BBBBB      SSSSS   CCCCC  RRRRRR    AAA   PPPPPP  EEEEEEE RRRRRR  
   WW      WW EE      BB   B    SS      CC    C RR   RR  AAAAA  PP   PP EE      RR   RR 
   WW   W  WW EEEEE   BBBBBB     SSSSS  CC      RRRRRR  AA   AA PPPPPP  EEEEE   RRRRRR  
    WW WWW WW EE      BB   BB        SS CC    C RR  RR  AAAAAAA PP      EE      RR  RR  
     WW   WW  EEEEEEE BBBBBB     SSSSS   CCCCC  RR   RR AA   AA PP      EEEEEEE RR   RR    
    
    """

# Konstanty
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
SLEEP = 2.0  # pauza mezi požadavky (sekundy)

# Můj příklad
muj_priklad = """python main.py 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6203' vystup.csv"""

print(f""" 👋🏽 Pro svůj příklad jsem si vzal okres Brno-venkov
      Stačí zadat: <{muj_priklad}>
      """
    )   


def validate_args() -> Tuple[str, str]:
    """Kontrola argumentů z příkazové řádky."""
    if len(sys.argv) != 3:
        print("Usage: python main.py <district_url> <output.csv>")
        sys.exit(1)
    district_url, outputfile = sys.argv[1], sys.argv[2]
    if not district_url.startswith(("http://", "https://")) or "ps32" not in district_url:
        print("Invalid URL: must contain 'ps32'.")
        sys.exit(1)
    if not outputfile.lower().endswith(".csv"):
        outputfile += ".csv"
    return district_url, outputfile

def fetch_data(url: str, retries: int = 3) -> str:
    """Stáhne HTML obsah z URL s retry mechanismem."""
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            if attempt == retries:
                print(f"Failed to fetch {url}: {e}")
                sys.exit(1)
            wait = random.uniform(1, 3)
            time.sleep(wait)
    return ""

def make_soup(url: str) -> BeautifulSoup:
    """Vytvoří BeautifulSoup objekt."""
    return BeautifulSoup(fetch_data(url), "html.parser")

def parse_h3_title(soup: BeautifulSoup) -> tuple[str, str]:
    """Parsuje H3 tag pro název a kód obce."""
    # Hledáme H3 s textem "Obec: XYZ"
    for h3 in soup.select("h3"):
        text = h3.get_text(strip=True)
        if text.startswith("Obec:"):
            municipality_name = text.replace("Obec:", "").strip()
            return municipality_name, ""
    return "", ""

def get_municipality_links(district_url: str) -> List[str]:
    """Vrací seznam odkazů na PS311 (obce) z okresní stránky."""
    soup = make_soup(district_url)
    links: List[str] = []
    
    # Hledáme všechny odkazy v tabulce obcí
    for row in soup.select("tr"):
        # Najdeme buňku s číslem obce a odkazem
        number_cell = row.select_one("td.cislo")
        if not number_cell:
            continue
            
        # V té samé buňce nebo vedlejší hledáme odkaz
        link = row.select_one("a[href*='ps311']")
        if not link:
            continue
            
        href = link["href"]
        if "ps311" in href and "ps32" not in href:
            full_url = urljoin(district_url, href)
            links.append(full_url)
    
    print(f"Found {len(links)} municipalities.")
    return links

def parse_municipality_stats(soup: BeautifulSoup) -> Dict[str, int]:
    """Parsuje základní statistiky obce."""
    stats = {"registered": 0, "envelopes": 0, "valid": 0}
    
    # Hledáme čísla v tabulce se statistikami
    for td in soup.select("td.cislo"):
        text = td.get_text(strip=True).replace("\xa0", "").replace(" ", "")
        if text.isdigit():
            num = int(text)
            # První velké číslo je obvykle počet voličů
            if num > 50 and stats["registered"] == 0:
                stats["registered"] = num
            elif num > 30 and stats["envelopes"] == 0 and num < stats["registered"]:
                stats["envelopes"] = num
            elif num > 30 and stats["valid"] == 0 and num <= stats["envelopes"]:
                stats["valid"] = num
                break
    
    return stats

def parse_municipality_parties(soup: BeautifulSoup) -> Dict[str, int]:
    """Parsuje hlasy pro jednotlivé strany."""
    parties: Dict[str, int] = {}
    
    # Hledáme tabulky s výsledky stran
    for table in soup.select("table.table"):
        for row in table.select("tr"):
            cells = row.select("td")
            if len(cells) < 4:
                continue
                
            # Druhá buňka obsahuje název strany
            party_cell = cells[1]
            if not party_cell:
                continue
                
            party_name = party_cell.get_text(strip=True)
            if not party_name or len(party_name) < 3:
                continue
                
            # Třetí buňka obsahuje počet hlasů
            votes_cell = cells[2]
            votes_text = votes_cell.get_text(strip=True).replace("\xa0", "")
            
            try:
                votes = int(votes_text)
                parties[party_name] = votes
            except ValueError:
                continue
    
    return parties

def parse_municipality_data(url: str) -> Dict[str, str | int]:
    """Parsuje data jedné obce."""
    soup = make_soup(url)
    name, code = parse_h3_title(soup)
    
    # Pokud název není nalezen, zkusíme jiný způsob
    if not name:
        breadcrumb = soup.select_one("p.drobek")
        if breadcrumb:
            text = breadcrumb.get_text()
            if "Obec" in text:
                parts = text.split("Obec")
                if len(parts) > 1:
                    name = parts[-1].strip()
    
    data: Dict[str, str | int] = {
        "code": code,
        "location": name
    }
    
    data.update(parse_municipality_stats(soup))
    data.update(parse_municipality_parties(soup))
    
    return data

def save_to_csv(rows: List[Dict[str, str | int]], filename: str) -> None:
    """Uložení do CSV se středníky."""
    if not rows:
        print("No data to save.")
        return
        
    header = ["code", "location", "registered", "envelopes", "valid"]
    extras = sorted({k for row in rows for k in row.keys() if k not in header})
    fieldnames = header + extras
    
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"CSV saved: {filename} ({len(rows)} municipalities)")

def main() -> None:
    """Hlavní program."""
    print("Election Scraper - Volby.cz")
    print("=" * 30)
    
    district_url, outputfile = validate_args()
    print(f"District: {district_url}")
    print(f"Output: {outputfile}")
    
    links = get_municipality_links(district_url)
    if not links:
        print("No municipalities found!")
        sys.exit(1)
    
    all_data: List[Dict[str, str | int]] = []
    
    for i, link in enumerate(links, start=1):
        print(f"[{i}/{len(links)}] Processing...")
        data = parse_municipality_data(link)
        all_data.append(data)
        print(f"  -> {data['location']}")
        time.sleep(SLEEP)
    
    save_to_csv(all_data, outputfile)
    print("Done!")

if __name__ == "__main__":
    main()
