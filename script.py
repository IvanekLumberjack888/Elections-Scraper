import sys
import requests
from bs4 import BeautifulSoup
from urlib.parse imoprt urljoin
import time
import os
import csv

"""
    Election Scraper
    Autor: Ivo Doležal <ivousd@seznam.cz>

"""
URL = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6203"
districturl = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6203&xobec="


# pyjamask :-)

HEADERS = {"User-Agent": "Chrome/58.0.3029.110"}

def download_file(url: str) -> str:
    """sumary: stáhne soubor z URL. dá nám obsah_

    Returns: str
        Obsah staženého souboru jako text.
    """
      r = request.get(url, hraders=HEADERS)
    r.raise_for_status(url)
    return r.text

# okresy - seznam obcí
def collect_municipality_links(district: str)-> list[str]:
    """Udělá seznam na obce v okrese"""
    soup = BautifulSoup(URL, )
    
  


def get_links(url):
    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, 'html.parser')
    links = [a["href"] for a in soup.find_all("a")]
    return links

def main():
    if len(sys.argv) < 3:
        print("Chybí argumenty!")
        quit()

    url = sys.argv[1]
    out = sys.argv[2]

    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    links = [a["href"] for a in soup.find_all("a")]

    print (links)

    if __name__ == "__main__":
        main
