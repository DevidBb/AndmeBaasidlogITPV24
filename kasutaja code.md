admin
```sql
create database kasutajaRUSLAN;

use kasutajaRUSLAN;
create table opilane(
opilaneID int primary key identity(1,1),
nimi varchar(30) not null,
vanus int,
aadress Text);

insert into opilane
values ('Nikita Mart', 24, 'Eesti, Tartu')

select * from opilane

--GRANT - õiguste määramine
--DENY - õiguste keelamine
-- anname kasutajale õigus vaadata tabelit (SELECT), 
-- lisada admeid (INSERT) ning uuendada neid(UPDATE)
GRANT SELECT ON opilane TO direktorRuslan;
GRANT INSERT ON opilane TO direktorRuslan;
GRANT UPDATE ON opilane TO direktorRuslan;

DENY DELETE ON opilane TO direktorRuslan;
```

kasutaja
```sql
use kasutajaRUSLAN;

select * from opilane

insert into opilane
values('test', 18, 'Eesti, Tallinn')

UPDATE opilane SET nimi='Arsen' WHERE opilaneID=3;

DELETE FROM opilane where opilaneID=2

--kasutame süsteemse funktsiooni, et vaadata oma õigusi
SELECT * from fn_my_permissions('opilane', 'OBJECT')
```
