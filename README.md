🚀 Production-Ready REST API
A fully functional backend REST API built from scratch and deployed to the cloud.
This project demonstrates real-world backend engineering concepts including authentication, database design, testing, CI/CD, and production deployment.

🌐 Live Demo

🔗 API Base URL: (Railway url will expire on March 6, 2026)

<https://learning-rest-api-production.up.railway.app/>

📌 Project Overview

This project was built to practice and implement real backend architecture patterns. It simulates how production APIs are structured, secured, tested, and deployed.

The goal was to understand how all backend components work together:
**Architecture Flow**
```
Client → API → Auth → Database → Deployment → Monitoring

```

## 🔐 Authentication System

- JWT access tokens  
- OAuth2 password flow  
- Password hashing  
- Token validation middleware  
- Secure authentication endpoints 

## 🗄️ Database Features

- Structured relational schema  
- SQLAlchemy models  
- Migration system with Alembic  
- Versioned schema upgrades  
- Persistent cloud database

## ⚙️ Tech Stack & Why Each Was Used
| Technology | Purpose |
|--------|--------|
FastAPI | High-performance async API framework |
PostgreSQL | Reliable relational database |
SQLAlchemy | ORM for structured DB interaction |
Alembic | Version-controlled database migrations |
JWT | Secure token-based authentication |
OAuth2 | Standardized auth flow |
CORS | Enable secure cross-origin requests |
Railway | Simple cloud hosting platform |
GitHub | Version control + collaboration |
CI/CD | Automated build & deployment workflows |
Pytest | Automated testing framework |
YAML | Configuration + pipeline definitions |
Environment Variables | Secure secret management |


## 🏗️ Deployment

The API is deployed on Railway with:

- automated build
- environment variables
- production config
- live hosting

**Deployment Flow**
```
Code → GitHub → CI/CD → Railway → Live API
```