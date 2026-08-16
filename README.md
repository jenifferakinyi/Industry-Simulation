# Industry-Simulation
# Northstar Retail Co. — Support Deflection MVP
> **Group 83 Champions — Northstar Sprint**  
> Pure Django + HTML/CSS/JS Support Deflection Chatbot built to automate retail customer support lookups.

---

## Overview

Northstar Retail Co.'s support team was drowning in repetitive inquiries. This lightweight, zero-dependency Django application deflects manual tickets across **all 3 primary support categories**:

| Ticket Category | Automated Deflection Method | Status |
| :--- | :--- | :--- |
| 📦 **1. Order Status** | Instant DB lookup via order number (`NS-XXXX`) returning status, tracking #, carrier, and ETA | ✅ Operational |
| ↩️ **2. Returns & Refunds** | Self-serve policy lookup & real-time return request status tracking | ✅ Operational |
| 🔍 **3. Stock Availability** | Real-time inventory query by product name/SKU + Swahili dialect support (`kiatu iko?`) | ✅ Operational |

---

## ⚙️ Quick Start

```bash
# 1. Clone repository & enter project directory
git clone https://github.com/jenifferakinyi/Industry-Simulation.git
cd Industry-Simulation

# 2. Set up & activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Migrate database & seed 10 demo orders
python manage.py migrate
python manage.py populate_demo_data

# 5. Start development server
python manage.py runserver 8080
```

Open your browser at **`http://localhost:8080/`** to test the live chatbot interface.

---

## 📁 Key Files & Architecture

```text
northstar_support/
├── CHARTER.md                  ← Assignment 1: Team Working Agreement & Charter
├── BOARD.md                    ← Assignment 1: Task Tracking Board & Audit Trail
├── BOARD.txt                   ← Sprint Task Board (Formatted ASCII Table)
├── GO_LIVE_NOTE.md             ← Assignment 2: Client Go-Live Readiness Note
├── requirements.txt            ← Django 5.1 dependencies
├── manage.py
│
├── northstar_support/          ← Django project settings & URLs
│   ├── settings.py
│   └── urls.py
│
└── support/                    ← Main support deflection app
    ├── models.py               ← Order, ReturnRequest, & StockItem ORM models
    ├── views.py                ← Intent engine & JSON chat_api endpoint
    ├── urls.py                 ← App URL routing
    ├── management/commands/
    │   └── populate_demo_data.py ← Seeder script (populates 10 demo orders)
    └── templates/support/
        └── chatbot.html        ← Self-contained Chatbot UI with suggestion chips
```

---

## 👥 Pod 83 Engineering Team

- **Jacob Muema (`jacobmuema02@gmail.com`)** — Team Lead & Backend Eng (Architecture, Django Views & Audit Log)
- **Victor Njagi (`vnjagi05@gmail.com`)** — Backend Eng (Database Models, Migrations & Seeder Engine)
- **Jeniffer Otigo (`otigojeniffer19@gmail.com`)** — QA & Product Eng (Deflection Test Suite & Go-Live Note)
- **Olajide Balogun (`bolfem@gmail.com`)** — Frontend Eng (Chatbot HTML/CSS Interface & Responsive Layout)
- **Bianca Akumu (`biancaakumu2005@gmail.com`)** — Frontend Eng (Interactive Chips & Swahili Dialect UX)
