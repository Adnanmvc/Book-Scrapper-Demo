# Book Scraper Demo

A simple web scraping project demonstrating BeautifulSoup4, FastAPI backend, and a responsive dashboard.

## Overview

This project scrapes book data from [books.toscrape.com](http://books.toscrape.com/) and provides a REST API and web interface to search and export the data.

## Features

- Web scraping with BeautifulSoup4
- FastAPI REST API
- Search books by title
- Export data to XLSX
- Responsive web dashboard

## Tech Stack

**Backend:**
- Python 3.11+
- FastAPI
- BeautifulSoup4
- Requests
- OpenPyXL

**Frontend:**
- HTML/CSS/JavaScript

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/Adnanmvc/Book-Scrapper-Demo.git
cd book-scraper-demo
```

### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn[standard] beautifulsoup4 requests pydantic openpyxl
```

### 3. Run Backend

```bash
uvicorn main:app --reload
```

API runs at `http://127.0.0.1:8000`

### 4. Open Dashboard

Open `index.html` in your browser.

## Project Structure

```
book-scraper-demo/
├── backend/
│   ├── main.py              # FastAPI app
│   └── scraper/
│       └── books.py         # Scraping logic
└── index.html               # Dashboard
```

## API Endpoints

### Search Book
```http
GET /api/book?title=BookTitle
```

Response:
```json
{
  "title": "A Light in the Attic",
  "price": 51.77,
  "availability": "In stock",
  "rating": 3,
  "url": "http://books.toscrape.com/..."
}
```

### Export Books
```http
GET /api/books?limit=50
```

Returns XLSX file with scraped books.

## Dependencies

```bash
pip install fastapi uvicorn[standard] beautifulsoup4 requests pydantic openpyxl
```

## Notes

- Uses [books.toscrape.com](http://books.toscrape.com/) - a sandbox site for scraping practice
- Always respect robots.txt and website terms of service
- Implement rate limiting for production use

## License

MIT
