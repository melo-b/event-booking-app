# 🗓️ Event Booking App

A Django-based web application that allows users to create events and RSVP to them. Includes search and filtering, capacity limits, admin tools, and RSVP confirmation logic.

---

## 🚀 Features

- ✅ User authentication (login, logout)
- ✅ Create, edit, delete events (CRUD)
- ✅ RSVP to events (many-to-many relationships)
- ✅ Prevent overbooking (model-level validation)
- ✅ Search & filter by title, event type, and date
- ✅ Django admin customization
- ✅ Signals for RSVP confirmation
- 🚫 Deployment not included in this version

---

## 🔧 Tech Stack

- Python 3.x
- Django 4.x
- SQLite (default, can be swapped)
- Bootstrap (CDN)

---

## 📸 Screenshots

_(Add screenshots here later if you'd like)_

---

## ⚙️ Getting Started (to see steps with code, to the last section at the bottom)

### 1. Clone the repo 
### 2. Create virtual environment
### 3. Install dependencies
### 4. Run migrations
### 5. Create superuser
### 6. Start development server


## Testing the app
Visit http://127.0.0.1:8000/

Register or log in as a user

Create and RSVP to events

Try filtering, searching, and capacity limits

## Admin Panel
Visit: http://127.0.0.1:8000/admin/

Log in using your superuser account

Manage events and attendees

## Folder Structure
event-booking-app/
│
├── events/              # App with models, views, URLs
├── templates/           # HTML templates
├── static/              # Static files (optional)
├── eventbooking/        # Project settings and URLs
├── manage.py            # Django entry point
├── requirements.txt     # Dependencies
├── README.md            # Project documentation
└── .gitignore           # Git ignored files

## Contributing
Contributions are welcomed! Fork the repo, make your changes, and submit a pull request.


### Steps 1 to 6 See here
```bash
### git clone https://github.com/your-username/event-booking-app.git
### cd event-booking-app


### 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


### 3. Install dependencies
pip install -r requirements.txt


### 4. Run migrations
python manage.py migrate


### 5. Create a superuser
python manage.py createsuperuser


### 6. Start development server
python manage.py runserver

