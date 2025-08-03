# Election Scraper – Volby 2017

**Třetí projekt Engeto Online Python Akademie**

## Itinerář

1. Příprava prostředí  
   a) Otevřít terminál a přejít do složky projektu  
   b) Vytvořit virtuální prostředí  
   c) Aktivovat virtuální prostředí  
   d) Aktualizovat pip  
   e) Nainstalovat závislosti z `requirements.txt`  

2. Spuštění skriptu  
   a) V řádku zadat:  
   ```
   python main.py "" ""
   ```
   b) Počkejte na výpis:  
   ```
   STAHUJI DATA Z VYBRANÉHO URL: 
   UKLÁDÁM DO SOUBORU: 
   HOTOVO!
   ```

3. Kontrola výstupu  
   Otevřít CSV v Excelu nebo v textovém editoru a ověřit sloupce:  
   ```
   kód obce, název obce, voliči v seznamu, vydané obálky, platné hlasy, [název strany]...
   ```

## 1. Příprava prostředí

```bash
uděláte si prázdnou složku a v terminálu zadáte přikaz:
python -m venv .venv
# PowerShell:
.venv\Scripts\Activate.ps1
# nebo CMD:
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Spuštění skriptu

```bash
python main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6203" "vysledky_brno_venkov.csv"
```

- **Argument 1:** URL okresu (obsahuje `ps32`)  
- **Argument 2:** Název výstupního CSV souboru  

### Příklad výstupu

```
STAHUJI DATA Z VYBRANÉHO URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6203
UKLÁDÁM DO SOUBORU: vysledky_brno_venkov.csv
HOTOVO!
```

## 3. Kontrola CSV

Otevřít `vysledky_brno_venkov.csv` a ověřit, že obsahuje:

```
kód obce,název obce,voliči v seznamu,vydané obálky,platné hlasy,ANO 2011,ODS,Piráti,SPD,...
582282,Bedřichovice,148,120,118,25,15,8,12,...
589268,Bedihošť,834,527,524,91,150,89,65,45,...
...
```

## Verze Python

Testováno na Python 3.13.3 (Windows)

## Kontakt

**Ivo Doležal**  
Email: ivousd@gmail.com  
GitHub: @IvanekLumberjack888
