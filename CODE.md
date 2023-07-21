# Technická dokumentace
Všechny dosud vygenerované pokusy se spolu s ohodnocením ukládají do úložiště *predchozi*. První pokus se negeneruje (aby se mi nevygenerovaly samé 1 a abych neměla problém s indexováním podle pozice v *predchozi*). Samotné generování probíhá podle následujícího algoritmu:
## Funkce *dalsi*
Funkce *dalsi* spustí generování nového pokusu a to pomocí funkce *generuj* a *moznosti*.
## Funkce *moznosti* 
1. Vytvoří se seznamy *novy* a *mozne*. Seznam *novy* je samotný nově generovaný pokus délky 5, na počátku na každé pozici 0. *Mozne* je seznam seznamů délky 5, na každém indexu je seznam možných číslic, které lze umístit na danou pozici (tedy na počátku je na každém indexu seznam čísel od 1 do 8). Prochází se postupně všechny už vygenerované pokusy z~*predchozi* a podle jejich hodnocení se vyškrtávají hodnoty z *mozne* pokud:
	- součet černých a bílých se rovná 5 (neboli znám správné hodnoty); u každého indexu se odstraní všechny hodnoty, které v daném pokusu nejsou,
	- 0 černých, 0 bílých; u každého indexu se odstraní všechny hodnoty, které v daném pokusu jsou,
	- 0 černých; u každého indexu se odstraní příslušná hodnota na pozici v daném pokusu.
2. Do seznamu \textit{novy} se umístí jednoznačné hodnoty: při délce 1 nějakého seznamu ze seznamů v \textit{mozne}.
3. Pokud se v seznamu \textit{novy} nenachází 0, našla se správná kombinace, pokus se vypíše a~vyhodnotí; konec hry.
4. V opačném případě funkce vrátí dvojici \textit{mozne, novy} jako parametry funkce \textit{generuj}. 
## Funkce *generuj*
1. Parametry jsou: seznam *novy* - právě vytvářený pokus, pomocný seznam *mozne* s možnostmi na každou pozici a index, který značí index pokusu ze seznamu *predchozi*, generování probíhá od konce seznamu. 
2. U každého pokusu:
	- Pokud *cerne* $!= 0 $: vygeneruje se seznam všech možností, které hodnoty mohou být umístěny správně, rekurzivně se umísťují hodnoty podle jednotlivých možností a~vyškrtávají hodnoty, které naopak už na daných pozicích být nemohou (pokud daná hodnota stále ještě umístit lze (pomocí seznamu *mozne*)).
	- Pokud *bile* $!= 0 $: vygeneruje se seznam všech možností, které hodnoty mohou být v zadání, dále se vygeneruje seznam všech pozic, kam tyto hodnoty mohou být umístěny. Rekurzivně se umísťují hodnoty podle jednotlivých možností a vyškrtávají hodnoty, které naopak už na daných pozicích být nemohou (pokud daná hodnota stále ještě umístit lze (pomocí seznamu *mozne*)).
  - Pokud nejsou ještě vyhodnoceny všechny předchozí vygenerované pokusy, rekurzivně probíhá generování funkcí *generuj* s indexem +1.
	- Po vyhodnocení všech předchozích pokusů, pomocí funkce *gener* se doplní stále volné, nejednoznačné pozice do *nove* (nahradí se pozice s 0).
## Funkce *gener*
1. Parametry jsou: seznam *novy* - právě vytvářený pokus, pomocný seznam *mozne* s možnostmi na každou pozici a index, který značí pozici doplňovaného čísla.
2. Rekurzivně se pomocí *mozne* doplňují možné hodnoty do *nove*. 
3. Po doplnění všech hodnot (*0 not in novy*): zkontroluje se jestli hodnocení s každým z~předchozích pokusů odpovídá s hodnocením u tohoto daného pokusu, pokud ano, pokus se vytiskne a proběhne vyhodnocení pomocí funkce *kontrola*, v opačném případě pokračuje generování. Pokud se nejedná o vítězný pokus, pomocí funkce *dalsi* se spustí generování dalšího pokusu.
## Funkce *kontrola*
2. Parametry jsou: *zadani* - podle čeho se vyhodnocuje, *pokus* - co se vyhodnocuje.
3. Nejprve se vyhodnotí počet správných pozic (počet černých), následně počet bílých. Vyhodnocování probíhá pomocí pomocného boolean seznamu *zadani2* (kvůli možnému opakování hodnot v zadání). Vrátí dvojici v pořadí počet černých, počet bílých.
## Funkce *tisk*
1. Parametrem je vygenerovaný pokus, který chci vytisknout. Funkce také počítá počet už vygenerovaných pokusů. Spolu s počty černých a bílých (vygenerované funkcí *kontrola*) vytiskne také číslo pokusu.
