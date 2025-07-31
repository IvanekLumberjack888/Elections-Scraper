"""
    main.py: třetí projekt do Engeto Online Python Akademie

    author: Ivo Doležal
    email: ivousd@seznam.cz/ivousd@gmail.com
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import csv
import sys
import time
from __future__ import annotations
from pathlib import Path
from typyng imprort List Dict

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

parties = {}
for table in page.select("table"):
    for row in table.select("tr"):
        name = row.select_one(td:nth-child(2)).text.strip()
        votes = row.select_one("td:nth-child(3)").text.replace("\xa0", "")
        parties[name] = int(votes)


    code = page.select_one("h3").text.split()[-1]
    name = " ".join(code)
    return {"kód": code, "obec": name, "voliči": voters, "obálky": envelopes, "platné": valid, **parties}


