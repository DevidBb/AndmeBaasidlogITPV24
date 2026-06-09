create database keys
use keys

create table kasutaja(
kasutaja_id int primary key identity(1,1),
kasutaja_nimi varchar(30),
vanus int)

insert into kasutaja
values('Ruslan', 18), ('Nikita', 16), ('Artem', 17)

select * from kasutaja

create table toit(
id int primary key identity(1,1),
toidu_nimi varchar(30),
kasutaja_id int,
foreign key (kasutaja_id) references kasutaja(kasutaja_id))

insert into toit
values('Tomat', 1), ('Kurk', 2)

select * from toit

insert into toit
values('Vesi', 4)

create table sonaraamat(
id int primary key identity (1,1),
sona varchar(30) unique)

insert into sonaraamat
values('Toit'), ('Inimene')

select * from sonaraamat

insert into sonaraamat
values('Toit')

create table loomad(
looma_id int primary key,
looma_nimi varchar(30))

insert into loomad
values(1, 'Koer'), (2, 'Kass')

select * from loomad

insert into loomad
values (2, 'Kilpkonn')

create table tellimus(
tellimuse_id int,
toote_id int,
kogus int,
primary key(tellimuse_id, toote_id))

insert into tellimus
values(1, 1, 2), (1, 2, 1), (2, 1, 3);

select * from tellimus

insert into tellimus
values(1, 1, 5)

create table opilane_kursus(
opilane_id int,
kursus_id int,
primary key(opilane_id, kursus_id))

insert into opilane_kursus(opilane_id, kursus_id)
values(1, 1), (2, 2)

select * from opilane_kursus

create table hinne(
hinne_id int primary key identity(1,1),
opilane_id int,
kursus_id int,
hinne int,
foreign key(opilane_id, kursus_id) references opilane_kursus(opilane_id, kursus_id))

insert into hinne 
values (1, 1, 5), (2, 2, 4)

select * from hinne

insert into hinne 
values (1, 2, 5)

create table inimene(
id int primary key identity(1,1),
nimi varchar(30),
email varchar(50))

insert into inimene
values('Ruslan', 'ruslan@gmail.com'), ('Nikita', 'nikita@gmail.com'), ('Maksim', 'maksim@gmail.com')

select * from inimene

select * from inimene where id=1
select * from inimene where nimi='Nikita'
select * from inimene where id=3 and email='maksim@gmail.com'

create table telefon(
tel_id int primary key identity(1,1),
mudel varchar(50),
kogus int,
pood varchar(30))

insert into telefon
values('iPhone 14', 10, 'T1'), ('iPhone 14', 10, 'Kristiine Keskus'), ('Samsung S23', 5, 'T1'), ('Nokia 3310', 2, 'Ulemiste');

select * from telefon

--tel_id on candidate key, sest ainult tel_id on iga rea ​​jaoks unikaalne.

drop table telefon

create table telefon(
tel_id int primary key identity(1,1), -- see on primary key
mudel varchar(50) unique, -- see on alternate key 1
kogus int unique, -- see on alternate key 2
pood varchar(30) unique) -- see on alternate key 3

insert into telefon
values('iPhone 14', 10, 'T1'), ('iPhone 15', 11, 'Kristiine Keskus'), ('Samsung S23', 5, 'Mustikas'), ('Nokia 3310', 2, 'Ulemiste');

select * from telefon
