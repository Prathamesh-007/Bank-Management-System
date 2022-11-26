CREATE DATABASE BANK;

USE BANK;

CREATE TABLE Customer(cust_id int PRIMARY KEY AUTO_INCREMENT, name varchar(50), DOB varchar(15));

ALTER TABLE Customer AUTO_INCREMENT = 100;

CREATE TABLE Branch(branch_id int PRIMARY KEY, location varchar(20), manager varchar(50), total_accounts int);

INSERT INTO Branch VALUES(411009, "Sinhagad Road", "Sinhagad Road Manager", 0),
(411038, "Kothrud", "Kothrud Manager", 0),
(411052, "Karve Nagar", "Karve Nagar Manager", 0);

CREATE TABLE Account(acc_no int PRIMARY KEY AUTO_INCREMENT, type varchar(20), cust_id int, branch_id int, balance int, password varchar(165), FOREIGN KEY(cust_id) REFERENCES Customer(cust_id), FOREIGN KEY(branch_id) REFERENCES Branch(branch_id));

ALTER TABLE Account AUTO_INCREMENT = 1000;

CREATE TABLE Statements(acc_no int, date varchar(15), time varchar(15), amount varchar(15), FOREIGN KEY(acc_no) REFERENCES Account(acc_no));