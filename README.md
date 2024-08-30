# API Documentation for E-commerce Project

## Overview
This document provides a detailed overview of all API endpoints available in the E-commerce project.

## Table of Contents
1. [Products API](#products-api)
2. [Orders API](#orders-api)
3. [Reports API](#reports-api)

---

## Products API

### 1. Get List of Products

- **Endpoint:** `/api/products/`
- **Method:** `GET`
- **Description:** Returns a list of products with optional filters by category and subcategory. Only products with stock greater than 0 are included.
- **Query Parameters:**
  - `category` (string): Filter by category
  - `subcategory` (string): Filter by subcategory
- **Responses:**
  - `200 OK` - List of products
  - `400 Bad Request` - Invalid query parameters

### 2. Create a New Product

- **Endpoint:** `/api/products/`
- **Method:** `POST`
- **Description:** Adds a new product.
- **Request Body:**
  ```json
  {
    "name": "string",
    "description": "string",
    "price": "float",
    "stock": "int",
    "category": "string",
    "subcategory": "string",
    "discount": "float"
  }

- **Responses:**
  - `200 OK` -  Product created successfully
  - `400 Bad Request` - Validation error
  

### 3. Update Product Price

- **Endpoint:** `/api/products/{id}/update_price/`
- **Method:** `POST`
- **Description:** Updates the price of a product by its ID.
- **Request Body:**
  ```json
  {
  "price": "float"
  }

- **Responses:**
  - `200 OK` -  Price updated successfully
  - `400 Bad Request` - Invalid data
  - `404 Not Found` - Product not found

### 4. Start Promotion on Product

- **Endpoint:** `/api/products/{id}/start_promotion/`
- **Method:** `POST`
- **Description:** Applies a discount to a product by its ID.
- **Request Body:**
  ```json
  {
  "discount": "float"
  }

- **Responses:**
  - `200 OK` -  Discount applied successfully
  - `400 Bad Request` - Invalid data
  - `404 Not Found` - Product not found

### 5. Delete a Product

- **Endpoint:** `/api/products/{id}/`
- **Method:** `DELETE`
- **Description:** Delete a product by its ID

- **Responses:**
  - `204 No Content` - Product deleted successfully
  - `404 Not Found` - Product not found


## Orders API

### 1. Get List of Orders

- **Endpoint:** `/api/orders/`
- **Method:** `GET`
- **Description:** Returns a list of all orders.
- **Responses:**
  - `200 OK` - List of orders

### 2. Retrieve an Order

- **Endpoint:** `/api/orders/{id}/`
- **Method:** `GET`
- **Description:** Retrieves details of a specific order by its ID.
- **Responses:**
  - `200 OK` - Order details
  - `404 Not Found` - Order not found

### 3. Reserve a Product

- **Endpoint:** `/orders/reserve/`
- **Method:** `POST`
- **Description:** Reserves a product for a customer.
- - **Request Body:**
  ```json
  {
  "product_id": "int",
  "quantity": "int"
  }
- **Responses:**
  - `201 Created` - Product reserved successfully
  - `400 Bad Request` - Insufficient stock or other errors

### 4. Cancel a Reservation

- **Endpoint:** `/api/orders/{id}/cancel/`
- **Method:** `POST`
- **Description:** Cancels a product reservation by order ID.
- **Responses:**
  - `200 OK` - Reservation cancelled successfully
  - `400 Bad Request` - Invalid operation or order status

### 5. Complete a Sale

- **Endpoint:** `/api/orders/{id}/complete/`
- **Method:** `POST`
- **Description:** Marks an order as sold.
- **Responses:**
  - `200 OK` - Order completed successfully
  - `400 Bad Request` - Invalid operation or order status  

## Reports API

### 1. Get Sold Products Report

- **Endpoint:** `/api/reports/sold_products/`
- **Method:** `GET`
- **Description:** Returns a report of sold products with optional filters.
- **Query Parameters:**
  - `category` (string): Filter by category
  - `subcategory` (string): Filter by subcategory
- **Responses:**
  - `200 OK` - Report of sold products
  - `400 Bad Request` -  Invalid query parameters


## How to Use

- **Base URL:** All endpoints are prefixed with `/api/`.
- **Pagination:** For list endpoints, pagination is applied with the default Django REST framework settings. Use `?page=<number>` in query parameters to navigate pages.
- **Swagger Documentation:** Access the interactive API documentation at `/swagger/` to try out endpoints and view detailed specifications.


