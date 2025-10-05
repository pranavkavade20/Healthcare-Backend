# Healthcare Backend System
Dear Gungun and WhatBytes Team,
  - I hope you are doing well.
  - Please find attached my completed Django REST Framework backend assignment as part of the hiring process.  
 - I’ve implemented all the required features as mentioned in the assignment instructions.
## 📋 Table of Contents
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)


## 📁 Project Structure

```
healthcare_backend/
│
├── healthcare/                 # Main project directory
│   ├── __init__.py
│   ├── settings.py             # Project settings
│   ├── urls.py                 # Main URL configuration
│   ├── asgi.py
│   └── wsgi.py
│
├── authentication/              # Authentication app
│   ├── models.py               # Custom User model
│   ├── serializers.py          # User serializers
│   ├── views.py                # Authentication views
│   ├── urls.py                 # Authentication URLs
│   ├── utils.py                # Helper functions
│   └── admin.py                # Admin configuration
│
├── patients/                    # Patient management app
│   ├── models.py               # Patient model
│   ├── serializers.py          # Patient serializers
│   ├── views.py                # Patient views
│   ├── urls.py                 # Patient URLs
│   └── admin.py                # Admin configuration
│
├── doctors/                     # Doctor management app
│   ├── models.py               # Doctor model
│   ├── serializers.py          # Doctor serializers
│   ├── views.py                # Doctor views
│   ├── urls.py                 # Doctor URLs
│   └── admin.py                # Admin configuration
│
├── mappings/                    # Patient-Doctor mapping app
│   ├── models.py               # Mapping model
│   ├── serializers.py          # Mapping serializers
│   ├── views.py                # Mapping views
│   ├── urls.py                 # Mapping URLs
│   └── admin.py                # Admin configuration
│
├── venv/                        # Virtual environment
├── .env                         # Environment variables (not in git)
├── .env.example                 # Example environment file
├── .gitignore                   # Git ignore file
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd healthcare_backend
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### Step 1: Environment Variables

Create a `.env` file in the project root directory:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-generate-a-strong-one
DEBUG=True

# Database Settings
DB_NAME=healthcare_db
DB_USER=healthcare_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
```

### Step 2: Generate Secret Key

Generate a new Django secret key:

```python
# Run in Python shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Copy the generated key to your `.env` file.

## 🗄️ Database Setup

### Step 1: Create PostgreSQL Database

Open PostgreSQL command line or pgAdmin and run:

```sql
-- Create database
CREATE DATABASE healthcare_db;

-- Create user
CREATE USER healthcare_user WITH PASSWORD 'your_secure_password';
```

### Step 2: Run Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Step 3: Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

## 🏃 Running the Application

### Development Server

```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

### Admin Panel

Access the admin panel at: `http://127.0.0.1:8000/admin/`

Login with the superuser credentials you created.

## 📚 API Documentation

### Base URL

```
http://127.0.0.1:8000/api/
```

### Authentication Endpoints

#### 1. Register User
```http
POST /api/auth/register/
```

**Request Body:**
```json
{
  "name": "pranav kavade",
  "email": "pranav@example.com",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user": {
      "id": 1,
      "name": "pranav kavade",
      "email": "pranav@example.com",
      "date_joined": "2025-10-05T10:30:00Z"
    },
    "tokens": {
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
      "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
  }
}
```

#### 2. Login User
```http
POST /api/auth/login/
```

**Request Body:**
```json
{
  "email": "pranav@example.com",
  "password": "SecurePass123!"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": 1,
      "name": "pranav kavade",
      "email": "pranav@example.com",
      "date_joined": "2025-10-05T10:30:00Z"
    },
    "tokens": {
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
      "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
  }
}
```

### Patient Endpoints

#### 1. Create Patient
```http
POST /api/patients/
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "first_name": "ABC",
  "last_name": "XYZ",
  "email": "abc@email.com",
  "phone": "+919876543210",
  "date_of_birth": "1990-05-15",
  "gender": "F",
  "blood_group": "A+",
  "address": "123 Main Street, Apartment 4B",
  "city": "Mumbai",
  "state": "Maharashtra",
  "postal_code": "400001",
  "country": "India",
  "medical_history": "No significant medical history",
  "allergies": "Penicillin",
  "current_medications": "None",
  "emergency_contact_name": "pranav abc",
  "emergency_contact_phone": "+919876543211",
  "emergency_contact_relation": "Spouse"
}
```

#### 2. List Patients
```http
GET /api/patients/
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `search`: Search by name, phone, or email
- `gender`: Filter by gender (M/F/O)
- `city`: Filter by city
- `is_active`: Filter by active status (true/false)
- `page`: Page number
- `page_size`: Items per page

#### 3. Get Patient Details
```http
GET /api/patients/<id>/
Authorization: Bearer <access_token>
```

#### 4. Update Patient
```http
PUT /api/patients/<id>/
Authorization: Bearer <access_token>
```

#### 5. Delete Patient
```http
DELETE /api/patients/<id>/
Authorization: Bearer <access_token>
```

### Doctor Endpoints

#### 1. Create Doctor
```http
POST /api/doctors/
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "first_name": "Rajesh",
  "last_name": "Kumar",
  "email": "dr.rajesh@hospital.com",
  "phone": "+919876543220",
  "date_of_birth": "1975-08-20",
  "gender": "M",
  "specialization": "CARDIOLOGY",
  "qualification": "MBBS, MD Cardiology",
  "license_number": "MH12345",
  "experience_years": 15,
  "clinic_name": "City Heart Hospital",
  "clinic_address": "456 Medical Plaza, Ground Floor",
  "city": "Mumbai",
  "state": "Maharashtra",
  "postal_code": "400002",
  "country": "India",
  "consultation_fee": 1500,
  "available_days": "Monday to Friday",
  "available_time": "9:00 AM - 5:00 PM",
  "bio": "Experienced cardiologist specializing in heart disease prevention",
  "languages_spoken": "English, Hindi, Marathi"
}
```

#### 2. List Doctors
```http
GET /api/doctors/
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `search`: Search by name, specialization, city
- `specialization`: Filter by specialization
- `city`: Filter by city
- `is_available`: Filter by availability
- `min_experience`: Minimum years of experience
- `max_fee`: Maximum consultation fee
- `page`: Page number
- `page_size`: Items per page

#### 3. Get Doctor Details
```http
GET /api/doctors/<id>/
Authorization: Bearer <access_token>
```

#### 4. Update Doctor
```http
PUT /api/doctors/<id>/
Authorization: Bearer <access_token>
```

#### 5. Delete Doctor
```http
DELETE /api/doctors/<id>/
Authorization: Bearer <access_token>
```

### Mapping Endpoints

#### 1. Create Mapping (Assign Doctor to Patient)
```http
POST /api/mappings/
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "patient": 1,
  "doctor": 1,
  "reason": "Regular checkup and consultation for hypertension",
  "notes": "Patient prefers morning appointments",
  "status": "ACTIVE"
}
```

#### 2. List All Mappings
```http
GET /api/mappings/
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `patient_id`: Filter by patient ID
- `doctor_id`: Filter by doctor ID
- `status`: Filter by status (ACTIVE/INACTIVE/COMPLETED)
- `search`: Search by patient or doctor name
- `page`: Page number
- `page_size`: Items per page

#### 3. Get Doctors for a Patient
```http
GET /api/mappings/<patient_id>/
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `status`: Filter by mapping status

#### 4. Update Mapping
```http
PATCH /api/mappings/detail/<mapping_id>/
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "status": "INACTIVE",
  "notes": "Updated notes"
}
```

#### 5. Delete Mapping (Remove Doctor from Patient)
```http
DELETE /api/mappings/detail/<mapping_id>/
Authorization: Bearer <access_token>
```

### Using Postman

1. **Import the Collection:**
   - Download Postman
   - Create a new collection
   - Add all endpoints listed above

2. **Set Environment Variables:**
   - `base_url`: `http://127.0.0.1:8000/api`
   - `access_token`: (Set after login)

3. **Authentication Flow:**
   - Register a new user
   - Login to get access token
   - Use the access token in Authorization header for protected endpoints

## 🔒 Security Features

### Authentication & Authorization
- JWT-based authentication with access and refresh tokens
- Password hashing using Django's built-in PBKDF2 algorithm
- Token expiration (Access: 1 hour, Refresh: 7 days)
- User-specific data access (users can only access their own data)

### Data Validation
- Comprehensive input validation on all endpoints
- Email format validation
- Phone number format validation
- Date validation (no future dates for DOB)
- Age validation (reasonable age ranges)
- Cross-field validation

### Security Headers
- CORS configuration for frontend integration
- CSRF protection enabled
- Secure password validation rules

