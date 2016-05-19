# comments

## Spustenie

#### Terminal

```
python manage.py runserver
```

#### Browser

http://127.0.0.1:8000/article/3/

## Riešenie

#### Script na generovanie dát

Na vytvorenie vzorových dát bol použitý script ktorého funkcionalita sa nachádza v súbore `script.py`.
V tomto súbore sa dá nastaviť počet vygenerovaných článkov, počet komentárov na najvyššej úrovni a hĺbka vnorenia komentárov.
Na vyplnenie atribútov vytváraných objektov článku a komentára bolo použité rozšírenie `faker`, ktoré umožňuje generovanie náhodného textu alebo mien.

<a href="https://github.com/joke2k/faker/" target="_blank">Github repository</a>

<a href="https://pypi.python.org/pypi/fake-factory" target="_blank">Python packages site</a>

Tento script v cykle vytvorí článok a následne vytvorý k tomuto článku komentáre a k týmto komentárom ďalšie podkomentáre do vopred stanovenej hĺbky. Počet podkomentárov sa volí náhodne z intervalu 0 až počet komentárov na úrovni rodiča tohto komentára a to celé predelené dvomi.

##### Spustenie scriptu

> Poznámka: Aby pre spustenie zadania nebolo potrebné inštalovať rozšírenie `faker` bolo toto rozšírenie zakomentované v súbore `settings.py` v zozname nainštalovaných aplikácií ako aj celý zdrojový kód scriptu.

```
python manage.py shell < script.py
```

### Opis možností a funkcionalít

Po zobrazení niektorého z článkov sa zobrazí jeho vygenerovaný obsah ako napríklad názov, autor, obsah článku a kedy
bol vytvorený.
Pod obsahom článku sa nachádzajú odkazy na zvyšné články vo vygenerovanej databáze a pod nimi je možnosť na zobrazenie
komentárov k článku.
Prostredníctvom tlačidla `Show comments` sa objaví 10 najnovších komentárov na najvyššej úrovni k tomuto článku a
jednoduchý formulár na pridávanie komentárov obsahujúci pole na prezývku a pole na obsah komentáru.
Formulár je ošetrený aby nebolo možné pridávanie komentárov bez mena/prezývky alebo bez obsahu.
Po pridaní komentára sa tento nový komentár automaticky objavý na zaciatku zoznamu načítaných komentárov.
Po načítaní prvých desiatich komentárov sa zmení popis tlačidlo `Show comments` na `Load older comments` a po jeho
opetovnom stlačení sa načíta ďalších 10 komentárov na danej úrovni až kým nie su načítane všetky komentáre z tejto
úrovne a tlačidlo `Load older comments` sa zmení na oznam, že už nie su komentáre, ktoré by sa dali zobraziť.
Keďže táto aplikácia rieši vnorené komentáre je pri každom komentári z jednej úrovne, ktorý obsahuje ďalšie podkomentáre
možnosť zobrazenia prvých +10 z týchto podkomentárov a takto rekurzívne až kým nie su zobrazené všetky komentáre v
každej hĺbke.
Pri každom komentári je možnosť reagovať na daný komentár pomocou formuláru, ktorý sa zobrazí pod konkrétnym komentárom.
Pri každom komentári sú taktiež tlačidlá `+` a `-` a zobrazené celkové skóre komentáru. Po stlačení jedného z týchto
tlačidiel sa komentáru priráta alebo odráta jeden lajk a ukazovaťeľ lajkov zobrazí novú hodnotu.
Keďže toto zadanie nerieši prihlasovanie sa používateľov do systému je pridávanie lajkov ošetrené tak, aby bolo z
jedného prehliadača možné jednému komentáru pridať/odobrať práve jedne krát až do zatvorenia a znovuotvorenia
prehliadača.

### Opis riešenia

Zadanie bolo naimplementovane s použitím programovacieho jazyka `Python 3.5`, webového frameworku `Django 1.8.4` a
s použitím `javascriptu`, `cookies`, `html`, `css`.

#### Model komentáru a jeho zobrazenie

Návrh počíta s možnosťou reagovať do ľubovoľnej hĺbky. Zobrazenie reakcií je formou vetveného stromu.
Keďže návrh počíta s možnosťou reagovania na komentáre do ľubovoľnej hĺbky bol bodel komentára navrhnutý tak, ze
obsahuje záznam o prezývke používateľa a obsahu komentára, počte lajkov a nahlásení, že sa jedná o spam a taktiež
obsahue referenciu na článok k torému bol tento komentár vytvorený a referenciu na komentár ak bol daný komentár
reakciou na iný komentár.
Zobrazenie komentárov je riešené tak, že na prvej úrovni sú zobrazené komentáre bez referencie na iný komentár, čiže
komentáre priamo k článku, a následne pre každý z týchto komentárov sú zobrazené komentáre s referenciou na tento
komentár.
Z toho dôvodu toto riešenie nijak neobmedzuje hĺbku vnorenia komentárov. 

#### Načítavanie komentárov

Na stránke článku je pomocou tag-ov vytvorený a zobrazený script, tlačidlo, ktoré tento script po kliknutí zavolá a
ďalšie elementy.
Tento script volá ďalšiu javascriptovú funkciu s parametrami, ktorá prostredníctvom ajax-u a pohľadu zobrazujúceho
zoznam komentárov vráti html dáta s týmto zoznamom a ten pridá za predchádzajúcu stránku obsahujúcu komentáre.
Všetky vyššie spomenuté funkcionality pracujú na podobnom princípe.
Pomocou django tag-ov sú do html stránky detailu článku pridávané tlačidlá, scripty a ďalšie elementy.
Následne sú prostredníctvom týchto tlačidiel zavolané javascriptové funkcie, ktoré pomocou ajax-u volajú pohľady,
kde sa vykonajú potrebné akcie a tie su vrátené na pôvodnú stránku detailu článku a tam su zobrazené bez nutnosti
znovunačítania celej stránky.
Možnosť obmedzenia pridávania lajkov k jednému komentáru práve raz je vyriešená prostredníctvom `cookies`.
