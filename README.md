# 🏡 Rental System API

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14-red.svg)](https://www.django-rest-framework.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![Pytest](https://img.shields.io/badge/Tested_with-Pytest-yellow.svg)](https://pytest.org/)

## Overview

Rental System API is a production-oriented backend service for a property rental marketplace similar to Airbnb.

The platform supports the complete rental lifecycle:

* Property management
* Availability tracking
* Reservation workflow
* Review and rating system
* Search history collection
* Listing analytics
* Role-based access control

The project was designed with scalability, maintainability, and clean separation of business domains in mind.

---

## Key Features

### Authentication & Authorization

* JWT authentication (Djoser + SimpleJWT)
* Custom user model
* Role-based permissions:

  * User
  * Host
  * Admin
* Protected API endpoints

### Property Listings

Hosts can:

* Create listings
* Update listings
* Manage availability
* Track listing popularity

Users can:

* Browse properties
* Search listings
* Filter by location, price, and room count

### Reservation Management

Booking workflow includes:

* Reservation creation
* Date conflict validation
* Overbooking prevention
* Host approval process

All booking operations are validated at the application layer to ensure data consistency.

### Reviews & Ratings

* Reviews available only for eligible bookings
* Rating aggregation per property
* Ownership validation
* Fraud prevention through booking verification

### Search & Analytics

The system collects behavioral metrics including:

* Search history
* Listing views
* Popular search terms
* Most viewed properties

Analytics endpoints provide aggregated business insights without affecting transactional workloads.

---

## Architecture

The application follows a modular domain-driven structure.

```text
apps/
├── users
├── listings
├── bookings
├── reviews
├── searches
└── analytics
```

### Domain Responsibilities

| Module    | Responsibility                        |
| --------- | ------------------------------------- |
| users     | Authentication, profiles, permissions |
| listings  | Property management                   |
| bookings  | Reservation workflow                  |
| reviews   | Ratings and feedback                  |
| searches  | Search history                        |
| analytics | Aggregated metrics                    |

This separation minimizes coupling between domains and simplifies future scaling and maintenance.

---

## Technology Stack

### Backend

* Python 3.12
* Django 4.2
* Django REST Framework

### Database

* MySQL 8

### Infrastructure

* Docker
* Docker Compose
* Gunicorn

### Testing

* Pytest
* Pytest-Django
* Factory Boy
* Coverage

### Authentication

* JWT
* Djoser
* SimpleJWT

---

## Business Rules

### Booking Validation

The system prevents overlapping reservations for the same property.

Before creating a booking:

1. Existing reservations are checked.
2. Date ranges are validated.
3. Conflicting reservations are rejected.

This guarantees booking consistency and eliminates double-booking scenarios.

### Review Validation

Users may submit reviews only when:

* A valid booking exists.
* The booking belongs to the requesting user.
* The booking satisfies review eligibility requirements.

### Permission Model

#### User

* Browse listings
* Create bookings
* Submit reviews

#### Host

* Manage owned properties
* Confirm reservations
* Access listing statistics

#### Admin

* Full platform access

---

## API Highlights

### Authentication

```http
POST /auth/users/
POST /api/token/
POST /api/token/refresh/
```

### Listings

```http
GET    /api/listings/
POST   /api/listings/
GET    /api/listings/popular/
```

### Bookings

```http
GET    /api/bookings/
POST   /api/bookings/
POST   /api/bookings/{id}/confirm_booking/
```

### Reviews

```http
GET    /api/reviews/?listing={id}
POST   /api/reviews/
```

---

## Local Development

### Environment Variables

```env
SECRET_KEY=your_secret_key

DEBUG=True

DB_NAME=rental_db
DB_USER=rental_user
DB_PASSWORD=rental_password
DB_HOST=db
DB_PORT=3306
```

### Run Application

```bash
docker-compose up -d --build
```

Apply migrations:

```bash
docker-compose exec web python manage.py migrate
```

Create administrator:

```bash
docker-compose exec web python manage.py createsuperuser
```

---

## Testing

Run test suite:

```bash
docker-compose exec web pytest
```

Run coverage:

```bash
docker-compose exec web coverage run -m pytest
docker-compose exec web coverage report
```

The test suite covers:

* Authentication flows
* Permission checks
* Booking validation
* Review restrictions
* Business logic
* API endpoints

---

## Production Readiness

### Security

* JWT authentication
* Environment-based configuration
* Secret isolation via environment variables
* Role-based authorization

### Deployment Recommendations

```text
Nginx
   ↓
Gunicorn
   ↓
Django API
   ↓
MySQL
```

### Operational Requirements

* DEBUG=False
* Reverse proxy (Nginx)
* Scheduled maintenance jobs
* Centralized logging
* Automated backups

---

## Future Enhancements

* Redis caching layer
* Celery background workers
* OpenAPI/Swagger documentation
* Stripe payment integration
* Object storage for media uploads
* Event-driven notifications
* Elasticsearch integration
* Horizontal scaling support

---

## Engineering Focus

This project demonstrates:

* REST API design
* Domain-driven application structure
* Authentication and authorization
* Transaction-safe booking workflows
* Business rule enforcement
* Containerized deployment
* Automated testing practices
* Production-oriented backend architecture

---

## License

MIT License
