create database EZ_AGROw;
use EZ_AGROw;

create table FARMER
(
    farmer_id int primary key,
    full_name varchar(50) not null,
    date_of_birth date not null,
    gender enum('Male', 'Female', 'Other') not null,
    phone_number varchar(10) not null,
    email varchar(255)  ,
	farm_type varchar(100) not null,
    password varchar(200) not null
);

select * from farmer;
create table LABOUR
(
	labour_name varchar(50) unique not null,
    labour_id int primary key,
    full_name varchar(50) not null,
    date_of_birth date not null,
    gender enum('Male', 'Female', 'Other') not null,
    age int(2),
    phone_number varchar(10) not null,
    email varchar(20) unique not null,
    address varchar(200) not null,
    city varchar(25) not null,
    state varchar(20) not null,
    postal_code varchar(6) NOT NULL,
    password varchar(20) not null
);
alter table labour drop column full_name;

select * from Labour;
insert into LABOUR values (
	'Lucifer', 1001, 'Gagan', '2005-05-29', 'Male', 18, '8971547085', 'itzmegagan@gmail.com','noneofurbuisness','Mangalore', 'Karnataka', '574240', '12345'
);

create table CATEGORY (
	category_id int primary key,
    category_name varchar(50)
);

create table BUYER(
	buyer_id int primary key,
    buyer_name varchar(30)
);
