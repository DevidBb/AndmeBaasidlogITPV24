```SQL
CREATE DATABASE klientprotseduur
use klientprotseduur

create table klient(
klient_id int PRIMARY KEY identity(1,1),
klient_name varchar(10) not null,
linn varchar(10) not null,
vanus int,
saldo money
)

INSERT INTO klient
VALUES('Anastasia', 'Narva', '36', '12500')

select * from klient

--Protseduur, mis tagastab kõik kliendid või valitud väljad (nimi, linn). 
CREATE Procedure kliendinimi_linn
AS 
BEGIN
	select klient_name, linn from klient
END;

--kutse
exec kliendinimi_linn

--Protseduur, mis lisab uue kliendi (nimi, linn, vanus, saldo). 
CREATE Procedure lisa_klient
--parameeter
@name varchar (10),
@linn varchar (10),
@vanus int,
@saldo money
AS
BEGIN
	INSERT INTO klient(klient_name, linn, vanus, saldo)
	VALUES (@name, @linn, @vanus, @saldo);
	select * from klient
END;

--kutse
EXEC lisa_klient 'Martin', 'Tallinn', 16, 250;

--Protseduur, mis uuendab linna väärtust ID alusel.
CREATE Procedure uus_andmed
--parameetrid
@veerg varchar(10),
@uustahendus varchar(10),
@id int
AS
BEGIN
    DECLARE @sqltegevus varchar(max);
	select * from klient;
	SET @sqltegevus =
		CONCAT('UPDATE klient SET ', @veerg,'=''', @uustahendus, '''	WHERE klient_id=', @id);
	PRINT @sqltegevus;
    EXEC (@sqltegevus);
	select * from klient;
END;
drop procedure uus_andmed

--kutse
exec uus_andmed @uustahendus='169', @veerg='korgus', @id=3

-- Protseduur, mis kustutab kliendi ID järgi. 
CREATE procedure kustuta_klient
--parameeter
@delete_id int
AS
BEGIN
	SELECT * FROM klient;
	DELETE FROM klient WHERE klient_id=@delete_id
	SELECT * FROM klient;
END;

--kutse 
exec kustuta_klient 4

--Protseduur, mis otsib nime või esimese tähe järgi. 
CREATE PROCEDURE otsi_klienti
--parameeter
@taht char(1)
AS
BEGIN
	SELECT * FROM klient
	WHERE klient_name LIKE @taht + '%'; --% - teised sümboolid  
END;

--kutse
EXEC otsi_klienti 'Anton';

--Protseduur, mis leiab väikseima ja suurima saldo
CREATE PROCEDURE minmaxSaldo
--parameetrid
@minSaldo MONEY OUTPUT,
@maxSaldo MONEY OUTPUT
AS
BEGIN
	SELECT
		@minSaldo = MIN(saldo),
		@maxSaldo = MAX(saldo)
	FROM klient;
END;

--kutse
DECLARE @minSaldo MONEY, @maxSaldo MONEY;

EXEC minmaxSaldo @minSaldo OUTPUT, @maxSaldo OUTPUT;

PRINT 'Min hind = ' + CONVERT(varchar, @minSaldo);
PRINT 'Max hind = ' + CONVERT(varchar, @maxSaldo);

--Protseduur, mis kuvab iga kliendi kohta lisaveeru
CREATE Procedure kliendi_staatus
AS
BEGIN
	select klient_name, saldo,
		case
			WHEN saldo < 8000 THEN 'Hea klient'
			ELSE 'Tavaklient'
		END AS kliendi_staatus
	FROM klient;
END;

--kutse
exec kliendi_staatus

--Protseduur, mis lisab või kustutab veeru
CREATE procedure veerg_muutus
--parameetrid
 @tegevus varchar(10),
 @tabelinimi varchar(10),
 @veerunimi varchar(25),
 @tyyp varchar(25) = NULL
AS
BEGIN
    DECLARE @sqltegevus varchar(max);

    SET @sqltegevus = CASE 
        WHEN @tegevus = 'add' THEN 
            CONCAT('ALTER TABLE ', @tabelinimi, ' ADD ', @veerunimi, ' ', @tyyp)
        WHEN @tegevus = 'drop' THEN 
            CONCAT('ALTER TABLE ', @tabelinimi, ' DROP COLUMN ', @veerunimi)
    END;

    PRINT @sqltegevus;
    EXEC (@sqltegevus);
END;

drop procedure veerg_muutus

--kutse
EXEC veerg_muutus 'add', 'klient', 'korgus', 'int'

SELECT * FROM klient;

exec veerg_muutus 'drop', 'klient', 'testVeerg'
```
