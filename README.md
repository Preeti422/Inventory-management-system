# Inventory Order Management System

A web-based Inventory Order Management System developed using Flask, MySQL, HTML and CSS.

## Features

- Admin Login and Logout
- Dashboard with summary statistics
- Customer Management
- Product Management
- Order Management
- Order Item Management
- Add, Update and Delete Customers
- Add, Update and Delete Products
- Update and Delete Orders
- Update and Delete Order Items
- Search Customer
- Search Product
- Low Stock Report
- Sales Report
- Automatic Stock Management
- MySQL Database Integration
- Session-based Login Protection

## Technologies Used

- Python
- Flask
- MySQL
- HTML5
- CSS3

## Database

The application uses MySQL to store and manage:

- Users
- Customers
- Categories
- Products
- Orders
- Order Items

## Project Workflow

Login → Dashboard → Customers → Products → Orders → Order Items → Sales Report

## Project Structure

```text
Inventory_Order_Management/
│
├── app.py
├── customer.py
├── database.py
├── README.md
├── requirements.txt
├── .gitignore
│
└── templates/
    ├── base.html
    ├── login.html
    ├── dashboard.html
    ├── customer.html
    ├── product.html
    ├── order.html
    ├── order_item.html
    ├── search_customer.html
    ├── search_product.html
    ├── low_stock.html
    └── sales_report.html
```

## How to Run

### 1. Install Python

Make sure Python is installed on your system.

### 2. Install Required Packages

```bash
pip install -r requirements.txt
```

### 3. Start MySQL

Make sure MySQL Server is running.

### 4. Create the Database

Create the required database and tables in MySQL Workbench.

### 5. Configure Database Connection

Update the MySQL connection details in `app.py` according to your local MySQL setup.

### 6. Run the Application

```bash
python app.py
```

### 7. Open the Application

Open the following URL in your browser:

```text
http://127.0.0.1:5000/login
```

## Authentication

The application provides an admin login system.

Users must log in before accessing protected pages such as:

- Dashboard
- Customers
- Products
- Orders
- Order Items
- Search
- Low Stock
- Sales Report

## Purpose

This project was created to practice:

- Flask web development
- MySQL database integration
- CRUD operations
- SQL queries
- Session-based authentication
- Inventory management
- Order processing
- Stock management
- Report generation