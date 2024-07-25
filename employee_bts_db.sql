create table employee
(
empLoginId varchar(10) primary key,
empPassword varchar(20),
empType varchar(20) ,
empName varchar(45),
empPhone varchar(10),
empEmail varchar(45),
empStatus varchar(20) DEFAULT 'ACTIVE'
);