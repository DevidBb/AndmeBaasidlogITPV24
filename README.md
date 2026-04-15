## sisukord
- [põhimõisted](#põhimõisted)
- [piirangud](#Piirangud)
- [andmetüübid](#andmetüübid)




# AndmeBaasidlogITPV24
andmebaaside haldusega seotud sql kood

# põhimõisted
- Andmebaasihaldussüsteemid - tarkvara, millega abil saab luua andmebaas(mariaDB - XAMPP,SQL Server- SQL Server Managment Studio) (server name (localdb)\MSSQLLocalDB)
- Andmebaas - strukteeritud andmete kogun
- tabel olem сущности
Veerg väli поле 
rida kirje запись
primaarne võti PK первичный ключ
välisvõti foreign key FK вторичный ключ

SQL-structuured query language - strukteeritud päringu keel   
<img width="427" height="339" alt="image" src="https://github.com/user-attachments/assets/6041d155-7a36-4013-8182-ff5bbcadf9e2" />
DDL - data definition language 
DML - data manipulation

# Piirangud - ограничения - CINSTRAINT (5)
1. primary key
2. foreign key
3. not null
4. check
5. 
# Andmeetüübid
```
1. int,smallint, decimal(5,2) - numbrilised
2. varchar(30), char(5), TEXT - tekst/sümbolised
3. date,time, datetime - kuupäev
4. boolean, bit ,bool - loogilised
```
`` - ctrl+e
# tabelivahelised seosed
üks-ühile (nt naine-mee)
üks-mitmele (nt naine-lapsed)
mitmele-mitmele
<img width="718" height="383" alt="{E0F4D3C8-3DC0-493B-A89C-6E27879854B5}" src="https://github.com/user-attachments/assets/9ae0dfbe-665d-4349-a1a0-9fd4d0c7d3f2" />

<img width="554" height="248" alt="{657E8891-B93F-4C50-AE7C-648B3F9B4E4B}" src="https://github.com/user-attachments/assets/19c9fadf-5029-468b-8d28-02ffa456a071" />

Какие из приведенных ниже типов SQL могут использоваться для хранения действительных чисел?
<img width="172" height="213" alt="{75C7B98E-9147-4884-B442-0AD7C52522FA}" src="https://github.com/user-attachments/assets/20f1050a-0f4d-4f02-9ccc-99775074e9e6" />

