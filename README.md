# 🗺️ Google Maps & Yandex Maps Scraper

Google Maps & Yandex Maps scraper supporting **ALL countries worldwide** with population-based city selection and custom search queries.

## ✨ Features

- 🌍 **All Countries Worldwide** - Every country recognized by ISO 3166
- 📊 **Population-Based Selection** - Automatically scrapes top N most populated cities
- 🔍 **Custom Search Queries** - Search for anything: "Diesel Services", "Italian Restaurants", "Yoga Studios"
- 📈 **Comprehensive Data Extraction**:
  - Business Title
  - Rating (stars)
  - Number of Reviews
  - Category
  - Address
  - Website
  - Phone Number
  - Image Link
  - Google Maps Link
- 💾 **Multiple Export Formats** - CSV, JSON, or both
- ⚡ **Efficient & Fast** - Optimized for large-scale scraping
- 🛡️ **Robust Error Handling** - Auto-saves data on interruption

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/ilteris1/Google-Maps-Scraper.git
cd Google-Maps-Scraper
pip install -r requirements.txt
```

### Usage

```bash
python main.py
```

**Interactive Prompts:**
1. Enter country name 
2. Specify number of cities (1-100) - automatically selects most populated
3. Enter custom search query (e.g., "Diesel Services", "Coffee Shops")
4. Choose output format (CSV, JSON, or both)


## ⚙️ Configuration

Edit `config.py`:
```python
SCROLL_PAUSE_TIME = 2          # Seconds between scrolls
MAX_SCROLL_ATTEMPTS = 10       # Max scrolls per search
IMPLICIT_WAIT = 10             # Selenium wait time
PAGE_LOAD_TIMEOUT = 30         # Page load timeout
```

## 📋 Requirements

- Python 3.8+
- Chrome browser, Firefox Browser (ChromeDriver auto-installed)
- Internet connection
