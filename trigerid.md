## Trigger - päästik

[Põhimõisted](README.md) | [Protseduurid](protseduurid.md) | [Kasutajad](kasutaja.md) | [Trigerid](triger.md)

### SQL triggerid on spetsiaalsed andmebaasi objektid, mis käivituvad automaatselt, kui toimub teatud sündmus (nt INSERT, UPDATE või DELETE).

Trigger lisatud kirjeid jälgimiseks tabelis “linnad” – INSERT
Jälgib andmete sisestamine tabelis linnad ja teeb vastava kirje tabelis logi
```sql
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
```
<img width="557" height="183" alt="{E393B9CD-C3D2-4773-BC87-1A6A018D558E}" src="https://github.com/user-attachments/assets/f0533482-53b8-41db-a0f0-3026f55b878e" />

Delete triger
```sql
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
```
<img width="563" height="180" alt="{16DE1A83-7BB8-42D7-ABF9-A142917E6D77}" src="https://github.com/user-attachments/assets/57a762fc-b1f8-4be3-aeed-7878461af8ae" />

Kombineerime INSERT ja DELETE triggerid
```sql
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
```
Trigerid meie tabelis
<img width="198" height="163" alt="{172A794F-B89F-4810-A91C-A6696DC837CE}" src="https://github.com/user-attachments/assets/dc3d24c4-4dc5-43bb-9213-72a7666b22c5" />

<img width="897" height="255" alt="{F4FC29DA-67D5-4FD4-99A5-506461A1AB50}" src="https://github.com/user-attachments/assets/12a92bd1-b074-47d1-aa8b-56b176d44320" />


UPDATE triger
```sql
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
```
<img width="926" height="354" alt="{490E096A-F1F8-4344-B9CF-7EBCB1D96A0E}" src="https://github.com/user-attachments/assets/80aa0287-b779-411d-82bb-7188205de623" />
