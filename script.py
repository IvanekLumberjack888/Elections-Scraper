# import sys, requests
# from bs4 import BeautifulSoup

"""
    Election Scraper
    Autor: Ivo Doležal 
"""


def main():
    if len(sys.argv) < 3:
        print("Chybí argumenty!")
        quit()

    url = sys.argv[1]
    out = sys.argv[2]

    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    links = [a["href"] for a in soup.find_all("td")]

    print (links)

    if __name__ == "__main__":
        main