create database trigerDevid
use trigerDev

--1. tabel juhu sekretaar lisab andmed
Create table linnad(
linnID int PRIMARY KEY IDENTITY (1,1),
linnanimi varchar(15) NOT NULL unique,
rahvaarv int);

--2. tabel kus automaatselt salvestatakse 1. tabeli muudatused--logi
Create table logi(
id int PRIMARY KEY IDENTITY (1,1),
kuupaev DATETIME,
kasutaja varchar (30),
toiming varchar(100), -- tegevus
andmed TEXT) -- tabelist linnad

select * from linnad
select * from logi

insert into linnad(linnanimi, rahvaarv)
values('Tartu', 125633)

-- Trigger lisatud kirjeid jälgimiseks tabelis “linnad” – INSERT
-- Jälgib andmete sisestamine tabelis linnad ja teeb vastava kirje tabelis logi
CREATE TRIGGER linnaLisamine
ON linnad --tabelinimi, mis on vaja jälgida
FOR INSERT
AS
INSERT INTO logi(kuupaev, kasutaja, toiming, andmed)
SELECT
GETDATE(),  --aeg
SYSTEM_USER, --kasutaja mis on sisselogitud serverisse
'on tehtud INSERT käsk',  --toiming
concat ('linn:', inserted.linnanimi, ', rahvaarv:', inserted.rahvaarv)  --andmed tabelisy linnad
FROM inserted;

--insert trigeri kontroll
insert into linnad(linnanimi, rahvaarv)
values('Paide', 12976)

select * from linnad
select * from logi

--delete triger
CREATE TRIGGER linnaKustutamine
ON linnad --tabelinimi, mis on vaja jälgida
FOR DELETE
AS
INSERT INTO logi(kuupaev, kasutaja, toiming, andmed)
SELECT
GETDATE(),  --aeg
SYSTEM_USER, --kasutaja mis on sisselogitud serverisse
'on tehtud DELETE käsk',  --toiming
concat ('linn:', deleted.linnanimi, ', rahvaarv:', deleted.rahvaarv)  --andmed tabelisy linnad
FROM deleted;

delete from linnad where linnID=3

--drop trigger 
disable trigger linnaKustutamine on linnad;
enable trigger linnaKustutamine on linnad

select * from linnad
select * from logi

--Kombineerime INSERT ja DELETE triggerid
disable trigger linnaKustutamine on linnad;
disable trigger linnaLisamine on linnad;

CREATE TRIGGER linnaLisaKustuta
ON linnad --tabelinimi, mis on vaja jälgida
FOR INSERT, DELETE
AS
BEGIN
SET NOCOUNT ON;
	INSERT INTO logi(kuupaev, kasutaja, toiming, andmed)
	SELECT
	GETDATE(),  --aeg
	SYSTEM_USER, --kasutaja mis on sisselogitud serverisse
	'on tehtud INSERT käsk',  --toiming
	concat ('linn:', inserted.linnanimi, ', rahvaarv:', inserted.rahvaarv)  --andmed tabelisy linnad
	FROM inserted

	union all -- соединить все

	SELECT
	GETDATE(),  --aeg
	SYSTEM_USER, --kasutaja mis on sisselogitud serverisse
	'on tehtud DELETE käsk',  --toiming
	concat ('linn:', deleted.linnanimi, ', rahvaarv:', deleted.rahvaarv)  --andmed tabelisy linnad
	FROM deleted;
END;

insert into linnad
values('Pärnu 2', 123476)

delete from linnad where linnanimi='Pärnu 2'

select * from linnad
select * from logi

--UPDATE triger
CREATE TRIGGER linnaUuendamine
ON linnad --tabelinimi, mis on vaja jälgida
FOR UPDATE
AS
INSERT INTO logi(kuupaev, kasutaja, toiming, andmed)
SELECT
GETDATE(),  --aeg
SYSTEM_USER, --kasutaja mis on sisselogitud serverisse
'on tehtud UPDATE käsk',  --toiming
concat ('vanad andmed - linn:', deleted.linnanimi, ', rahvaarv:', deleted.rahvaarv,
', uued andmed - linn', inserted.linnanimi, ', rahvaarv -', inserted.rahvaarv)  --andmed tabelisy linnad
FROM deleted inner join inserted 
on deleted.linnID=inserted.linnID;

update linnad set linnanimi='Narva222', rahvaarv=0 where linnanimi='Narva'

select * from linnad
select * from logi

--kasutaja sekretarDevid, parool 12345
--Õigused - sekretar ei saa luua ehk muuta trigerid, ei näi tabeli logi
--saab ainlut näha, lisada, ja kustutada tabelist linnad
grant select, insert, delete, update on linnad to sekretarRuslab;
deny select, delete on logi to sekretarDevid;
