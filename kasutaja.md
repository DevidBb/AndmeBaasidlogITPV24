## SQL Server – Kasutajate autentimine ja õiguste haldamine

[Põhimõisted](README.md) | [Protseduurid](protseduurid.md) | [Kasutajad](kasutaja.md) | [Trigerid](triger.md)

Mis on autentimine SQL Serveris?
 ### Autentimine tähendab kasutaja tuvastamist ehk kontrollimist, kas kasutajal on õigus SQL Serverisse sisse logida.

**SQL Serveris kasutatakse kahte peamist autentimise tüüpi:**

1. Windows Authentication
Selle puhul kasutatakse samu kasutajaandmeid, millega logitakse sisse Windows operatsioonisüsteemi.

>Kasutajanimi ja parool on seotud Windowsiga. 
>Turvalisem lahendus. 
>Paroole haldab Windows. 
>Kasutaja ei pea eraldi SQL Serveri parooli teadma.

2. SQL Server Authentication
>Selle puhul luuakse kasutaja otse SQL Serverisse.
>Kasutaja ei ole seotud Windowsiga. 
>Määratakse eraldi kasutajanimi ja parool. 
>Sobib veebirakenduste jaoks. 
---------------------------------------------------------------
**Näide kasutajast: DirectorIrina. Parool: director**
----------------------------------------------------------------
## Kasutaja loomine SQL Serveris
1. Serveritaseme kasutaja loomine (Login) Sammud Ava:
Security → Logins Tee permklikk ja vali:
New Login...
<img width="703" height="670" alt="{5CCD37E4-A09C-41A7-95F6-EFF636881D0C}" src="https://github.com/user-attachments/assets/a5a3adfa-9d64-475f-8d19-93ff6ea60468" />

Harjutamiseks võib eemaldada linnukese:  User must change password at next login.

**Server Roles**
Menüüst Server Roles saab määrata serveri üldised õigused.

Tavaliselt piisab rollist: public

<img width="629" height="560" alt="{D6BFEBCB-16AB-4B54-BE90-CEFE6D23C70C}" src="https://github.com/user-attachments/assets/c49cad2c-97e5-4c3c-ba50-bf62479ab11f" />


```sql
--GRANT - õiguste määramine
--DENY - õiguste keelamine
-- anname kasutajale õigus vaadata tabelit (SELECT), 
-- lisada admeid (INSERT) ning uuendada neid(UPDATE)
GRANT SELECT ON opilane TO direktorDevid;
GRANT INSERT ON opilane TO direktorDevid;
GRANT UPDATE ON opilane TO direktorDevid;

DENY DELETE ON opilane TO direktorDevid;
```
## Kasutaja õiguste kontroll

1. tuleb sisselogida kasutajana directorIrina. Connect--> Database Engine

<img width="706" height="648" alt="{FD4CA956-4FFD-418B-902D-88CDF871C499}" src="https://github.com/user-attachments/assets/a106e761-3196-4b12-ad90-f64d3c8987e7" />


2. saab tabeli sisu näha ja sisestada uus kiri.
<img width="441" height="85" alt="{92422C7E-F322-419C-BBC8-42A3D1A6D201}" src="https://github.com/user-attachments/assets/17f47336-ec9c-4484-afa6-9533ef38e4cf" />


3. saab lisada uusi andmeid.
<img width="325" height="97" alt="{01390BCD-9553-48B0-96EE-A8AFF3BD5CD6}" src="https://github.com/user-attachments/assets/cc79316e-4cb3-4866-b950-af30fd5ed19a" />


4. kontrollime tegevus, mis ei ole lubatud kasutajale, näiteks andmete loomine
<img width="469" height="529" alt="{13900007-E5F8-4641-B899-4F9E92052147}" src="https://github.com/user-attachments/assets/85b23263-7c19-42d3-9f8a-6bd83055b233" />

5. Selle käsuga saate kontrollida, millised õigused meie kasutajal on.
<img width="524" height="445" alt="{9240A347-A2C4-4208-8B50-63D88F6FF864}" src="https://github.com/user-attachments/assets/d3fc8ca7-77bb-4c3b-8d67-0801e6dfc3c8" />
<img width="304" height="256" alt="{D6516948-9116-434D-9B98-80E5D1336AE3}" src="https://github.com/user-attachments/assets/9895919f-10af-4b8d-aa85-5569cb3c8793" />
