# 🗓️ Event Booking App API

[![Django CI Pipeline](https://github.com/melo-b/event-booking-app/actions/workflows/django-ci.yml/badge.svg)](https://github.com/melo-b/event-booking-app/actions/workflows/django-ci.yml)

A highly reliable, concurrency-safe event booking platform built with Django. 

This project demonstrates how to build a production-ready backend that handles race conditions, enforces strict data integrity, and provides predictable API responses for frontend clients.

---

## 🛡️ Engineering Focus: Safety & Reliability

Coming from a Product Safety Engineering background in the TIC industry, my primary focus in software development is risk mitigation, fault tolerance, and system reliability. This application implements several enterprise-level safety patterns:

### 1. Concurrency & Race Condition Prevention
In an event booking system, the most critical failure point is the "Last Ticket" race condition. This application utilizes database transactions (`transaction.atomic()`) and row-level locking (`select_for_update()`). This guarantees atomic operations and completely prevents double-booking when multiple users attempt to claim the final capacity slot at the exact same millisecond.

### 2. Defense-in-Depth Data Integrity
While application-level validation exists in the views, strict data integrity is enforced at the database level. The schema utilizes a `UniqueConstraint` on the RSVP model to mathematically guarantee a user can never possess duplicate tickets, regardless of how the data enters the system (e.g., bypassing the UI via API or Admin panel).

### 3. Predictable API Error Handling (Global Middleware)
Unhandled server crashes (500 errors) typically return HTML tracebacks, which break frontend/mobile applications and leak system data. I implemented a **Global Exception Handling Middleware** that intercepts crashes, securely logs the full stack trace on the server, and returns a sanitized, standardized JSON response to the client with a traceable UUID:

```json
{
  "error": {
    "code": "INTERNAL_SERVER_ERROR",
    "message": "An unexpected system error occurred. Our engineering team has been notified.",
    "reference_id": "8f4b2c9d1a3e47b29f8c7d6e5a4b3c2d"
  }
}

🔧 Tech Stack & Architecture
Framework: Python 3.11, Django 5.2

Database: SQLite (Configured for easy swap to PostgreSQL in production)

Testing: Django TestCase (Automated suite proving concurrency limits and model constraints)

CI/CD: GitHub Actions (Automated testing and linting on every push to main)

Infrastructure: Docker & Docker Compose for isolated, reproducible environments


🚀 Getting Started (Local Development)
This project is fully containerized with Docker, eliminating "it works on my machine" environment issues.

Prerequisites
Docker Desktop installed and running.

1-Click Setup
Clone the repository and spin up the isolated container:


git clone [https://github.com/melo-b/event-booking-app.git](https://github.com/melo-b/event-booking-app.git)
cd event-booking-app
docker-compose up --build


The application will be instantly available at http://localhost:8000.

Note: The local database volume is mounted automatically. To run migrations or tests inside the container, use:
docker-compose exec web python manage.py test