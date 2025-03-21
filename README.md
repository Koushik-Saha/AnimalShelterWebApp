# Animal Shelter API

## Overview

This project is a **Django REST Framework (DRF)**-based API for managing an animal shelter. It provides a **CRUD system** for managing animals, user authentication, payment integration (PayPal & Stripe), email notifications, and more.

## Features

- **Authentication:** User registration & login using Django Token Authentication.
- **Animal Management:** Create, read, update, and delete animal records.
- **Adoption Requests:** Submit and manage adoption requests.
- **Donation System:** Make donations via Stripe or PayPal.
- **Email Notifications:** Send emails upon successful donations or adoption approvals.
- **Filtering & Searching:** Filter animals based on availability and species.

## Setup Instructions

### 1️⃣ Clone the Repository

```sh
$ git clone https://github.com/your-repo/animal-shelter-api.git
$ cd animal-shelter-api
```

### 2️⃣ Create & Activate Virtual Environment

```sh
$ python3 -m venv venv
$ source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3️⃣ Install Dependencies

```sh
$ pip install -r requirements.txt
```

### 4️⃣ Setup Database (PostgreSQL)

Configure `.env` file:

```env
DATABASE_URL=postgres://your-user:your-password@localhost:5432/animal_shelter_db
```

Run migrations:

```sh
$ python manage.py migrate
```

### 5️⃣ Create Superuser

```sh
$ python manage.py createsuperuser
```

### 6️⃣ Run Server

```sh
$ python manage.py runserver
```

---

## API Documentation

### **1️⃣ User Authentication**

#### 🔹 **Register User**

**Endpoint:** `POST /api/register/`

```json
{
  "username": "koushik",
  "password": "password123"
}
```

**Response:**

```json
{
  "message": "Staff registered successfully",
  "token": {{token}}
}
```

#### 🔹 **Login User**

**Endpoint:** `POST /api/login/`

```json
{
  "username": "koushik",
  "password": "password123"
}
```

**Response:**

```json
{
  "token": {{token}}
}
```

Use this token in headers for other API calls:

```json
Authorization: Token {{token}}
```

---

### **2️⃣ Animal Management**

#### 🔹 **List All Animals**

**Endpoint:** `GET /api/animals/` **Headers:**

```json
Authorization: Token {{token}}
```

**Response:**

```json
[
  {
    "id": 1,
    "name": "Buddy",
    "species": "Dog",
    "breed": "Labrador",
    "status": "available"
  }
]
```

#### 🔹 **Get Single Animal Details**

**Endpoint:** `GET /api/animals/{id}/` **Example:** `/api/animals/1/`

#### 🔹 **Create an Animal**

**Endpoint:** `POST /api/animals/`

```json
{
  "name": "Bella",
  "species": "Cat",
  "breed": "Persian",
  "status": "available"
}
```

#### 🔹 **Update Animal**

**Endpoint:** `PUT /api/animals/{id}/`

```json
{
  "name": "Bella",
  "species": "Cat",
  "breed": "Siamese",
  "status": "adopted"
}
```

#### 🔹 **Delete Animal**

**Endpoint:** `DELETE /api/animals/{id}/`

---

### **3️⃣ Adoption Requests**

#### 🔹 **Request Adoption**

**Endpoint:** `POST /api/adoption/`

```json
{
  "user": 1,
  "animal": 2,
  "status": "Pending"
}
```

#### 🔹 **View Adoption Requests**

**Endpoint:** `GET /api/adoption/`

---

### **4️⃣ Donations**

#### 🔹 **Stripe Payment**

**Endpoint:** `POST /api/stripe-payment/`

```json
{
  "amount": "10.00"
}
```

#### 🔹 **PayPal Payment**

**Endpoint:** `POST /api/paypal-payment/`

```json
{
  "amount": "15.00"
}
```

---

### **5️⃣ Email Notifications**

#### 🔹 **Send Email**

**Endpoint:** `POST /api/email/`

```json
{
  "recipient": "user@example.com",
  "subject": "Adoption Confirmation",
  "message": "Your adoption request has been approved!"
}
```

---

## Environment Variables

Create a `.env` file and add:

```env
SECRET_KEY=your-secret-key
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_SECRET=your-paypal-secret-key
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-app-password
```

---

## Deployment (Optional)

For production, use **Gunicorn & Nginx**:

```sh
$ pip install gunicorn
$ gunicorn --bind 0.0.0.0:8000 animal_shelter.wsgi:application
```

For Docker deployment, create a `Dockerfile` and `docker-compose.yml`.

---

## License

This project is open-source and available under the MIT License.

---

## Contributors

- **Koushik Saha** - Developer

🚀 **Enjoy building and improving the Animal Shelter API!**

