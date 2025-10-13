import pycountry
from geonamescache import GeonamesCache
import pgeocode
import pandas as pd

class GeoDataManager:
    def __init__(self):
        self.gc = GeonamesCache()
        self.us_nomi = None
        
    def get_all_countries(self):
        """Get all countries sorted alphabetically"""
        countries = [(c.name, c.alpha_2) for c in pycountry.countries]
        return sorted(countries, key=lambda x: x[0])
    
    def get_top_cities(self, country_code, limit=10):
        """Get top N cities by population for a country"""
        cities = self.gc.get_cities()
        country_cities = []
        
        for city_id, city_data in cities.items():
            if city_data['countrycode'] == country_code:
                country_cities.append({
                    'name': city_data['name'],
                    'population': city_data.get('population', 0)
                })
        
        # Sort by population and return top N
        country_cities.sort(key=lambda x: x['population'], reverse=True)
        return [city['name'] for city in country_cities[:limit]]
    
    def search_country(self, query):
        """Search for countries by name"""
        query = query.lower()
        countries = self.get_all_countries()
        return [(name, code) for name, code in countries if query in name.lower()]
    
    def get_cities_by_state(self, country_code, state_name, limit=50):
        """Get all cities for a US state using geonamescache"""
        if country_code != 'US':
            return []
        
        state_codes = {
            'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
            'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
            'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
            'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
            'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
            'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH',
            'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND',
            'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI',
            'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
            'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
            'Wisconsin': 'WI', 'Wyoming': 'WY'
        }
        
        state_code = state_codes.get(state_name)
        if not state_code:
            return []
        
        cities = self.gc.get_cities()
        state_cities = []
        
        for city_data in cities.values():
            if city_data['countrycode'] == 'US' and city_data.get('admin1code') == state_code:
                state_cities.append({
                    'name': city_data['name'],
                    'population': city_data.get('population', 0)
                })
        
        state_cities.sort(key=lambda x: x['population'], reverse=True)
        return [city['name'] for city in state_cities[:limit]]
