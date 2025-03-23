# Animal Shelter Web App API

## 📋 Overview
The Animal Shelter Web App API is a RESTful backend service for managing animal adoptions, donations, subscriptions, and reporting. It is designed to help shelters manage animals, staff, adoption requests, notifications, and financial operations efficiently.

## ✨ Features
- JWT and Token-based Authentication
- Role-Based Access Control (User, Staff, Admin)
- Animal CRUD and Adoption Workflow
- Stripe/PayPal Donations with Email Receipts
- Home Check Uploads
- AI-Powered Animal Matching System
- Admin Dashboard & Financial Reporting
- Caching (Redis), Rate Limiting, and i18n support

## ⚙️ Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/your-username/animal-shelter-api.git
cd animal-shelter-api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure your `.env`:
```env
DEBUG=True
SECRET_KEY=your-django-secret
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
STRIPE_SECRET_KEY=your-stripe-secret
STRIPE_PUBLISHABLE_KEY=your-stripe-pub
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_SECRET=your-paypal-secret
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Start the server:
```bash
python manage.py runserver
```

## 📚 API Documentation

The full API endpoints are documented in the [Postman Collection](AnimalShelter.postman_collection.json) and include:

- **Auth**: `/api/register/`, `/api/login/`, `/api/token/`
- **Animals**: `/api/animals/`, `/api/animals/<id>/`
- **Adoptions**: `/api/adopt/`, `/api/adopt/requests/`, `/api/adopt/requests/<id>/`
- **Payments**: `/api/stripe-payment/`, `/api/paypal-payment/`, `/api/subscribe/`
- **Profile & Upload**: `/api/profile/`, `/api/upload-home-verification/`
- **Notifications**: `/api/notifications/`, `/api/approve-adoption/<id>/`
- **Analytics**: `/api/admin-dashboard/`, `/api/analytics/*`
- **AI**: `/api/match-animals/`, `/api/animals/<id>/rank-candidates/`

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

To deploy:
1. Set `DEBUG=False` and configure `ALLOWED_HOSTS`
2. Use Gunicorn + Nginx or deploy on services like:
   - Heroku
   - Render
   - Railway
   - AWS (EC2 + RDS)

## 📝 License

This project is licensed under the [MIT License](LICENSE).

## 🤝 Contributors

- [Koushik Saha](https://github.com/your-profile) — Developer
- [Animal Shelter Volunteer Team] — Design & Feedback
