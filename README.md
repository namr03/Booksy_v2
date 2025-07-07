# Booksy\_v2

**Booksy\_v2** is a web application for managing service appointments, built with Django. The project is currently under development and aims to allow users to book appointments, while enabling business owners to manage availability, services, and clients.

## 🔧 Tech Stack

* **Backend**: Django (Python)
* **Frontend**: HTML, CSS, JavaScript
* **Database**: SQLite3
* **Authentication System**: Django's built-in auth system

## ✨ Key Features (Implemented & Planned)

### ✅ Implemented:

* User registration and login
* User profiles
* Basic admin panel
* Service and appointment management
* Appointment booking system
* Client panel with appointment history
* Extended client panel with appointment cancellation

### 🔄 Planned:

* Email notification system
* Client data editing from the panel
* Responsive Web Design (RWD)
* Docker containerization

## 🚀 Running the Project Locally

```bash
git clone https://github.com/namr03/Booksy_v2.git
cd Booksy_v2
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
