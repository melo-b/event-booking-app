# 🗓️ Event Booking App

A Django-based web application that allows users to create events and RSVP to them. Includes search and filtering, capacity limits, admin tools, and RSVP confirmation logic.


[![Django CI Pipeline](https://github.com/melo-b/event-booking-app/actions/workflows/django-ci.yml/badge.svg)](https://github.com/melo-b/event-booking-app/actions/workflows/django-ci.yml)


---

## 🚀 Features

- ✅ User authentication (login, logout, registration)
- ✅ Create, edit, delete events (CRUD)
- ✅ RSVP to events with cancellation support
- ✅ Prevent overbooking (model-level validation)
- ✅ Search & filter by title, event type, and date
- ✅ Pagination for event listings
- ✅ Django admin customization
- ✅ Email notifications for RSVPs (simulated)
- ✅ Error handling with custom 404/500 pages
- ✅ Responsive CSS styling
- ✅ Comprehensive test coverage
- ✅ Environment variable configuration
- 🚫 Deployment not included in this version

---

## 🛡️ Engineering Focus: Safety & Reliability

Coming from a Product Safety Engineering background, my primary focus in backend development is risk mitigation, data integrity, and system reliability. This application implements several enterprise-level safety patterns:

* **Concurrency & Race Condition Prevention:** The RSVP booking engine utilizes database transactions (`transaction.atomic()`) and row-level locking (`select_for_update()`). This guarantees atomic operations and completely prevents double-booking race conditions when multiple users attempt to claim the final capacity slot simultaneously.
* **Defense-in-Depth Data Integrity:** While application-level validation exists, strict data integrity is enforced at the database level. The PostgreSQL/SQLite schema utilizes `UniqueConstraint` on the RSVP model to mathematically guarantee a user can never possess duplicate tickets, regardless of how the data enters the system.

---

## 🔧 Tech Stack

- Python 3.x
- Django 5.2.1
- SQLite (default, can be swapped)
- HTML/CSS with custom styling
- Python-decouple for environment variables

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

## Running Tests
```bash
python manage.py test
```

The test suite includes:
- Model tests (Event, RSVP, UserProfile)
- View tests (CRUD operations, permissions, search/filtering)
- Authentication tests
- Capacity and RSVP functionality tests

## Folder Structure
event-booking-app/
│
├── events/              # App with models, views, URLs
├── templates/           # HTML templates
├── config/              # Project settings and URLs
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

