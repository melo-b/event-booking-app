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

## ⚙️ Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/event-booking-app.git
cd event-booking-app


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


## Testing the App
Visit http://127.0.0.1:8000/

Register/login as a user

Create and RSVP to events

Try filtering, searching, and capacity limits

## Admin Panel
Access at: http://127.0.0.1:8000/admin/

Login with your superuser account to manage events and attendees.

## Folder Structure
event-booking-app/
│
├── events/              # App with models, views, URLs
├── templates/           # HTML templates
├── static/              # Static files (optional)
├── eventbooking/        # Project settings and URLs
├── manage.py
├── requirements.txt     # Generated via pip freeze
└── README.md


## Contributing

Contributions are welcomed! Fork the repo, make changes, and submit a pull request.

