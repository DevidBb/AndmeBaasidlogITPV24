
[Põhimõisted](README.md) | [Protseduurid](protseduurid.md) | [Kasutajad](kasutaja.md) | [Trigerid](triger.md)

'''
use devitrigger24
Create table linnad(
linnID int PRIMARY KEY IDENTITY (1,1),
linnanimi varchar(15) NOT NULL,
rahvaarv int);
 
 insert into linnad(linnanimi, rahvaarv)
values('Tartu', 125633)


Create table logi(
id int PRIMARY KEY IDENTITY (1,1),
kuupaev DATETIME,
kasutaja varchar (30),
toiming varchar(100), -- tegevus
andmed TEXT) -- tabelist linnad
'''


Trigger linnaLisamine
'''
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

insert into linnad(linnanimi, rahvaarv)
values('Paide', 12976)
'''



Trigger linnaKustutamine
'''
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

delete from linnad where linnID=1
'''

Trigger linnaUuendamine
'''
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

update linnad set linnanimi='Narva', rahvaarv=676767 where linnanimi='Narva'
'''

Grant for SekretarDevid
'''
grant select, insert, delete, update on linnad to sekretarDevid;
deny select, delete on logi to sekretarDevid;
'''
