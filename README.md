---ENG---

# Election Scraper – Chamber of Deputies 2017

**Third Project for Engeto Online Python Academy**

## Itinerary

1. Environment Setup  
   a) Open your terminal and navigate to the project folder  
   b) Create a virtual environment  
   c) Activate the virtual environment  
   d) Upgrade pip  
   e) Install dependencies from `requirements.txt`  

2. Running the Script  
   a) In the terminal type:  
   ```
   python main.py "" ""
   ```
   b) Wait for console output:  
   ```
   Fetching data from: 
   Saving to: 
   Done!
   ```

3. Verify Output  
   Open the generated CSV in Excel or a text editor and check that the header and first rows look like this:

   ```
   code;location;registered;envelopes;valid;ANO 2011;Blok proti islam.-Obran.domova;CESTA ODPOVĚDNÉ SPOLEČNOSTI;Dobrá volba 2016;Dělnic.str.sociální spravedl.;Komunistická str.Čech a Moravy;Křesť.demokr.unie-Čs.str.lid.;Národ Sobě;Občanská demokratická aliance;Občanská demokratická strana;REALISTÉ;ROZUMNÍ-stop migraci,diktát.EU;Radostné Česko;Referendum o Evropské unii;SPORTOVCI;SPR-Republ.str.Čsl. M.Sládka;STAROSTOVÉ A NEZÁVISLÍ;Strana Práv Občanů;Strana svobodných občanů;Strana zelených;Svob.a př.dem.-T.Okamura (SPD);TOP 09;Česká pirátská strana;Česká str.sociálně demokrat.;Česká strana národně sociální;Řád národa - Vlastenecká unie
   ;Babice nad Svitavou;925;660;660;129;0;2;0;1;31;69;0;0;109;2;3;0;0;1;3;53;1;10;7;58;39;93;43;0;1
   ;Babice u Rosic;553;353;353;93;0;0;0;1;30;25;0;2;32;4;1;1;0;1;1;27;0;6;5;49;13;37;18;5;0
   ;Běleč;160;131;131;30;0;0;0;0;14;14;0;0;13;0;1;0;1;0;0;8;0;0;0;12;1;11;25;0;0
   ```

## 1. Environment Setup

```bash
cd path/to/project
python -m venv .venv

# PowerShell
.venv\Scripts\Activate.ps1

# CMD
.venv\Scripts\activate.bat

python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Running the Script

```bash
python main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6203" "results_brno_venkov.csv"
```

- **Argument 1:** District URL (must contain `ps32`)  
- **Argument 2:** Name of the output CSV file  

### Expected Console Output

```
Fetching data from: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6203
Saving to: results_brno_venkov.csv
Done!
```

## 3. Verify CSV

Open `results_brno_venkov.csv` and confirm:

- The **header** is exactly:
  ```
  code;location;registered;envelopes;valid;ANO 2011;Blok proti islam.-Obran.domova;CESTA ODPOVĚDNÉ SPOLEČNOSTI;Dobrá volba 2016;Dělnic.str.sociální spravedl.;Komunistická str.Čech a Moravy;Křesť.demokr.unie-Čs.str.lid.;Národ Sobě;Občanská demokratická aliance;Občanská demokratická strana;REALISTÉ;ROZUMNÍ-stop migraci,diktát.EU;Radostné Česko;Referendum o Evropské unii;SPORTOVCI;SPR-Republ.str.Čsl. M.Sládka;STAROSTOVÉ A NEZÁVISLÍ;Strana Práv Občanů;Strana svobodných občanů;Strana zelených;Svob.a př.dem.-T.Okamura (SPD);TOP 09;Česká pirátská strana;Česká str.sociálně demokrat.;Česká strana národně sociální;Řád národa - Vlastenecká unie
  ```
- The **first three rows** match the example above.

## Python Version

Tested on Python 3.13.3 (Windows)

## Contact

**Ivo Doležal**  
Email: ivousd@gmail.com  
GitHub: @IvanekLumberjack888

-------------------------------------------------------------------------------------------------------

---CZE---

# Election Scraper – Volby 2017

**Třetí projekt Engeto Online Python Akademie**

## Itinerář

1. Příprava prostředí  
   a) Otevřete terminál a přejděte do složky projektu  
   b) Vytvořte virtuální prostředí  
   c) Aktivujte virtuální prostředí  
   d) Aktualizujte pip  
   e) Nainstalujte závislosti z `requirements.txt`  

2. Spuštění skriptu  
   a) Zadejte:
   ```
   python main.py "" ""
   ```
   b) Počkejte na výpis:
   ```
   Fetching data from: 
   Saving to: 
   Done!
   ```

3. Kontrola výstupu  
   Otevřete CSV v Excelu nebo v textovém editoru a ověřte, že hlavička a první řádky vypadají takto:

   ```
   code;location;registered;envelopes;valid;ANO 2011;Blok proti islam.-Obran.domova;CESTA ODPOVĚDNÉ SPOLEČNOSTI;Dobrá volba 2016;Dělnic.str.sociální spravedl.;Komunistická str.Čech a Moravy;Křesť.demokr.unie-Čs.str.lid.;Národ Sobě;Občanská demokratická aliance;Občanská demokratická strana;REALISTÉ;ROZUMNÍ-stop migraci,diktát.EU;Radostné Česko;Referendum o Evropské unii;SPORTOVCI;SPR-Republ.str.Čsl. M.Sládka;STAROSTOVÉ A NEZÁVISLÍ;Strana Práv Občanů;Strana svobodných občanů;Strana zelených;Svob.a př.dem.-T.Okamura (SPD);TOP 09;Česká pirátská strana;Česká str.sociálně demokrat.;Česká strana národně sociální;Řád národa - Vlastenecká unie
   ;Babice nad Svitavou;925;660;660;129;0;2;0;1;31;69;0;0;109;2;3;0;0;1;3;53;1;10;7;58;39;93;43;0;1
   ;Babice u Rosic;553;353;353;93;0;0;0;1;30;25;0;2;32;4;1;1;0;1;1;27;0;6;5;49;13;37;18;5;0
   ;Běleč;160;131;131;30;0;0;0;0;14;14;0;0;13;0;1;0;1;0;0;8;0;0;0;12;1;11;25;0;0
   ```

## 1. Příprava prostředí

```bash
cd cesta/ke/projektu
python -m venv .venv

# PowerShell
.venv\Scripts\Activate.ps1

# CMD
.venv\Scripts\activate.bat

python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Spuštění skriptu

```bash
python main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6203" "vysledky_brno_venkov.csv"
```

- **Argument 1:** URL okresu (obsahuje `ps32`)  
- **Argument 2:** Název výstupního CSV  

### Ukázka výstupu

```
Fetching data from: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6203
Saving to: vysledky_brno_venkov.csv
Done!
```

## 3. Kontrola CSV

Otevřete `vysledky_brno_venkov.csv` a ověřte, že:

- **Hlavička** je:
  ```
  code;location;registered;envelopes;valid;ANO 2011;Blok proti islam.-Obran.domova;CESTA ODPOVĚDNÉ SPOLEČNOSTI;Dobrá volba 2016;Dělnic.str.sociální spravedl.;Komunistická str.Čech a Moravy;Křesť.demokr.unie-Čs.str.lid.;Národ Sobě;Občanská demokratická aliance;Občanská demokratická strana;REALISTÉ;ROZUMNÍ-stop migraci,diktát.EU;Radostné Česko;Referendum o Evropské unii;SPORTOVCI;SPR-Republ.str.Čsl. M.Sládka;STAROSTOVÉ A NEZÁVISLÍ;Strana Práv Občanů;Strana svobodných občanů;Strana zelených;Svob.a př.dem.-T.Okamura (SPD);TOP 09;Česká pirátská strana;Česká str.sociálně demokrat.;Česká strana národně sociální;Řád národa - Vlastenecká unie
  ```
- **První tři řádky** jsou:
  ```
  ;Babice nad Svitavou;925;660;660;129;0;2;0;1;31;69;0;0;109;2;3;0;0;1;3;53;1;10;7;58;39;93;43;0;1
  ;Babice u Rosic;553;353;353;93;0;0;0;1;30;25;0;2;32;4;1;1;0;1;1;27;0;6;5;49;13;37;18;5;0
  ;Běleč;160;131;131;30;0;0;0;0;14;14;0;0;13;0;1;0;1;0;0;8;0;0;0;12;1;11;25;0;0
  ```

## Verze Python

Testováno na Python 3.13.3 (Windows)

## Kontakt

**Ivo Doležal**  
Email: ivousd@gmail.com  
GitHub: @IvanekLumberjack888