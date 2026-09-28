# Invoice AI

AI-powered invoice data extraction application built with Django and Gemini.

## Live Demo

https://invoice-extractor-c9qw.onrender.com/

> Note: The application is deployed on Render. If the server has been inactive, it may take a few minutes to start. Please wait for a few minutes and refresh the page if it does not load immediately.

## Features

* Upload invoice PDF files
* Upload multiple invoices
* Select specific information to extract
* AI-powered invoice data extraction
* Extract invoice number
* Extract invoice date
* Extract billed-to information
* Extract other user-selected invoice fields
* Display extracted invoice information
* Download AI extraction results
* Download original invoice PDFs
* View invoice history
* Delete invoice records
* Generate downloadable reports
* Store invoice files using Supabase Storage
* PostgreSQL database
* Django admin panel

## Tech Stack

* Python
* Django
* PostgreSQL
* Gemini
* Supabase Storage
* HTML
* CSS
* JavaScript

## Project Structure

```text
invoice-extractor/
│
├── invoices/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── ...
│
├── invoice_extractor/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
│
├── static/
│   └── css/
│       └── style.css
│
├── templates/
│   └── ...
│
├── .env.example
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

## How It Works

1. Upload one or more invoice PDF files.
2. Select the information you want to extract.
3. Gemini analyzes the invoice and extracts the selected information.
4. The extracted data is displayed in the application.
5. Results can be downloaded as a report.
6. Invoice files and extraction history can be viewed or managed later.

## Download and Run Locally

You can download the project by clicking **Code → Download ZIP** on the GitHub repository.

After downloading, extract the ZIP file and open the project folder in a terminal.

```bash
cd invoice-extractor

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

Open the application at:

```text
http://127.0.0.1:8000/
```

Create a `.env` file using `.env.example` and add your Django, Gemini, PostgreSQL and Supabase credentials before running the application.

## Deployment

The application is deployed on Render:

https://invoice-extractor-c9qw.onrender.com/

The first request may take a few minutes if the server is waking up. Please wait and refresh the
