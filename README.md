## Sisukord
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



SQL CODE
``
Create Database Logitpv24baas

--ab kustutamine
drop database veebipood;


use Logitpv24baas;
CREATE TABLE tootaja(

tootajaID int PRIMARY KEY identity(1,1), --identiry - automaatselt kasvav arv
eesnimi varchar(15) not null,
perekonnanimi varchar(30) not null,
synniaeg date,
aadres TEXT,
koormus int CHECK (koormus>0), -- piirang,et koormus >0
aktiivne bit);

--taabeli kuuvamine 
select * from tootaja;

--andmete lisamine tabelisse
insert into tootaja(eesnimi,perekonnanimi,synniaeg,aadres,koormus,aktiivne)
values ('markus','atksassov','2007-07-07','tartu','120','1');
insert into tootaja
Values('leena','punane','2000-10-3','Tartu',120,1),
('oleg','mirov','2000-5-13','Narva',200,0)

update tootaja SET aadres='Tallinn', koormus=10, aktiivne=1
where tootajaID=1;

create table toovahetus(
toovahetusID int primary key identity(1,1),
kuupaev date,
tundideArv int,
tootajaID int,
FOREIGN KEY (tootajaID) References tootaja(tootajaID))

select * from toovahetus;
select * from tootaja;

insert into toovahetus
values ('2026-04-15',8.5,5)

create table koolitus(
koolitusID Int Primary key identity(1,1),
nimetus varchar(25) not null,
kestvus int,
algus datetime,
lopp datetime,
opetaja varchar(25) not null);

create table opitamine(
opitamineID int primary key identity(1,1),
kuuppaev date,
tunindeArv int,
tootajaID int,
foreign key (tootajaID) references tootaja(tootajaID),koolitusID int,

foreign key (koolitusID) references koolitus(koolitusID),tunnistus bit, hinne int)

select * from opitamine;
insert into opitamine
values ('a','a','a','a','a');

select * from koolitus;

``
