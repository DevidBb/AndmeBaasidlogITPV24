```sql
create database work1
use work1

--loo tabeleid ja väärtusi
create table category (
category_id int primary key identity(1,1),
category_name varchar(100) not null unique)

insert into category
values('toit'), ('jook')

select * from category

create table product(
product_id int primary key identity(1,1),
product_name varchar(50) not null,
category_id int not null,
foreign key (category_id) references category(category_id),
price money not null check (price > 0))

insert into product
values('pitsa', 1, 2.5), ('burger', 1, 3), ('sprite', 2, 1.5), ('mahl', 2, 2)

select * from product

create table sale(
sale_id int primary key identity(1,1),
product_id int not null
foreign key (product_id) references product(product_id),
customer_id int not null
foreign key (customer_id) references customer(customer_id),
count int not null check (count > 0),
date_of_sale date not null DEFAULT GETDATE())

insert into sale
values(1, 1, 2, '2026-05-27'), (2, 1, 1, '2026-05-27')

insert into sale(product_id, customer_id, count)
values(3, 2, 4)

select * from sale

--lisa veerg "units" tabelisse "sale"
alter table sale add units varchar(10)

select * from sale

--veeru "units" andmetüübi muutmine
alter table sale alter column units int

--lisamine tabel customer
create table customer(
customer_id int primary key identity(1,1),
customer_name varchar(50),
contact varchar(50))

insert into customer
values('Dima', 'dima@gmail.com'), ('Nastja', 'nastja@gmail.com')

select * from customer
```
