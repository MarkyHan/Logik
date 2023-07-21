from itertools import combinations, permutations
import copy, sys


predchozi = [] #zde budu ukládat už provedené (vegenerované) kombinace čísel ("barev")

def kontrola(zadani, pokus):
    """
    Provede kontrolu daného pokusu a vrátí odpovídající počet černých (správná pozice) a bílých (správně pouze číslo ("barva"))
    :param zadani: zadaná kombinace zadaná uživatelem
    :param pokus: vegenerovaná kombinace určená ke kontrole
    :return: dvojice v pořadí počet černých, počet bílých
    """
    zadani2 = [True for i in range(5)] #pomocný seznam (kvůli možnosti opakování barev)
    pozice = 0
    barva = 0
    for i in range(len(pokus)):  #černé
        if pokus[i] == zadani[i]:
            pozice += 1
            zadani2[i] = False
    for i in range(len(pokus)): #bílé
        if pokus[i] in zadani and pokus[i] != zadani[i]:
            if zadani.count(pokus[i]) > 1:
                for x in range(len(zadani)):
                    if zadani[x] == pokus[i] and zadani2[x] is True:
                        barva += 1
                        zadani2[x] = False
                        break
            elif zadani2[zadani.index(pokus[i])] is True:
                barva += 1
                zadani2[zadani.index(pokus[i])] = False
    return pozice, barva

pocitadlo = 0 # počítá počet už provedených pokusů
def tisk(pokus):
    """
    Stará se o tisk předchozí kontroly daného pokusu, zároveň počítá počet už provedených pokusů
    pomocí globální proměnné pocitadlo
    :param pokus: daná vygenerovaná kombinace
    :return: vytiskne ohodnocení pokusu
    """
    global pocitadlo
    pozice = kontrola(zadani, pokus)[0]
    barva = kontrola(zadani, pokus)[1]
    pocitadlo += 1
    if pozice == 5:
        print(f"Pokus číslo {pocitadlo}: {pokus}, černé: {pozice}, bílé: {barva}")
        return print("správná kombinace, konec hry")
    return print(f"Pokus číslo {pocitadlo}: {pokus}, černé: {pozice}, bílé: {barva}")

def dalsi():
    """
    Spustí další generování dalšího pokusu.
    """
    global predchozi
    generuj(moznosti(zadani)[0], moznosti(zadani)[1], 0)

def moznosti(zadani):
    """
    Ze všech předchozích pokusů vyškrtá možnosti, kam se jednoznačně, které číslo ("barva") umístit nedá, nebo umístí
    jdenoznačné hodnoty
    :return: vrací dvojici: možné - seznam seznamů, u dané pozice jsou zbylé možnosti "barev", které se dají umístit
                            novy - nový, právě generovaný pokus, jednoznačné "barvy" už jsou umístěné (podle seznamu možné)
    """
    global predchozi
    novy = [0, 0, 0, 0, 0]
    mozne = [[i for i in range(1, 9)] for i in range(len(zadani))]
    for pokus in predchozi:
        if pokus[1][0] + pokus[1][1] == 0: #všechno špatně (hodnoty i pozice)
            for n in range(1,9):
                for m in range(len(mozne)):
                    if n in pokus[0] and n in mozne[m]:
                            mozne[m].remove(n)
        if pokus[1][0] == 0 and pokus[1][1] != 0: #špatně jsou pozice, nějaká hodnota je správně
            for n in range(len(mozne)):
                if pokus[0][n] in mozne[n]:
                    mozne[n].remove(pokus[0][n])
        if pokus[1][0] + pokus[1][1] == len(mozne): #mám hodnoty
            for i in range(1,9):
                for j in range(len(mozne)):
                    if i not in pokus[0] and i in mozne[j]:
                        mozne[j].remove(i)
    for v in range(len(mozne)): #nějaká pozice je jednoznačná
        if len(mozne[v]) == 1:
            novy[v] = mozne[v][0]
    if 0 not in novy and (novy, kontrola(zadani, novy)) not in predchozi: #vše je jednoznačné, tedy vlastně konec hry, mám správnou kombinaci
        tisk(novy)
        sys.exit()
    return mozne, novy


def generuj(mozne, novy, i):
    """
    Generuje nový pokus. Postupně procházím seznam starých pokusů (predchozi) a podle predchozi[i] (nebo predchozi[len(predchozi)-i-1])
    generuju novou kombinaci čísel
    :param mozne: u každého indexu mám seznam čísel, které můžu umístit
    :param novy: daný pokus, který generuju
    :param i: kolikátý pokus v předchozích právě procházím
    :return: vrátí nově vygenerovaný pokus
    """
    global predchozi #předchozí, už vygenerované pokusy
    if len(predchozi) == 0: #první možnost vygeneruji ručně, kvůli dalšímu šetření pokusů z predchozi
        novy = [1,1,1,2,2]
        tisk(novy)
        if kontrola(zadani, novy) != (5,0):
            predchozi.append((novy, kontrola(zadani, novy)))
            dalsi()
        sys.exit()
    else:
        pokus = predchozi[len(predchozi) - i - 1]  # pokus podle kterého doplňuju
        cerne = pokus[1][0] # správně "barva" i pozice
        bile = pokus[1][1] #správně pouze "barva"
        if cerne > 0: #nejprve umístím černé
            spravne = combinations([0, 1, 2, 3, 4], cerne) #indexy, ne hodnoty
            for moznost1 in spravne:
                tady = True
                novy1 = copy.deepcopy(novy)
                mozne1 = copy.deepcopy(mozne)
                for j in range(cerne):
                    if (pokus[0][moznost1[j]] in mozne1[moznost1[j]]):
                        novy1[moznost1[j]] = pokus[0][moznost1[j]]
                        mozne1[moznost1[j]] = [pokus[0][moznost1[j]]]
                    else:   #například už z předchozího generování nějaká "barva" nelze umístit a tedy už nebudu dál pokračovat v této moznost1
                        tady = False
                if tady is True:
                    for s in range(len(novy)): #další černé už nejsou
                        if s not in moznost1 and pokus[0][s] in mozne1[s]:
                            mozne1[s].remove(pokus[0][s])
                    for v in range(len(mozne1)): #umístím jednoznačné pozice
                        if len(mozne1[v]) == 1:
                            novy1[v] = mozne1[v][0]
                    if bile > 0 and [] not in mozne1: #pokračuju v umisťování podle bílých
                        pozice = []
                        for g in range(5):
                            if g not in moznost1: #indexy, ne hodnoty
                                pozice.append(g)
                        posun = list(permutations(pozice, bile))
                        for moznost2 in posun: #vyberu pozice, které chci umístit na jiné pozice.
                            # Nemusí to být jenom permutace těchto pozic, můžu to dát kamkoliv, kde je místo (nebo kde není ale rovná se to tomu, ale nemůžu vybrat ta místa
                            # kde jsem dávala z TOTOHO daného pokusu černé (z jiných pokusů už ano)!!). -> Tedy znovu chci indexy, které nejsou v moznost1
                            posun2 = list(permutations(pozice, bile)) # indexy KAM budu umisťovat
                            for moznost3 in posun2:
                                zde = True
                                novy2 = copy.deepcopy(novy1)
                                mozne2 = copy.deepcopy(mozne1)
                                if moznost2 != moznost3:
                                    for h in range(bile):
                                        if (moznost2[h] != moznost3[h]) and (pokus[0][moznost2[h]] != pokus[0][moznost3[h]]) and (pokus[0][moznost2[h]] in mozne2[moznost3[h]]):
                                            novy2[moznost3[h]] = pokus[0][moznost2[h]]
                                            mozne2[moznost3[h]] = [pokus[0][moznost2[h]]]
                                        else: #něco není možné umístit, v této moznost3 už dál nepokračuju
                                            zde = False
                                    if zde is True:
                                        for c in range(len(mozne2)):#další bílé nejsou, chci vymazat zbytek z mozne, abych nedostala potom stejne moznosti (barevne)
                                            for d in range(len(mozne2)):
                                                if (d not in moznost3) and (d not in moznost1) and (c not in moznost1) and(c not in moznost2) and (pokus[0][c] in mozne2[d]):
                                                    mozne2[d].remove(pokus[0][c])
                                        if [] not in mozne2: # v jiném případě už na nějaký index nemám, co umisťovat, tedy špatný pokus
                                            if i+1 < len(predchozi): #přesunu se na další pokus v předchozích
                                                generuj(mozne2, novy2, i+1)
                                            else: #všechny v předchozích už jsem prošla
                                                gener(novy2, mozne2, 0)
                    elif [] not in mozne1: #nemám bílé, jinak to stejné jako výše (a stále je u každého indexu potenciálně, co doplnit)
                        for c in range(len(mozne1)):#potřebuju oddělat z mozne, aby se mi neopakovaly bílé, ale zase pozor na možnost opakování barev přes černé
                            for d in range(len(mozne1)):
                                if (d not in moznost1) and (c not in moznost1) and (pokus[0][c] in mozne1[d]):
                                    mozne1[d].remove(pokus[0][c])
                        if [] not in mozne1: #na všechny pozice je potenciálně, co doplnit, je důvod pokračovat
                            if i + 1 < len(predchozi):
                                generuj(mozne1, novy1, i + 1)
                            else:
                                gener(novy1, mozne1, 0)
        elif bile > 0: #nemám černé, pouze bílé jinak stejné jako výše
            posun = list(permutations([0,1,2,3,4], bile))
            for moznost2 in posun:  # vyberu pozice, které chci umístit na jiné pozice.
                # Nemusí to být jenom permutace těchto pozic, můžu to dát kamkoliv, kde je místo (nebo kde není ale rovná se to tomu, ale nemůžu vybrat ta místa
                # kde jsem dávala z tohoto daného pokusu černé!!). -> Tedy znovu chci indexy, které nejsou v moznost1
                posun2 = list(permutations([0,1,2,3,4], bile))  # indexy KAM budu umisťovat
                for moznost3 in posun2:
                    zde = True
                    mozne2 = copy.deepcopy(mozne)
                    novy2 = copy.deepcopy(novy)
                    if moznost2 != moznost3:
                        for h in range(bile):
                            if (moznost3[h] != moznost2[h]) and (pokus[0][moznost2[h]] != pokus[0][moznost3[h]]) and (pokus[0][moznost2[h]] in mozne2[moznost3[h]]):
                                novy2[moznost3[h]] = pokus[0][moznost2[h]]
                                mozne2[moznost3[h]] = [pokus[0][moznost2[h]]]
                            else:
                                zde = False
                        if zde is True:
                            for c in range(len(mozne2)):# chci vymazat zbytek z mozne, abych nedostala potom stejne moznosti (barevne), ale taky ty černý ne jenom bílý
                                for d in range(len(mozne2)):
                                    if (d not in moznost3) and (c not in moznost2) and (pokus[0][c] in mozne2[d]):
                                        mozne2[d].remove(pokus[0][c])
                            if [] not in mozne2:
                                if i + 1 < len(predchozi):
                                    generuj(mozne2, novy2, i + 1)
                                else:
                                    gener(novy2, mozne2, 0)
        elif i+1 < len(predchozi): #nemám černé ani bílé, ale stále jsem neprošla všechny pokusy v předchozích
            generuj(mozne, novy, i+1)
        else: #nemám černé ani bílé, všechny pokusy v předchozích už prošlé
            gener(novy,mozne,0)

def gener(novy, mozne, i):
    """
    Spustí se při projití všech už vygenerovaných pokusů v předchozích, doplní prázdné pozici do právě generovaného nového pokus.
    Rekurzivně generujue všechny možné pokusy, při vygenerování první kombinace, která odpovídá hodnocení předchozích pokusů, se generování zastaví.
    :param novy: nově generovaný pokus, na pozice, kde je stále 0 se doplní hodnoty
    :param mozne: na daných indexech jsou seznamy možných hodnot, které lze umístit
    :param i: index
    :return: vytiskne vygenerovanou možnost, případně spustí generovaní dalšího pokusu
    """
    global predchozi
    if 0 not in novy:
        if (novy, kontrola(zadani, novy)) not in predchozi:
            k = True
            for u in predchozi:
                if kontrola(u[0], novy) != u[1]:
                    k = False
            if k is True:
                tisk(novy)
                if kontrola(zadani, novy) != (5, 0):
                    predchozi.append((novy, kontrola(zadani, novy)))
                    dalsi()
                sys.exit()
    elif i < len(novy):
        if novy[i] == 0:
            for j in mozne[i]:
                novy[i] = j
                gener(novy, mozne, i+1)
                novy[i] = 0
        else:
            gener(novy,mozne, i+1)

if __name__ == "__main__":
    h = False
    d = True
    while h is False:
        print("Vítejte! Prosím, zadejte kombinaci pěti čísel od 1 do 8.\nČísla oddělte mezerami, čísla se mohou opakovat.\nSvoji volbu potvrďte stisknutím klávesy Enter.")
        zadani = [int(i) for i in input().split()]
        for i in zadani:
            if (1 > i) or (i > 8):
                d = False
        if len(zadani) != 5:
            d = False
        if d is True:
            h = True
        else:
            print("Špatné zadání")
            d = True
    if d is True:
        print("Vaše zadaná kombinace:", *zadani)
        print("Řešení:")
        dalsi()