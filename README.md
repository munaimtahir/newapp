# Reminder App

This project starts a Django-based reminder service that parses natural language
to extract dates, times and locations. A simple web interface lets you paste a
sentence like "I will go to hospital tomorrow at 8 am" and stores the parsed
reminder in the database.

## Running locally

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then open http://localhost:8000/ to set reminders.
