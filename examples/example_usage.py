"""
Example usage of Google Maps Scraper
This demonstrates how to use the scraper programmatically
"""

from scraper import GoogleMapsScraper
import pandas as pd

def example_basic_scraping():
    """Basic example: Scrape restaurants in New York"""
    scraper = GoogleMapsScraper(headless=True)
    
    try:
        # Search for places
        links = scraper.search_places("restaurants", "New York", "USA")
        print(f"Found {len(links)} restaurants")
        
        # Extract data from first 5 places
        data = []
        for link in links[:5]:
            place_data = scraper.extract_place_data(link)
            if place_data:
                data.append(place_data)
        
        # Save to CSV
        df = pd.DataFrame(data)
        df.to_csv("nyc_restaurants.csv", index=False)
        print("Data saved to nyc_restaurants.csv")
        
    finally:
        scraper.close()

def example_multiple_cities():
    """Advanced example: Scrape multiple cities"""
    scraper = GoogleMapsScraper(headless=True)
    cities = ["Los Angeles", "Chicago", "Houston"]
    all_data = []
    
    try:
        for city in cities:
            print(f"Scraping {city}...")
            links = scraper.search_places("hotels", city, "USA")
            
            for link in links[:10]:  # Limit to 10 per city
                place_data = scraper.extract_place_data(link)
                if place_data:
                    place_data['city'] = city
                    all_data.append(place_data)
        
        df = pd.DataFrame(all_data)
        df.to_csv("usa_hotels.csv", index=False)
        print(f"Scraped {len(all_data)} hotels from {len(cities)} cities")
        
    finally:
        scraper.close()

if __name__ == "__main__":
    print("Example 1: Basic scraping")
    example_basic_scraping()
    
    print("\nExample 2: Multiple cities")
    example_multiple_cities()
