# Quick Start Guide

## Installation (Ubuntu/Linux)

```bash
# 1. Install dependencies
pip3 install -r requirements.txt

# 2. Test setup (optional)
python3 test_setup.py

# 3. Run the scraper
python3 main.py
```

## Usage Example

```
Enter country name: Germany
> ger

Selected: Germany

How many top cities to scrape? (1-100): 5

Enter search query: Diesel Services

Output format:
1. CSV
2. JSON
3. Both

Select (1-3): 1

Configuration:
Country: Germany
Cities: 5 (by population)
Query: Diesel Services

Cities to scrape: Berlin, Hamburg, Munich, Köln, Frankfurt am Main

Press Enter to start...
```

## What It Does

1. **All Countries**: 249 countries worldwide (uses ISO 3166 standard)
2. **Population-Based Cities**: Automatically selects most populated cities
3. **Custom Search**: Type any query (e.g., "Diesel Services", "Italian Restaurants")
4. **Extracts**: Title, rating, reviews, category, address, website, phone, image, link

## Output

Files saved as: `{Country}_{Query}_{Timestamp}.csv` or `.json`

Example: `Germany_Diesel_Services_20240115_143022.csv`

## Tips

- Type partial country names (e.g., "united" finds USA, UK, UAE)
- Start with 1-3 cities to test before scaling up
- Use specific queries for better results ("Diesel Repair Shops" vs "diesel")
- CSV format works best for Excel/Google Sheets
