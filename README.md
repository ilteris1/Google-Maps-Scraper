# 🗺️ Google Maps Scraper - Global Edition

Professional Google Maps scraper supporting **ALL countries worldwide** with population-based city selection and custom search queries.

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
git clone https://github.com/yourusername/Google-Maps-Scraper.git
cd Google-Maps-Scraper
pip install -r requirements.txt
```

### Usage

```bash
python main.py
```

**Interactive Prompts:**
1. Enter country name (e.g., "United States", "Germany", "Japan")
2. Specify number of cities (1-100) - automatically selects most populated
3. Enter custom search query (e.g., "Diesel Services", "Coffee Shops")
4. Choose output format (CSV, JSON, or both)

### Example Session

```
Enter country name: United States
How many top cities to scrape? 10
Enter search query: Diesel Services
Output format: 1 (CSV)

✓ Will scrape: New York, Los Angeles, Chicago, Houston, Phoenix...
```

## 📊 Output Format

### CSV Example
```csv
title,rating,reviews,category,address,website,phone,image,link,city,country,search_query
"ABC Diesel Service",4.7,342,"Diesel engine repair","123 Main St, New York, NY","https://example.com","+1234567890","https://...",https://maps.google.com/...,New York,United States,Diesel Services
```

### JSON Example
```json
[
  {
    "title": "ABC Diesel Service",
    "rating": "4.7",
    "reviews": "342",
    "category": "Diesel engine repair",
    "address": "123 Main St, New York, NY",
    "website": "https://example.com",
    "phone": "+1234567890",
    "image": "https://...",
    "link": "https://maps.google.com/...",
    "city": "New York",
    "country": "United States",
    "search_query": "Diesel Services"
  }
]
```

## 🌍 Supported Countries

**All 249 countries and territories** including:
- 🇺🇸 United States
- 🇬🇧 United Kingdom
- 🇩🇪 Germany
- 🇫🇷 France
- 🇯🇵 Japan
- 🇨🇳 China
- 🇮🇳 India
- 🇧🇷 Brazil
- 🇦🇺 Australia
- And 240+ more...

## 🎯 Use Cases

- 🔧 **B2B Lead Generation** - Find "Diesel Services", "Industrial Equipment", "Wholesale Suppliers"
- 🍕 **Market Research** - Analyze "Pizza Restaurants", "Vegan Cafes", "Luxury Hotels"
- 📍 **Location Intelligence** - Map "EV Charging Stations", "Pharmacies", "Gyms"
- 🏢 **Competitor Analysis** - Track businesses in specific industries
- 📊 **Data Analytics** - Build datasets for business intelligence

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
- Chrome browser (ChromeDriver auto-installed)
- Internet connection

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

## ⚠️ Disclaimer

Educational purposes only. Respect:
- Google's Terms of Service
- Rate limiting
- Data protection regulations (GDPR, CCPA)

## 📝 License

MIT License - See [LICENSE](LICENSE)

## 🌟 Star This Repository

If this helps your project, give it a star! ⭐

---

Made with ❤️ for global data intelligence
