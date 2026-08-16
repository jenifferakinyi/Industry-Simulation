# Assignment 2: 1-Page Go-Live Readiness Note
Client: Northstar Retail Co.  
System: Support Deflection MVP (Django Chatbot Engine)  
Date: August 15, 2026  
Authors: Pod 83 Engineering Team (Jacob Muema, Victor Njagi, Jeniffer Otigo, Olajide Balogun, Bianca Akumu)

---

## 1. Executive Summary & Deflection Scope
The Northstar Support Deflection MVP is a lightweight, zero-dependency Django application built to automate ticket handling across all 3 primary support categories:

| Ticket Category | Automated Handling Method | Live Status |
|---|---|---|
| 1. Order Status | Instant DB lookup via order number (`NS-XXXX`) returning status, tracking #, carrier, and ETA | ✅ Operational |
| 2. Returns & Refunds | Self-serve policy lookup & real-time return request status tracking | ✅ Operational |
| 3. Stock Availability | Real-time inventory query by product name/SKU + Swahili dialect support (`kiatu iko?`) | ✅ Operational |

---

## 2. What Works (Shipped Capabilities)
- Interactive Chatbot Interface: Pure HTML/CSS/JS frontend located at /chat/ with zero heavy node dependencies.
- Natural Language Intent Matching: Handles order status queries, return requests, and stock availability checks using regex and keyword matching.
- Swahili / Sheng Dialect Support: Maps local terms like kiatu`/`viatu directly to sneaker inventory lookups.
- Graceful Out-of-Catalog Fallback: When a product is not in the database, the system cleanly displays available store catalog items.
- Seeded Demo Data: Custom command (`python manage.py populate_demo_data`) populates 10 orders, stock items, and returns.

---

## 3. Known Limitations & Gaps
- Rule-Based Engine: Current NLP uses pattern matching; complex unstructured messages outside standard keywords trigger the fallback prompt.
- Auth Layer: Staff administrative endpoints were decoupled to streamline customer self-serve deflection. Database updates are currently performed via Django Admin (`/admin/`).
- Email Notifications: Back-in-stock alerts register customer emails in SQLite; SMTP delivery requires production gateway configuration.

---

## 4. Handover & Onboarding Guide for Northstar Team

### Quick Start Commands
# 1. Clone repository & enter directory
git clone https://github.com/jenifferakinyi/Industry-Simulation.git
cd Industry-Simulation

# 2. Activate virtual environment & install requirements
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Initialize database & seed demo data
python manage.py migrate
python manage.py populate_demo_data

# 4. Run development server
python manage.py runserver 8080