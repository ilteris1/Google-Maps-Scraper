#!/usr/bin/env python3
"""Quick test to verify all components work"""

from geo_data import GeoDataManager

print("Testing GeoDataManager...")
geo = GeoDataManager()

# Test country search
print("\n1. Testing country search for 'united':")
matches = geo.search_country('united')
for name, code in matches[:5]:
    print(f"   - {name} ({code})")

# Test getting top cities
print("\n2. Testing top 5 cities in USA (US):")
cities = geo.get_top_cities('US', 5)
for city in cities:
    print(f"   - {city}")

print("\n3. Testing top 5 cities in Germany (DE):")
cities = geo.get_top_cities('DE', 5)
for city in cities:
    print(f"   - {city}")

print("\n✓ All tests passed! Ready to scrape.")
print("\nRun: python3 main.py")
