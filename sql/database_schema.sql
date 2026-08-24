-- E-Commerce Analytics Database Schema
CREATE TABLE customers (
    CustomerID VARCHAR(10) PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Gender VARCHAR(20),
    Age INT,
    City VARCHAR(50),
    Province VARCHAR(50),
    SignupDate DATE
);

CREATE TABLE products (
    ProductID VARCHAR(10) PRIMARY KEY,
    ProductName VARCHAR(100),
    Category VARCHAR(50),
    UnitCost DECIMAL(12,2),
    UnitPrice DECIMAL(12,2)
);

CREATE TABLE orders (
    OrderID VARCHAR(10) PRIMARY KEY,
    CustomerID VARCHAR(10),
    ProductID VARCHAR(10),
    OrderDate DATE,
    Quantity INT,
    Discount DECIMAL(5,2),
    PaymentMethod VARCHAR(30),
    FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID),
    FOREIGN KEY (ProductID) REFERENCES products(ProductID)
);
