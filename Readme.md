# Inventory Management System

## Overview
This Inventory Management System is built using Django and Django REST Framework, allowing users to efficiently manage inventory items through a comprehensive API. It supports creating, retrieving, updating, and deleting items.

## Features
- **User Registration and Authentication**
- **CRUD Operations** for inventory items
- **Token-based Authentication**
- **Comprehensive API Endpoints** for easy integration

## Technologies Used
- **Django**: A high-level Python web framework for web application development.
- **Django REST Framework**: A powerful toolkit for building Web APIs.
- **SQLite** (or PostgreSQL/MySQL depending on your configuration): A lightweight database engine.
- **Redis**: An in-memory data structure store, used for caching and messaging.
- **Python 3.x**: The programming language used to develop the application.

## Installation

### Prerequisites
- **Python 3.x**
- **pip** (Python package installer)
- **Redis**: Ensure Redis is installed on your system. You can find installation instructions on the [Redis website](https://redis.io/download).

### Steps
1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/inventory_management.git
   cd inventory_management


2. **Create a virtual environment:**

    python -m venv venv


3. **Activate the virtual environment:**

    On Windows:


    venv\Scripts\activate
    On macOS/Linux:


    source venv/bin/activate
    Install dependencies: Create a requirements.txt file with the following contents:



    Django>=3.0,<4.0
    djangorestframework>=3.12,<4.0
    djangorestframework-authtoken>=1.0
    redis>=4.0


4. **Then run:**



    pip install -r requirements.txt
    Run database migrations:



    python manage.py migrate
    Create a superuser (optional):



    python manage.py createsuperuser
    Run the development server:



    python manage.py runserver
    Access the API: Navigate to http://127.0.0.1:8000/inventory/ in your web browser or use tools like Postman to interact with the API.

**API Endpoints**

    Method	Endpoint	        Description
    POST	/inventory/register/	    Register a new user
    POST	/inventory/login/	        Log in a user and receive a token
    GET	    /inventory/items/	        Retrieve all inventory items
    POST	/inventory/items/	        Create a new inventory item
    GET	    /inventory/items/{id}/	Retrieve a specific inventory item
    PUT	    /inventory/items/{id}/	Update a specific inventory item
    DELETE	/inventory/items/{id}/	Delete a specific inventory item



**Authentication**

    To authenticate, use the /inventory/login/ endpoint to obtain an access token. Include the token in the Authorization header as follows:

    Authorization: Bearer <your_access_token>


**Running Tests**


    To run the test suite, use the following command:

    python manage.py test inventory.tests




    






