[Põhimõisted](README.md) | [Protseduurid](protseduurid.md) | [Kasutajad](kasutaja.md) | [Trigerid](trigerid.md) | [Keys](keys.md)

andmebaaside haldusega seotud sql kood ja konspektid

## Sisukord
- [Põhimõisted](#põhimõisted)
- [Piirangud](#piirangud)
- [SQL](#sql)
- [Andmetüübid](#andmetüübid)
- [Tabelivahelised seosed](#tabelivahelised_seosed)
- [Alter table](#alter_table)

## Põhimõisted
- Andmebaasi haldussüsteemid - tarkvara, millega abil saab luua andmebaas (mariaDB - XAMPP, SQL Server - SQL Server Management Studio)
- Andmebaas - struktureeritud andmete kogum
- Tabel - olem - сущности
- Veerg = väli - поле
- Rida = kirje - запись
- Primaarne võti - Primary key -PK- veerg, unikaalse identifikaatoriga (tavaliselt nimetakse ID)- первичный ключ
- Välisvõti (võõrvõti) - Foreign key -FK- veerg, mis loob seose teise tabeli primaarne võtmega - вторичный ключ

## SQL 
structured query language - struktureeritud päringu keel - структуированый язык запросов
- päring - запрос
 <img width="450" height="366" alt="{0E671A89-7B3E-41A5-85A4-0413A085F037}" src="https://github.com/user-attachments/assets/995df4b8-e27f-4e94-b91d-2b77f932c952" />
 
1. DDL - Data Definition Language
2. DML - Data Manipulation Language

## Piirangud
Ограничения - Сonstraint (S)
1. PRIMARY KEY
2. NOT NULL
3. CHECK - valik
4. UNIQUE
5. FOREIGN KEY

## Andmetüübid
```
1. int, smallint, decimal(5,2) - numbrilised
2. varchar(30), char(5), TEXT - tekst/sümbolised
3. date, time, datetime - kuupäeva
4. boolean, bit, bool - loogilised
```

## Tabelivahelised_seosed
- üks-ühele (nt naine-mees)
- üks-mitmele (nt naine-lapsed)
- mitme-mitmele (nt õpilased-tunnid)

 <img width="832" height="698" alt="{4A665A97-EA30-4FE1-A967-FA147218F1DD}" src="https://github.com/user-attachments/assets/769e3aec-3885-490b-9857-79346db486e3" />

## ALTER_TABLE
Tabeli struktuuri muutmine
```
sql
--1. uue veeru lisamine
ALTER TABLE tootaja ADD testVeerg int;

--2. veeru kustumine
ALTER TABLE tootaja DROP COLUMN testVeerg;

--3. andmetüübi muutmine veerus
ALTER TABLE tootaja ALTER COLUMN testVeerg varchar(5);

--struktuuri kontrollimiseks kasutame protseduuri sp_help
sp_help tootaja;
```
  
