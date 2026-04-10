# SaaS Backend (FastAPI)

This project is a backend system for a subscription-based SaaS application.

## 🚀 Features
- User Registration & Login
- OTP Verification
- JWT Authentication
- Project Management (CRUD)
- Subscription Plans (Free & Pro)
- Project Limit Enforcement
- Payment History
- Admin APIs
- Notification System

## 🛠 Tech Stack
- FastAPI
- SQLAlchemy
- MySQL
- JWT Auth

## ▶️ Run Project
```bash
uvicorn main:app --reload
```

## 🔷 Stripe Integration

- Implemented Stripe Checkout for subscription payments  
- Users can subscribe to the Pro plan using test mode  
- Used Stripe test cards for safe payment simulation  

## 🔷 Webhook Handling

- Implemented Stripe webhook endpoint to receive payment events  
- Handled checkout.session.completed event  
- Updated user status in database on successful payment  
- Stored payment details in Payment table  
- Webhook tested locally using API calls  

## 🔷 Test Payment

- Card Number: 4242 4242 4242 4242  
- Expiry: 12/30  
- CVC: 123  

> Note: Stripe webhook requires a public URL. For this project, webhook was tested locally.

> ## 📌 API Endpoints

- POST /create-checkout-session → Create Stripe checkout session  
- POST /webhook → Handle Stripe payment events  
