# Andmebaasi võtmed (Keys)

[Põhimõisted](README.md) | [Protseduurid](protseduurid.md) | [Kasutajad](kasutaja.md) | [Trigerid](trigerid.md) | [Keys](keys.md)

## Primary Key 

### Definitsioon
Primary key - see on veerg (või veergude komplekt), mis identifitseerib tabeli iga rea ​​unikaalselt. Väärtused peavad olema unikaalsed ja ei tohi olla NULL.

### Kasutus
- Iga rea ​​unikaalse identifikaatorina
- Seoste jaoks teiste tabelitega (sellele viitab võõrvõti)
- Kiireks otsinguks indeksi automaatseks loomiseks

### Erinevus
- Ei tohi sisaldada NULL - väärtusi
- Igal tabelil saab olla ainult ÜKS primaarvõti
- Väärtused peavad olema unikaalsed

### Näide
<img width="468" height="292" alt="image" src="https://github.com/user-attachments/assets/304082c4-d54a-485c-8f17-ce5c8fa54467" />

<img width="215" height="116" alt="image" src="https://github.com/user-attachments/assets/80e7c542-7c72-4bfe-ae21-4f2c5fb60d1b" />

## Foreign Key 

### Definitsioon
Foreign key - see on ühe tabeli väli või väljade rühm, mis viitab teise tabeli primaarvõtmele.

### Kasutus
- Andmete terviklikkuse tagamiseks
- Tabelite vaheliste seoste loomiseks (1:M, M:M seosed)
- Orbkirjete vältimiseks

### Erinevus
- Võib sisaldada NULL-väärtusi
- Saab viidata ainult teises tabelis olemasolevatele väärtustele
- Ühel tabelil võib olla mitu võõrvõtit

### Näide
<img width="545" height="345" alt="image" src="https://github.com/user-attachments/assets/9458676e-be74-4981-b9c2-c2ffa6b4550e" />

<img width="1321" height="169" alt="image" src="https://github.com/user-attachments/assets/c95619a5-6d0f-40e3-8b47-b65a7eb2bdc3" />
Me ei saanud andmeid sisestada, kuna tabelis Kasutaja puudub väli, mille id oleks 4.

## Unique Key

### Definitsioon
Unique key - see on andmebaasides piirang, mis tagab, et kõik konkreetse veeru (või veergude kombinatsiooni) väärtused on kogu tabelis unikaalsed.

### Kasutus
- Alternatiivse unikaalse identifikaatorina
- Duplikaatide vältimiseks (nt email)
- Andmete kvaliteedi tagamiseks

### Erinevus
- Võib lubada ÜHE NULL väärtuse
- Tabelis võib olla mitu unique key'd
- Unikaalsus on ainus nõue\

### Näide
<img width="333" height="263" alt="image" src="https://github.com/user-attachments/assets/0eeecfcd-3af9-48dc-bc60-863e212b1fbb" />

<img width="1150" height="170" alt="image" src="https://github.com/user-attachments/assets/f4880090-0a3b-4b0b-b27c-dc23d737dcfa" />

## Simple Key

### Definitsioon
Simple key - see on võti, mis koosneb ainult ühest veerust, mis identifitseerib unikaalselt iga kirje (rea) tabelis.

### Kasutus
- Lihtsate tabelite puhul, kus üks väli on piisav
- Enamiku tabelite puhul vaikimisi lahendus
- Kiirem indekseerimine

### Erinevus
- Üksikväli: Täpselt ühes veerus (näiteks õpilase_id või e-posti aadress).
- Unikaalne: Igal real on oma väärtus, duplikaadid pole lubatud.
- Not Null: Väärtus ei tohi olla tühi.

### Näide
<img width="317" height="286" alt="image" src="https://github.com/user-attachments/assets/4f488ff1-92db-4fff-8b96-eebfadda44d0" />

<img width="1100" height="228" alt="image" src="https://github.com/user-attachments/assets/877a5ba3-1725-40bb-83df-6c2a048a86a7" />

## Composite Key

### Definitsioon
Composite Key - see on kahe või enama veeru kombinatsioon, mida kasutatakse tabeli iga rea ​​unikaalseks identifitseerimiseks. Erinevalt tavalisest primaarvõtmest, kus üks väli tagab unikaalsuse, on liitvõtmes unikaalne ainult väljade kombinatsioon.

### Kasutus
- Vahetabelites (many-to-many seostes)
- Kui üks veerg ei ole piisav unikaalsuse tagamiseks
- Naturaalsete võtmete loomiseks

### Erinevus
- Koosneb mitmest veerust
- Kõik veerud koos moodustavad unikaalse kombinatsiooni
- Üksikud veerud ei pea olema unikaalsed

### Näide
<img width="372" height="323" alt="image" src="https://github.com/user-attachments/assets/a9ca2f93-691b-4f30-ad83-7392d56dd58e" />

<img width="1142" height="206" alt="image" src="https://github.com/user-attachments/assets/e82fe020-5fb8-4929-a7aa-1ac3a574f76b" />

## Compound Key

### Definitsioon
Compound Key - see on primaar- ehk unikaalne võti on võti, mis koosneb kahest või enamast veerust. Kombineerituna identifitseerivad need veerud unikaalselt iga tabeli rea, kuigi individuaalselt võivad nende väärtused dubleeruda.

### Kasutus
- Välisvõtmete loomiseks, mis viitavad composite primaarvõtmele
- Keerukate andmebaaside sidumisel
- Tabelite vaheliste seoste loomiseks

### Erinevus
- Tavaliselt kasutatakse kui välisvõtit (FOREIGN KEY)
- Võib koosneda mitmest välisvõtmest
- Viitab teise tabeli liitvõtmele

### Näide
<img width="509" height="275" alt="image" src="https://github.com/user-attachments/assets/d508ea22-5f93-4cf9-b03b-af4f4ec2b33b" />

<img width="720" height="368" alt="image" src="https://github.com/user-attachments/assets/95b0abe0-732c-4981-9dc8-da523f5c85de" />

<img width="1128" height="148" alt="image" src="https://github.com/user-attachments/assets/956d8e3c-3b5d-4cfe-ad78-0077cd012f65" />

## Superkey

### Definitsioon
Superkey - see on üks või mitu veergu, mille kombinatsioon identifitseerib unikaalselt mis tahes tabeli kirje. Supervõtme põhiomadus on see, et see võib sisaldada mis tahes "lisa"veergusid, mis ei mõjuta unikaalsust ennast.

### Kasutus
- Teoreetiline alus teistele võtmetele
- Andmebaasi normeerimisel
- Kõigi võimalike unikaalsete kombinatsioonide leidmiseks

### Erinevus
- Võib sisaldada "ülearuseid" veerge
- Kõik candidate key'd on superkey'd
- Kõige laiem võtmete tüüp

### Näide
<img width="838" height="300" alt="image" src="https://github.com/user-attachments/assets/3b43acd5-f737-44e1-9983-ac6f11c82cf9" />

<img width="550" height="352" alt="image" src="https://github.com/user-attachments/assets/c3a1dcd0-0479-4764-b668-ae7beb88af04" />

## Candidate Key

### Definitsioon
Candidate Key - see on minimaalne supervõti. See ei sisalda lisaveergusid. Iga kandidaatvõtit saab kasutada primaarvõtmena.

### Kasutus
- Primaarvõtme valimiseks
- Alternatiivsete unikaalsete identifikaatorite leidmiseks
- Andmebaasi disainimisel

### Erinevus Superkey'st
- Superkey võib sisaldada ülearuseid veerge
- Candidate key EI sisalda ülearuseid veerge (minimaalne)
- Iga Candidate key on Superkey, aga mitte vastupidi

### Näide
<img width="1047" height="389" alt="image" src="https://github.com/user-attachments/assets/3cd2b2d7-0079-4d3e-9248-3d0ed9b40e68" />

## Alternate Key

### Definitsioon
Alternate key - see on candidate key, mida ei valitud primaarvõtmeks. Kõik candidate key'd peale ühe saavad alternate key'deks.

### Kasutus 
- Alternatiivseks otsinguks tabelis
- Teiste veergude unikaalsuse tagamiseks
- Täiendava viisina kirje leidmiseks

### Erinevus
- See on Candidate Key, aga mitte Primary Key
- Kasutab UNIQUE constraint'it
- Tabelis võib olla mitu alternate key'd

### Näide
<img width="1081" height="359" alt="image" src="https://github.com/user-attachments/assets/ed689ded-9c79-44e1-abf7-6677bca0c170" />
