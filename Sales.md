# andmebaadsales
```sql
--1.categories
CREATE TABLE categories(
category_id int PRIMARY KEY identity(1,1),
category_name varchar(25) UNIQUE);

INSERT INTO categories(category_name)
VALUES ('Ruuter');

SELECT * FROM categories;
```
<img width="205" height="81" alt="{46F6F411-77AC-4C26-8352-8C770060721A}" src="https://github.com/user-attachments/assets/3b4f98c9-795e-45c6-acdf-2916910ff70b" />

```sql
--2.brands
CREATE TABLE brands(
brand_id int PRIMARY KEY identity(1,1),
brand_name varchar(15) UNIQUE);

INSERT INTO brands(brand_name)
VALUES ('Samsung');

SELECT * FROM brands;
```
<img width="169" height="81" alt="{1015FEE3-6CFE-48CF-AABD-E36699D4AD06}" src="https://github.com/user-attachments/assets/5118f421-4320-4d24-baa1-48026d278ce6" />

```sql
--3.products
Create TABLE products(
product_id int PRIMARY KEY identity(1,1),
product_name varchar(50) not null,
brand_id int,
FOREIGN KEY (brand_id) references brands(brand_id),
category_id int,
FOREIGN KEY (category_id) references categories(category_id),
model_year int,
list_ürice money);

INSERT INTO products
VALUES ('nutitelefon X10',1, 1, 2025, 500);

select * from products;
```
<img width="445" height="78" alt="{605CA891-E16B-4F6D-9E7E-0C411928A369}" src="https://github.com/user-attachments/assets/b6e4358a-a723-4a7c-96bd-34ef98ffae2a" />

```sql
--4.stores
CREATE TABLE stores(
store_id int PRIMARY KEY identity(1,1),
store_name varchar(20) not null,
phone varchar(13),
email varchar(20),
street varchar(21),
city varchar(15),
state varchar(10),
zip_code char(5)
)

INSERT INTO stores
VALUES ('Ülemiste', 'iphone', 'ülemiste@gmail.com', 'ülemiste tee', 'Tallinn', 'Eesti', '10319');

SELECT * FROM stores;
```
<img width="591" height="77" alt="{D263F0E0-E82F-4130-9FA0-06AFD61F377A}" src="https://github.com/user-attachments/assets/c644baaa-2ef0-4d44-a5b8-b5a89dca96ff" />

```sql
--5.stocks
CREATE TABLE stocks(
store_id int,
product_id int,
PRIMARY KEY (store_id, product_id),
FOREIGN KEY (store_id) references stores(store_id),
FOREIGN KEY (product_id) references products(product_id),

quantity int 
)

INSERT INTO stocks
VALUES (1, 1, 4)

SELECT * FROM stocks;
```
<img width="209" height="77" alt="{6021AD9C-F9B4-4C0F-81B2-BC5A5538B503}" src="https://github.com/user-attachments/assets/0cdb3e71-7f3b-4afe-a9cb-61c06fdffcca" />

```sql
--6.customers
create table customers(
customer_id int primary key identity(1,1),
first_name varchar(15) not null,
last_name varchar(15) not null,
phone varchar(13),
email varchar(20),
street varchar(15),
city varchar(15) check (city='Tallinn' or city='Narva'),
zip_code char(5)
)

insert into customers
values('Andrei', 'Lomov', '52637294', 'andrei@gmail.com', 'Ülemiste tee', 'Tallinn','13912');

select * from customers
```
<img width="610" height="76" alt="{C3031A26-6DC6-432A-9EF9-D8C96B12CF92}" src="https://github.com/user-attachments/assets/dea2d49a-267e-4de5-ada8-59ced60094db" />

```sql
--7.staff
create table staff(
staff_id int primary key identity(1,1),
first_name varchar(15) not null,
last_name varchar(15) not null,
email varchar(20),
phone varchar(13),
active bit,
store_id int,
foreign key (store_id) references stores(store_id),
manager bit
);

insert into staff
values('Irina', 'Rahva', 'irina@gmail.com', '52635494', 1, 1, 1);

select * from staff;
```
<img width="544" height="74" alt="{277E9367-58E3-4372-AB92-BC8387CEA518}" src="https://github.com/user-attachments/assets/1f7416f2-9ed2-4d04-9ff7-a63080271ada" />

```sql
--8. orders
create table orders(
order_id int PRIMARY KEY identity (1,1),
customer_id int,
order_status varchar(15) check(order_status='complete' or order_status='incomplete'),
order_date  Date,
required_date Date,
shipped_date Date,
store_id int,
staff_id int,
foreign key (customer_id) references customers(customer_id),
foreign key (store_id) references stores(store_id),
foreign key (staff_id) references staff(staff_id)
);

insert into orders
values (1, 'incomplete', '2026-04-25', '2026-06-1', '2026-05-29', 1, 3);

select * from orders;
```
<img width="568" height="77" alt="{24A09D73-1DF5-4E31-BD7D-6CFFD8E1C02F}" src="https://github.com/user-attachments/assets/36f705b0-d38c-4c67-8c65-dcc66aec8e1a" />

```sql
--9.order_items
create table order_items(
order_id int,
item_id int,
primary key (order_id, item_id),
product_id int,
quantity int,
list_price money,
discount int,
foreign key (order_id) references orders(order_id),
foreign key (product_id) references products(product_id)
);

insert into order_items
values (2, 2, 1, 150, 1230, 90);

select * from order_items;
```
<img width="367" height="96" alt="{0810C442-3577-4F32-B679-54919ABCB7FE}" src="https://github.com/user-attachments/assets/f46b9411-ddb7-41f2-b2c3-c86ed50cab78" />


Database diagramm
<img width="1133" height="807" alt="{ADF83BBC-9FD2-4BFF-A3BA-62143DF7CE62}" src="https://github.com/user-attachments/assets/abaafb69-8dd8-4ccd-b309-f1a5f3368857" />
