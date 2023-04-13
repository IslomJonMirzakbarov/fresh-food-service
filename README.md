# FreshFoods - Online Food Ordering System 🍲

FreshFoods is a Django project that provides an online food ordering system. The project is built using the Django REST framework, Djoser, and SQLite3 as the database. This project offers RESTful APIs to manage categories, menu items, user groups, cart items, and orders.

![Django](https://img.shields.io/badge/django-3.2.8-green.svg)

![Djoser](https://img.shields.io/badge/djoser-2.1.0-blue.svg)

![SQLite3](https://img.shields.io/badge/sqlite3-3.37.0-orange.svg)

<!-- ![MIT License](https://img.shields.io/badge/license-MIT-brightgreen.svg) -->

## Project Structure 📁

FreshFoods
│
└───FreshFoodsAPI
│ │ admin.py
│ │ apps.py
│ │ models.py
│ │ permissions.py
│ │ serializers.py
│ │ views.py
│ │ urls.py
│
└───db.sqlite3

### FreshFoodsAPI

This folder contains the main application files:

- `admin.py`: Registers the models with the Django admin site.
- `apps.py`: Configures the FreshFoodsAPI application.
- `models.py`: Defines the data models used in the application.
- `permissions.py`: Contains custom permission classes for user roles.
- `serializers.py`: Serializes and deserializes data models for use with the API.
- `views.py`: Defines the API views and the business logic.
- `urls.py`: Defines the URL patterns for the application.

## Installation 💻

1. Clone this repository:
   git clone https://github.com/yourusername/freshfoods.git

2. Create a virtual environment and activate it:
   python -m venv venv
   source venv/bin/activate

3. Install the required dependencies:
   pip install -r requirements.txt

4. Run the migrations to create the database:
   python manage.py migrate

5. Create a superuser for the Django admin site:
   python manage.py createsuperuser

6. Start the development server:
   python manage.py runserver

7. Visit the Django admin site at [http://localhost:8000/admin](http://localhost:8000/admin) to manage the application data.

## API Endpoints 🌐

The following API endpoints are available:

- Categories: `GET, POST /categories/`, `GET, PUT, PATCH, DELETE /categories/<int:pk>`
- Menu Items: `GET, POST /menu-items/`, `GET, PUT, PATCH, DELETE /menu-items/<int:pk>`
- Manager Group Management: `GET, POST /groups/manager/users/`, `GET, DELETE /groups/manager/users/<int:user_id>/`
- Delivery Crew Group Management: `GET, POST /groups/delivery-crew/users/`, `GET, DELETE /groups/delivery-crew/users/<int:user_id>/`
- Cart Management: `GET, POST /cart/menu-items/`, `DELETE /cart/menu-items/`
- Orders: `GET, POST /orders/`, `GET, PUT, PATCH, DELETE /orders/<int:pk>`

<!-- ## License 📄 -->

<!-- This project is licensed under the [MIT License](LICENSE). -->
