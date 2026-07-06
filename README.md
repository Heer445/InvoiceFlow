# InvoiceFlow - GST Invoice Generator

InvoiceFlow is a web-based GST Invoice Generator developed using **Flask, Python, HTML, CSS, and JavaScript**. It helps businesses create professional GST invoices with automatic tax calculation, invoice preview, PDF download, and invoice history management.

---

## Features

- Supplier Information Management
- Client Information Management
- Automatic Invoice Number Generation
- Invoice Configuration
- Add Multiple Products/Services
- Automatic GST Calculation
- Real-Time Invoice Preview
- Download Invoice as PDF
- Invoice History
- Simple and Responsive User Interface

---

## Technology Stack

- Python
- Flask
- HTML5
- CSS3
- JavaScript
- SQLite
- ReportLab (PDF Generation)

---

## Project Structure

```
InvoiceFlow/
│
├── app.py
├── requirements.txt
├── README.md
├── database.db
│
├── static/
│   └── css/
│       └── style.css
│
├── templates/
│   ├── index.html
│   ├── supplier.html
│   ├── client.html
│   ├── config.html
│   ├── items.html
│   ├── preview.html
│   └── history.html
│
└── instance/
    └── database.db
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/Heer445/InvoiceFlow.git
```

### Open the project folder

```bash
cd InvoiceFlow
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## Screens

- Home
- Supplier Details
- Client Details
- Invoice Configuration
- Items & Services
- Invoice Preview
- PDF Download
- Invoice History

---

## Future Improvements

- User Authentication
- Email Invoice to Client
- QR Code on Invoice
- Company Logo Upload
- Multiple GST Rates
- Dashboard Analytics
- Cloud Database Integration

---

## Developed By

**Heer Patel**

B.Tech Student

---

## License

This project is developed for educational and learning purposes.
