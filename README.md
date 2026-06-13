SMART CAMPUS ERP & E-COMMERCE SYSTEM
DATABASE SETUP

---

1. CREATE DATABASE

---

CREATE DATABASE studentdb;

USE studentdb;

---

2. USERS TABLE

---

CREATE TABLE users (
user_id INT AUTO_INCREMENT PRIMARY KEY,
username VARCHAR(50),
password VARCHAR(50)
);

---

3. STUDENT DETAILS TABLE

---

CREATE TABLE studentdetails (
student_id INT AUTO_INCREMENT PRIMARY KEY,
student_name VARCHAR(100),
student_age INT,
student_college VARCHAR(100),
student_phone VARCHAR(10),
student_branch VARCHAR(50),
password VARCHAR(50)
);

---

4. PRODUCTS TABLE

---

CREATE TABLE products (
product_id INT AUTO_INCREMENT PRIMARY KEY,
product_name VARCHAR(100),
product_price DECIMAL(10,2),
product_category VARCHAR(50),
product_quantity INT
);

---

5. CART TABLE

---

CREATE TABLE cart (
cart_id INT AUTO_INCREMENT PRIMARY KEY,
product_id INT,
product_name VARCHAR(100),
quantity INT,
price DECIMAL(10,2)
);

---

6. ORDERS TABLE

---

CREATE TABLE orders (
order_id INT AUTO_INCREMENT PRIMARY KEY,
product_id INT,
product_name VARCHAR(100),
quantity INT,
total_amount DECIMAL(10,2),
order_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

---

7. CUSTOMERS TABLE (FUTURE)

---

CREATE TABLE customers (
customer_id INT AUTO_INCREMENT PRIMARY KEY,
customer_name VARCHAR(100),
customer_phone VARCHAR(10),
customer_email VARCHAR(100)
);

---

8. PAYMENTS TABLE (FUTURE)

---

CREATE TABLE payments (
payment_id INT AUTO_INCREMENT PRIMARY KEY,
order_id INT,
amount DECIMAL(10,2),
payment_method VARCHAR(50),
payment_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

---

9. FEEDBACK TABLE (OPTIONAL)

---

CREATE TABLE feedback (
feedback_id INT AUTO_INCREMENT PRIMARY KEY,
customer_name VARCHAR(100),
message TEXT
);

---

10. CONTACT MESSAGES TABLE (OPTIONAL)

---

CREATE TABLE contact_messages (
message_id INT AUTO_INCREMENT PRIMARY KEY,
sender_name VARCHAR(100),
sender_email VARCHAR(100),
message TEXT
);

---

## CHECK TABLES

SHOW TABLES;

---

## VIEW TABLE STRUCTURE

DESC users;
DESC studentdetails;
DESC products;
DESC cart;
DESC orders;
