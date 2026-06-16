create table turniir(
turniirid int primary key identity(1,1),
turniirnimi varchar(35));


CREATE TABLE voistlus (
    voistlusid int primary key identity(1,1),
    voistlusnimi varchar(100) NOT NULL,
    osalejate_arv int,
    turniirid int,
    foreign key (turniirid) references turniir(turniirid)
);

CREATE TABLE osaleja (
    osalejaid int primary key identity(1,1),
    osalejanimi varchar(100) NOT NULL,
    voistlusid int,
    foreign key (voistlusid) references voistlus(voistlusid)
);


INSERT INTO voistlus (voistlusnimi, osalejate_arv, turniirid)
VALUES
('Jalgpallivõistlus', 20, 1);
('Korvpallivõistlus', 16, 2),
('Maleturniir', 12, 3),
('Tenniseturniir', 8, 4),
('Ujumisvõistlus', 25, 5);


INSERT INTO osaleja (osalejanimi, voistlusid)
VALUES
('Martin Tamm', 21),
('Kati Saar', 22),
('Rasmus Kask', 23),
('Laura Põld', 24),
('Markus Oja', 25);


Create table logi(
id int PRIMARY KEY IDENTITY (1,1),
kuupaev DATETIME,
kasutaja varchar (30),
toiming varchar(100), -- tegevus
andmed TEXT) -- tabelist linnad

select * from turniir
select * from voistlus
select * from osaleja
select * from logi


create trigger voistlusKustutamine
on voistlus
for delete
as
insert into logi (kuupaev, kasutaja, toiming, andmed)
select
    GETDATE(),
    SYSTEM_USER,
    'on tehtud DELETE käsk',
    concat(
        'võistlus: ', deleted.voistlusnimi,
        ', osalejate arv: ', deleted.osalejate_arv,
        ', turniir ID: ', deleted.turniirid
    )
from deleted;

delete from voistlus
where voistlusid = 26;

create trigger voistlusLisamine
on voistlus
for insert
as
insert into logi (kuupaev, kasutaja, toiming, andmed)
select
    GETDATE(),
    SYSTEM_USER,
    'on tehtud INSERT käsk',
    CONCAT(
        'võistlus: ', inserted.voistlusnimi,
        ', osalejate arv: ', inserted.osalejate_arv,
        ', turniir ID: ', inserted.turniirid
    )
FROM inserted;

INSERT INTO voistlus (voistlusnimi, osalejate_arv, turniirid)
VALUES ('hokkey', 12, 1);





CREATE PROCEDURE kuvaVoistlused
@turniiri_nimi varchar(35)
AS
SELECT voistlus.*
FROM voistlus, turniir
WHERE voistlus.turniirid = turniir.turniirid
AND turniir.turniirnimi = @turniiri_nimi

EXEC kuvaVoistlused 'Thunder Cup'







CREATE LOGIN opilanedevid
WITH PASSWORD = 'Qmfjgid5zsk11@';


GRANT SELECT, INSERT ON voistlus TO opilanedevid;
GRANT SELECT, INSERT ON turniir TO opilanedevid;
GRANT SELECT, INSERT ON osaleja TO opilanedevid;
