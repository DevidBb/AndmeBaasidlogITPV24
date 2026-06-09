# andmebaadsales
```sql
--1.categories
CREATE TABLE categories(
category_id int PRIMARY KEY identity(1,1),
category_name varchar(25) UNIQUE);

INSERT INTO categories(category_name)
VALUES ('ram');

SELECT * FROM categories;
```
<img width="234" height="111" alt="{BB16BBEE-7951-4723-A413-12C521C70F41}" src="https://github.com/user-attachments/assets/1a05834f-1caf-4796-857e-7970051a9173" />


```sql
--2.brands
CREATE TABLE brands(
brand_id int PRIMARY KEY identity(1,1),
brand_name varchar(15) UNIQUE);

INSERT INTO brands(brand_name)
VALUES ('msi');

SELECT * FROM brands;
```
<img width="211" height="120" alt="{47E79BCC-2028-4F15-B14F-EB5F2B2998E3}" src="https://github.com/user-attachments/assets/c3439287-032b-4319-9031-4e3c45262f23" />

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
VALUES (' rtx3060',1, 1, 2025, 500);

select * from products;
```
<img width="532" height="171" alt="{F87F51C8-2A62-4927-8FA0-BBCB1DC234D1}" src="https://github.com/user-attachments/assets/c106c68c-5269-4f28-9aee-cc386b209890" />

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
  VALUES ('klick', '5566666', 'klick@gmail.com', 'eldna tee', 'Tallinn', 'Eesti', '10319');

SELECT * FROM stores;
```
<img width="646" height="134" alt="{5B695077-4A6A-4210-9E0E-9C064D02154E}" src="https://github.com/user-attachments/assets/dac63d5a-8466-47cd-82c7-eda624ae3c44" />

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
<img width="230" height="139" alt="{0E32ADE2-13B0-4D4C-8080-412FAE3B7590}" src="https://github.com/user-attachments/assets/be495a84-8ed4-4df6-84d4-173f75bfbb65" />

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
values('Martin', 'Rumynskij', '56666666', 'martinrum@gmail.com', 'mustamae tee', 'Tallinn','16212');

select * from customers
```
<img width="703" height="169" alt="{32B3FE30-6AE5-4C01-BFFD-8E1105E5588E}" src="https://github.com/user-attachments/assets/69572cc7-00f4-4fcc-8f9a-aaa45c43f486" />

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
values('Maksim', 'Kislicin', 'Makismk@gmail.com', '52635494', 2, 2, 1);

select * from staff;
```
<img width="645" height="132" alt="{00FF8F7C-6E3E-4EEC-B509-A9996C607F4C}" src="https://github.com/user-attachments/assets/ef86e495-5ed2-4fb7-873d-3ffa5e03df7b" />

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
<img width="611" height="118" alt="{7C83FDDC-B7A6-4D58-901B-830C3EA1DEAA}" src="https://github.com/user-attachments/assets/c1f1cc1a-f26e-45af-854a-c1760e3dbb45" />

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
<img width="384" height="140" alt="{BD2FC493-6839-4599-81B3-B719E906F320}" src="https://github.com/user-attachments/assets/6c99e61f-8c6d-49aa-bbc5-73fce31525a8" />


Database diagramm
<img width="1133" height="807" alt="{ADF83BBC-9FD2-4BFF-A3BA-62143DF7CE62}" src="https://github.com/user-attachments/assets/abaafb69-8dd8-4ccd-b309-f1a5f3368857" />
