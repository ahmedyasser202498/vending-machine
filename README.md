# 🥤 Vending Machine 

## Introduction

A RESTful APIs that simulates a vending machine, allowing buyers to deposit coins and purchase products, and sellers to manage product inventory.

Built with **Django + Django REST Framework**, served in production with **Gunicorn and Nginx in Docker**.


## Features

### 🖥️ Backend (Django + DRF)

- **Models**:
  - `User` (with roles: buyer, seller)
  - `Product`

- **API Endpoints**:
    - `POST /api/token/`: Login with username & password (JWT).
    - `POST /core/users/`: Sign up (no authentication required).
    - `GET /core/users/`: Get all users (authentication required).
    - `PATCH /core/users/{id}/`: Update user info (authentication required).
    - `DELETE /core/users/{id}/`: Delete user (authentication required).
    - `POST /core/users/deposit/`: Buyer deposits coins (only accepts 5, 10, 20, 50, 100).
    - `POST /core/users/reset/`: Buyer resets their deposit to zero.
    - `POST /core/users/buy/`: Buyer purchases product with deposited money.
    - `GET /core/products/`: Public product listing.
    - `POST /core/products/`: Seller creates a product.
    - `PUT /core/products/{id}/`: Seller updates their own product.
    - `DELETE /core/products/{id}/`: Seller deletes their own product.

- **Validation**:
    - Product cost must be divisible by 5.
    - Only valid coin values can be deposited (5, 10, 20, 50, 100).
    - Buyer cannot buy with insufficient deposit.
    - Buyer cannot buy more than available product stock.
    - Only sellers can manage their own products.


---


## 🔐 Security

- API permissions ensure users cannot access other users' data.
- JWT token used for authentiaction.

---


## Setup Environment and Using Docker Compose

To set up the environment and run the application using Docker Compose, follow these steps:

### Prerequisites
Ensure that you have [Docker](https://www.docker.com/products/docker-desktop) and [Docker Compose](https://docs.docker.com/compose/) installed on your machine.

### Steps to Set Up

1. **Clone the Repository (OPTIONAL)**  
   Clone this repository to your local machine:
   ```bash
   git clone https://github.com/ahmedyasser202498/vending-machine.git
   cd backend
	```
2. **Build the Docker Containers**  
   To build the Docker images defined in the docker-compose.yml file, run:
   ```bash
   docker-compose build
   ```

3. **Start the Application with Docker Compose**  
   After building the images, start the services (database, backend and nginx) with:
   ```bash
   docker-compose up
   ```
   
   This will:
	- Set up a PostgreSQL database service (db).
	- Set up a backend service (backend).
    - Set up a nginx.

4. **Stopping the Services**  
   To stop the services, use:
   ```bash
   docker-compose down
   
# 📦 Models Overview

The application includes Django models that define the essential entities for a **Vending Machine** system. These models handle core validation and business logic, such as product pricing, deposit management, and role-based permissions.


## 👤 User Model

The `User` model extends Django’s built-in `AbstractUser` to support two distinct roles: **seller** and **buyer**. It also includes a `deposit` field used in transaction flows.

### Fields:
- `role`: A choice field that determines if a user is a `seller` or `buyer`.
- `deposit`: An integer representing the user's current deposit (default is `0`).
- Inherits all fields from `AbstractUser` (e.g., `username`, `email`, etc.).

### Notes:
- Valid coins for deposit are loaded from the environment variable `VALID_COINS`.
- Intended for use in enforcing role-specific permissions and managing user balance in the vending process.



## 🛒 Product Model

The `Product` model represents items that sellers can offer to buyers.

### Fields:
- `seller`: A foreign key to the `User` model (must have role `seller`).
- `product_name`: The name of the product.
- `cost`: The cost of the product (must be divisible by `5`).
- `amount_available`: Number of product units currently in stock.

### Validation:
- Overrides the `save()` method to ensure:
  - `cost` is divisible by `5`. If not, a `ValidationError` is raised.


## 🔐 Validation Summary

- Only coins specified in the `VALID_COINS` environment variable can be deposited.
- Product `cost` must be divisible by `5`.
- Sellers can only manage their own products.
- Buyer deposit and product stock must be sufficient for purchases.

---
## 🔧 Environment Variables

- `VALID_COINS`: A string representation of a list of accepted coin values (e.g., `"[5, 10, 20, 50, 100]"`).


# 🔗 Relationships Between Models

- **User ↔ Product**:  
  A `User` with the role of **seller** can have multiple `Product` instances.  
  - One seller ➝ many products  
  - Enforced through the `seller` ForeignKey in the `Product` model

- **Product Attributes and Logic**:
  - Each `Product` has a `cost` (must be divisible by 5)
  - Each product tracks `amount_available` to manage inventory
  - Only the owning seller can manage (create/update/delete) their products

- **Buyer Role & Transactions** (expected behavior for buyers):
  - Buyers interact with products via purchase operations
  - The buyer’s `deposit` is used to make purchases
  - Deposit must include valid coin denominations (loaded from `VALID_COINS` environment variable)

- **Roles and Permissions**:
  - `User.role` determines whether a user is a **seller** or a **buyer**
  - System behavior (e.g., access control) is enforced based on this role

---


# 📬 API Usage & Postman Test Bodies

This section provides example request bodies for testing the key API endpoints using Postman.

---

## 🔐 Authentication & Roles

### 🔑 Token-Based Authentication (JWT)

This project uses **JWT (JSON Web Tokens)** for authentication, powered by `djangorestframework-simplejwt`.

### 🔓 Obtain Access & Refresh Tokens

`POST /api/token/`

```json
{
  "username": "buyer1",
  "password": "StrongPassword123!"
}
```
- ✅ Successful Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJh...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJh..."
}
```
`POST /api/token/refresh/`

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJh..."
}
```
- ✅ Successful Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJh..."
}
```

## 🚦 Role-Based Access Control

- Buyers (role = buyer):
  - Can deposit, buy, and reset their deposit.
  - Cannot create or manage products.
- Sellers (role = seller):
  - Can create, update, and delete their own products.
  - Cannot use buyer-only actions (e.g. deposit, buy).

### ***All protected endpoints require the Authorization header:***
```http
Authorization: Bearer <your-access-token>
```

## 👤 User Endpoints

### 🔐 Register a New User

`POST /core/users/`

```json
{
  "username": "buyer1",
  "email": "buyer1@example.com",
  "password": "StrongPassword123!",
  "role": "buyer"
}
{
  "username": "seller1",
  "email": "seller1@example.com",
  "password": "StrongPassword123!",
  "role": "seller"
}
```

### 💰 Deposit Coins (Buyer Only)

`POST /core/users/deposit/`
- ⚠️ Must be authenticated as a user with role buyer.
```json
{
  "amount": 50
}
```
- 📌 Note: Accepted values: 5, 10, 20, 50, 100
- ❌ Invalid coin values will raise a validation error.
- ✅ Successful Response:

```json
{
  "deposit": 100
}
```
### 🔄 Reset Deposit (Buyer Only)

`POST /core/users/reset/`
- ⚠️ Must be authenticated as a user with role buyer.
- 📌 This resets the user's deposit to 0.
- ✅ Successful Response:

```json
{
  "deposit": 0
}
```

### 🛍️ Buy Product (Buyer Only)

`POST /core/users/buy/`
- ⚠️ Must be authenticated as a user with role buyer.
```json
{
  "product_id": 3,
  "quantity": 2
}
```
- ✅ Successful Response:

```json
{
  "total_spent": 40,
  "product": "Soda",
  "change": {100:0,
              50:0,
              20:1,
              10:1,
              5:0
            }  
}
```
- ❌ Errors:
  - Not enough deposit
  - Insufficient product stock
  - Invalid product ID


## 📦 Product Endpoints

### ➕ Create Product (Seller Only)

`POST /core/products/`
- ⚠️ Must be authenticated as a user with role seller.
```json
{
  "product_name": "Chips",
  "cost": 15,
  "amount_available": 20
}
```
- ✅ Successful Response:

```json
{
  "id": 7,
  "product_name": "Chips",
  "cost": 15,
  "amount_available": 20,
  "seller": 1
}
```
- ❌ Validation Errors:
  - `cost` must be divisible by 5

### 📄 List All Products

`GET /core/products/`
- ✅ Successful Response:
```json
[
  {
    "id": 1,
    "product_name": "Water",
    "cost": 10,
    "amount_available": 5,
    "seller": 2
  },
]
```

### ✏️ Update Product (Seller Only, Owner Only)

`PATCH /core/products/1/`
- ✅ changes:
  - product_name
  - amount_available
```json
{
  "product_name": "Water Bottle",
  "cost": 10,
  "amount_available": 10
}
```

### ❌ Delete Product (Seller Only, Owner Only)

`DELETE /core/products/1/`
- Only the seller who created the product can delete it.



# 🧪 Running Tests

This project uses **pytest** and **pytest-django** for testing the API endpoints and core logic.

---

## ✅ What’s Tested?

The test suite covers the following key use cases:

### 💰 Deposit Functionality
- ✅ Valid coin deposit (`amount = 50`)
- ❌ Invalid coin deposit (`amount = 3`) → must be divisible by 5

### 🔁 Deposit Reset
- Resets user deposit to `0`

### 🛒 Purchase Flow
- ✅ Successful product purchase (with sufficient deposit and stock)
- ❌ Purchase with insufficient deposit
- ❌ Purchase of non-existent product
- ❌ Purchase with insufficient stock

### 🏷️ Product Management
- ✅ Product creation by seller
- ❌ Product creation by buyer (unauthorized)

## ⚙️ How to Run the Tests
- Prerequisites:
  - Docker services should be up.

```bash
sudo docker-compose exec web pytest
```
---


# ⚙️ Environment & Deployment Info

This project is fully containerized using **Docker** and follows production best practices, including the use of **NGINX** as a reverse proxy and **Gunicorn** as the WSGI server.


## 🌍 Environment Variables

Some key settings are configured via environment variables to allow flexibility across environments (e.g. local, staging, production).

### 📌 Important Variables

| Variable       | Description                            | Example                     |
|----------------|----------------------------------------|-----------------------------|
| `VALID_COINS`  | List of acceptable coin denominations  | `[5, 10, 20, 50, 100]`      |
| `POSTGRES_DB`  | Name of the PostgreSQL database         | `vending_db`               |
| `POSTGRES_USER`| Database user                          | `vending_user`             |
| `POSTGRES_PASSWORD`| User password                    | `vending_pass`             |

Environment values like `VALID_COINS` are accessed at runtime in Django using:

```python
import os, ast
valid_coins = ast.literal_eval(os.environ.get('VALID_COINS'))
```

## 🐳 Docker & Docker Compose
The project uses docker-compose to orchestrate services including:

- Django web server (via Gunicorn)
- PostgreSQL database
- NGINX reverse proxy (for production)

### 🔧 docker-compose.yml Overview
`web` **Service**
- Runs the Django application.
- Uses `gunicorn` for WSGI serving in production.
- Performs migrations automatically on startup.
- Mounted with the local source code for development flexibility.

`db` **Service**
- Uses **PostgreSQL 15** as the database engine.
- Configured with persistent volume and exposed on port `5434`.

`nginx` **Service**
- Acts as a **reverse proxy** in front of `Gunicorn`.
- Uses a custom `nginx.conf` file for routing requests to the Django `web` service.
- Exposes the app to port `80` (HTTP).

---

# 🪵 Logging & Exception Handling

Robust logging and structured exception handling are integrated into the APIS to help with debugging, monitoring, and operational insights.

---

## 📋 Logging Configuration

Logging is configured using Django's `LOGGING` settings and outputs to the console, ideal for Docker and containerized environments.

### 🔧 Sample Logging Settings (in `settings.py`):

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',  # Use DEBUG for local dev
    },
}
```

## 🧠 How Logging Is Used
A module-level logger is initialized using:
```python
import logging
logger = logging.getLogger(__name__)
```
Logging is implemented across the service layer and view layer to track:

- User actions (e.g. deposits, purchases)
- System events (e.g. invalid input, errors)
- Warnings and failures (e.g. insufficient deposit, invalid coins)

### 🔍 Example Logging in Services (CoreService):
```python
logger.info(f"{user.username} attempts to deposit {amount}")
logger.warning(f"Invalid deposit amount: {amount} by user {user.username}")
logger.error(f"Product {product_id} not found")
```
These logs help trace user behavior, catch bugs, and simplify post-mortem analysis.

## 🚨 Exception Handling


| Layer       | Type                            | Result                     |
|----------------|----------------------------------------|-----------------------------|
| 🔁 View Layer	  | `try-except` around service calls  | Captures unexpected runtime errors      |
| 🔐 Service Layer	  | Explicit Django exceptions	         | Raises standard `DRF` errors (`NotFound`, `PermissionDenied`, etc.)               |

### ✅ Built-In Exceptions Used

- `ValueError`: For simple validation like unsupported coin values.
- `NotFound`: Raised when a product doesn't exist.
- `PermissionDenied`: Raised for business rules like insufficient deposit.
- `ValidationError`: Raised for quantity/stock issues.

#### 🔒 Views Example:
```python
try:
    total_cost, coin_change, product_name = CoreService().handle_buy(...)
except Exception as e:
    logger.error(f"Buy failed: {str(e)}")
    return Response({"error": str(e)}, status=400)
```

#### 🧰 Services Example:
```python
if amount not in self.valid_coins:
    logger.warning("Invalid coin deposit")
    raise ValueError("Invalid coin")
```

---



