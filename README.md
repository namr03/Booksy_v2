# Booksy_v2

**Booksy_v2** to aplikacja webowa do zarządzania rezerwacjami usług, tworzona w Django. Projekt jest w trakcie rozwoju i ma na celu umożliwienie użytkownikom umawiania wizyt, a właścicielom firm – zarządzanie dostępnością, usługami i klientami.

## 🔧 Stack technologiczny

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Baza danych**: SQlite3
- **System uwierzytelniania**: wbudowany system Django auth

## ✨ Główne funkcjonalności (obecne i planowane)

### ✅ Zaimplementowane:
- Rejestracja i logowanie użytkowników
- Profile użytkowników
- Podstawowy panel administratora
- Obsługa usług i terminów
- System rezerwacji wizyt
- Panel klienta z historią wizyt
- Rozbudowa panelu klienta o możliwość anulowania wizyt

### 🔄 W planach:
- System powiadomień e-mailowych
- Możliwość edycji danych klienta z poziomu panelu
- Implementacja RWD
- Konteneryzacja Docker

## 🚀 Uruchomienie projektu lokalnie

```bash
git clone https://github.com/namr03/Booksy_v2.git
cd Booksy_v2
python -m venv venv
source venv/bin/activate  # lub venv\Scripts\activate na Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
