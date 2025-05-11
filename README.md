# E-Commerce Django Project

A full-featured e-commerce platform built with Django, featuring user authentication, product management, shopping cart functionality, and more.

## Features

- 🔐 User Authentication & Authorization
- 🛍️ Product Catalog with Categories
- 🛒 Shopping Cart Functionality
- 👤 User Account Management
- 📧 Email Notifications
- 💳 Payment Integration Ready
- 📱 Responsive Design
- 🔍 Product Search
- 📦 Order Management

## Tech Stack

- Python 3.x
- Django 3.1
- SQLite (Development)
- HTML/CSS/JavaScript
- Bootstrap

## Prerequisites

- Python 3.x
- pip (Python package manager)
- Virtual Environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/e-commerce-django.git
cd e-commerce-django
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Project Structure

- `accounts/` - User authentication and account management
- `category/` - Product category management
- `store/` - Product management and store functionality
- `carts/` - Shopping cart functionality
- `templates/` - HTML templates
- `media/` - User-uploaded files
- `static/` - Static files (CSS, JS, images)

## Configuration

1. Update the email settings in `greatkart/settings.py` with your SMTP credentials
2. Set up your database configuration in `greatkart/settings.py`
3. Update `SECRET_KEY` and `DEBUG` settings for production

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

