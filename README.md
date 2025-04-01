# Animal Shelter Web App API

## 📋 Overview
A comprehensive backend API for managing an animal shelter system. Built using Django and Django REST Framework, this app allows shelters to manage animals, adoptions, fosters, volunteers, donations, and user authentication securely and efficiently.

## ✨ Features
- JWT and Token-based Authentication
- Custom User Authentication (Token + JWT)
- Secure Registration & Login for Admins, Volunteers, and General Users
- Password Reset and Account Recovery
- Role-based Access Control (Admin, Staff, Volunteer)
- Animals CRUD with Filtering & Search
- Adoptions and Fosters CRUD and Matching Tools
- Volunteer Scheduling and Tracking
- Donations (One-time + Recurring via Stripe/PayPal)
- Lost & Found Pet Reporting System
- Analytics and CSV Export
- Email Notification System
- CAPTCHA Integration
- Social Logins (Google, Facebook, Twitter)

## ⚙️ Setup Instructions

1. **Clone Repository:**
   ```bash
   git clone https://github.com/your-username/animal-shelter-webapp.git
   cd animal-shelter-webapp
   ```

2. **Create & Activate Virtual Environment:**
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run Server Locally:**
   ```bash
   python manage.py runserver
   ```

6. **Create Superuser (Optional):**
   ```bash
   python manage.py createsuperuser
   ```


## 📚 API Documentation

The full API documentation is structured folder-wise as in the Postman collection:

### 1. 🧑 Auth
- POST `/auth/register/` — Register
- POST `/auth/login/` — Login
- POST `/auth/password-reset/`
- POST `/auth/password-reset/confirm/`

### 2. 🐾 Animals
- POST `/animals/`
- GET `/animals/`
- GET `/animals/{id}/`
- PUT `/animals/{id}/`
- DELETE `/animals/{id}/`

### 3. 📋 Adoption
- Adoption Applications, Tracking, Matching, Agreements, Follow-up

### 4. 🏠 Foster Program
- Foster Applications, Placements, Matching, Communication

### 5. 🔍 Lost & Found
- Lost Pet Reporting: `/lostfound/lost/`
- Found Animal Reporting: `/lostfound/found/`
- Matching: `/lostfound/match/`

### 6. 📦 Inventory
- Inventory Items: `/inventory/items/`
- Low Stock Alerts: `/inventory/alerts/`
- Orders: `/inventory/orders/`

### 7. 🧮 Reporting & Analytics
- Reports: `/reports/`
- Visualizations: `/reports/visualize/`
- Export: `/reports/export/`

## 🔧 Environment Variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `EMAIL_HOST_USER` | Gmail address |
| `EMAIL_HOST_PASSWORD` | Gmail app password |
| `STRIPE_SECRET_KEY` | Stripe secret key |
| `STRIPE_PUBLISHABLE_KEY` | Stripe publishable key |
| `PAYPAL_CLIENT_ID` | PayPal sandbox/live client ID |
| `PAYPAL_SECRET` | PayPal sandbox/live secret |
| `REDIS_URL` | Redis connection URI |

## 🚀 Deployment

### Option 1: Render (One-Click GitHub Deploy)
1. Go to [https://render.com](https://render.com)
2. Create new Web Service
3. Connect GitHub repo
4. Set environment variables:
   - `DEBUG=False`
   - `DJANGO_SECRET_KEY=your-secret`
   - `DATABASE_URL=your-db-url`
   - `ALLOWED_HOSTS=your-domain`
5. Select Python build and deploy

### Option 2: Railway / Vercel + Supabase (or ElephantSQL)
1. Clone GitHub
2. Connect Railway
3. Add PostgreSQL Plugin
4. Set environment variables


## 📝 License

This project is licensed under the [MIT License](LICENSE).

## 🤝 Contributors

- [Koushik Saha](https://github.com/Koushik-Saha) — Developer
- [Animal Shelter Volunteer Team] — Design & Feedback
