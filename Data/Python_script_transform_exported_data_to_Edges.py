# Tietokannasta ulosotetussa CSV:ssä henkilöt ovat riveittäin:
# Tapaus_ID,	Role_ID,	Role_name,	Person_ID,	Normalisoitu,	Pääluokka,	Alaluokka
# Role_Name ja Normalisoitu ovat turhia, sillä ID:n avulla saadaan ne myöhemmin.
# Esim. Role_ID = 1 = Kantaja/Asianomainen. Person _ID = 400 = Henrich Huttunen
# Kaikilla samassa oikeustapauksessa olevilla henkilöillä on yhteinen Tapaus_ID.
# Network analyysia varten henkilöt pitää olla pareittain. Tietokantaa täytyy siis muuttaa siten, että tehdään kaikki mahdolliset
# parit jokaisen oikeustapauksen osalta.

# Tiedoston avaaminen ja purku
import csv
with open ("C:/Users/Ville kone/OneDrive/Digital Humanities opinnot/Computational literacy for the humanities and social sciences (metodikurssi)/qry_Roolit_csv.csv") as f:
    roolit=[] # alustetaan lista, johon CSV puretaan
    for rivi in csv.reader(f, delimiter=";"):
        roolit.append(rivi) # jokainen rivi lisätään listana roolit listaan

# Yhdistetään Tapaus_ID perusteella samat henkilöt, käytetään sanakirjaa.
# Avain = Tapaus_ID. Arvo=Lista. Listalla ekana on lista, jossa henkilöt ovat tupleina (henkilö_id, rooli_id)
skirja={} # alustetaan sanakirja
for alkio in roolit:
    if alkio[0] not in skirja: #mikäli Tapaus_ID ei vielä löydy sanakirjasta, alustetaan se
        skirja[alkio[0]]=[[(alkio[3],alkio[1])],alkio[5],alkio[6]] #skirja[Tapaus_ID]=[[(henkilö_id, rooli_id)], Pääluokka, Alaluokka]
    elif alkio[0] in skirja: #mikäli Tapaus_ID löytyy, lisätään vain henkilö
        lisays=(alkio[3],alkio[1]) #(henkilö_id, rooli_id)
        skirja[alkio[0]][0].append(lisays)

# Huomataan että otsikot on livahtaneet mukaan, joten poistetaan ne varmuuden vuoksi, ettei tule ongelmia
del skirja["Tapaus_ID"]

# Nyt kun meillä on sanakirja, jossa kaikki henkilöt ovat saman tapauksen alla, voidaan tehdä pareja
parit={} # käytetään taas sanakirjaa, alustetaan uusi
for alkio in skirja.items(): # iteroidaan vanhan sanakirjan läpi
    mylist=(alkio[1][0]) # tallennetaan muuttujaan mylist, kaikki henkilö_id-rooli_id tuplet, jotka kyseisessä tapauksessa on
    res = [(a, b) for idx, a in enumerate(mylist) for b in mylist[idx + 1:]]
    # Yllä oleva on copy-pastettu netistä. Tekee uuden listan, jossa kaikki aiemman listan arvot mahdollisina pareina.
    # Tämä oli siitä hyvä, että se tekee uniikkeja pareja. esim. jos lista on [1,2,3] se tekee [[1-2], [1-3], [2-3]] eikä [[1-2],[1-3],[2-1],[2-3],[3-1],[3-2]]
    parit[alkio[0]]=[res, alkio[1][1], alkio[1][2]] #parit[Tapaus_ID]=[[kaikki parit], Pääluokka, Alaluokka]

# Uuden CSV:n otsikko ja rivit
otsikot=["Osapuoli_1","Osapuoli_2","Suhde","Pääluokka","Alaluokka","Tapaus_ID"] #otsikkorivi
rivit=[] # alustetaan rivit
for avain, arvo in parit.items(): # Iteroidaan sanakirjaa läpi
    for alkio in arvo[0]: # Iteroidaan pari kerrallaan
        eka_osapuoli=alkio[0][0] # Osapuoli_1:n henkilö_ID
        toka_osapuoli=alkio[1][0] # Osapuoli_2:n henkilö_ID
        suhde=f"{alkio[0][1]}–{alkio[1][1]}" # Tehdään rooli_id:eistä "suhdetyyppi" esim. "1–2" on "kantaja/asianomistaja - vastaaja/syytetty" 
        rivit.append([eka_osapuoli,toka_osapuoli,suhde,arvo[1],arvo[2],avain]) # Tehdään rivit otsikkorivin mukaisesti

# Uuden CSV:n kirjoittaminen
tnimi="C:/Users/Ville kone/OneDrive/Digital Humanities opinnot/Computational literacy for the humanities and social sciences (metodikurssi)/edges.csv"
with open(tnimi, "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(otsikot)
    csvwriter.writerows(rivit)