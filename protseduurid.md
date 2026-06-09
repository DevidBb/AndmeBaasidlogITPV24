[Põhimõisted](README.md) | [Protseduurid](protseduurid.md) | [Kasutajad](kasutaja.md) | [Trigerid](trigerid.md) | [Keys](keys.md)


store procedure - salvestatud protseduurid - sama miis on funktsioonid programmeerimises, mingi tegevus, mis 
on salvestatud andmebaasi, ja mida saab automaatsel teha(INSERT, UPDATE, SELECT, UPDATE).

```SQL
CREATE Procedure lisaKategooria
--parameetrid @...
@uusKategooria varchar(30)
AS
BEGIN
--kirjeldus
	INSERT INTO categories(category_name)
	VALUES(@uusKategooria);
	SELECT * FROM categories;
END;

--kutse
EXEC lisaKategooria 'Tablet';
```

<img width="318" height="260" alt="{22599276-CE5D-4B4F-BB06-EFC67722B238}" src="https://github.com/user-attachments/assets/8630208a-82ad-448b-bad2-c2dd3f57799b" />

```SQL
-- protseduur, mis kustutab kategooria id järgi
CREATE procedure kustutaKategooria
@kustutaId int
AS
BEGIN
	SELECT * FROM categories;
	DELETE FROM categories WHERE category_id=@kustutaId
	SELECT * FROM categories;
END;

--kutse
EXEC kustutaKategooria 1
```
<img width="321" height="265" alt="{A1CE72B0-7DF4-426A-A41C-4D8B43E3A4AC}" src="https://github.com/user-attachments/assets/d6d17c26-5d81-450e-8425-9816e96fa81a" />

```SQL
--protseduur mis kuvab kategooriad sisestatud esimese tähte järgi
CREATE PROCEDURE otsing1taht
@taht char(1)
AS
BEGIN
	SELECT * FROM categories
	WHERE category_name LIKE @taht + '%'; --% - teised sümboolid  
END;

--kutse
EXEC otsing1taht 'A';
```
<img width="300" height="124" alt="{72689C8C-3373-48DF-978A-512D01E47C59}" src="https://github.com/user-attachments/assets/9c4632df-308c-4eae-9d95-b2e58d2489f3" />

```SQL
--brandid
create table brands(
brandId int Primary Key identity(1,1),
brand_name varchar(15) UNIQUE);
Insert into brands(brand_name)
values('Apple')
select * from brands;

--3. products
Create table products(
productId int primary key identity(1,1),
product_Name varchar(50) not null,
brandId int, 
foreign key (brandId) references brands (brandId),
category_Id int,
foreign key (category_Id) references categories(category_Id),
model_year int,
list_price money);


INSERT INTO products
values ('Samsung S23', 1, 3, 2025, 720);
select * from products
--protseduur, mis kuvab tooded, kus on hind suurem kui sisestatud
create procedure suuremHind
@hind int
AS
BEGIN
	SELECT * FROM  products
	WHERE list_prices > @hind;
END;

--kutse
EXEC suuremHind 400;
```
<img width="487" height="124" alt="{A0E47DC7-17D0-446E-BCD0-C544995F86FE}" src="https://github.com/user-attachments/assets/2eefa158-718b-4f9e-9066-de1ad9ed8582" />

```SQL
--OUTPUT parameetr
CREATE PROCEDURE minmaxHind
	@minHind MONEY OUTPUT,
	@maxHind MONEY OUTPUT
AS
BEGIN
	SELECT
		@minHind = MIN(list_prices),
		@maxHind = MAX(list_prices)
	FROM products;
END;

--kutse
DECLARE @minHind MONEY, @maxHind MONEY;

EXEC minmaxHind @minHind OUTPUT, @maxHind OUTPUT;

PRINT 'Min hind = ' + CONVERT(varchar, @minHind);
PRINT 'Max hind = ' + CONVERT(varchar, @maxHind);
```
<img width="360" height="142" alt="{C6A95442-BE5B-4ADA-A2B1-30B73FDA77D7}" src="https://github.com/user-attachments/assets/f3921c03-a1dc-40c9-8318-cb6b2a41b45c" />

```SQL
--6. universaalne protseduur, mis töötab üks kõik millise tabeliga
-- muudab struktuuri(veeru lisamine -ADD, veeru kustutamine -DROP)

CREATE PROCEDURE muudatus
    @tegevus varchar(10),
    @tabelinimi varchar(25),
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

EXEC muudatus 'add', 'categories', 'testVeerg', 'int' 

SELECT * FROM categories;

EXEC muudatus 'drop', 'categories', 'testVeerg'
```
<img width="576" height="179" alt="{F93CE584-3AE6-47DF-91C2-420A8CC120D1}" src="https://github.com/user-attachments/assets/1e990331-eccf-46bc-9ecb-abc675ef4060" />
<img width="518" height="165" alt="{F9EE8A99-3795-4DF8-BCE1-18C69035E07E}" src="https://github.com/user-attachments/assets/ab8c9e9a-9694-4811-ba27-f7878d97a688" />
