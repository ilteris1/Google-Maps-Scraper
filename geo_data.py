import pycountry
from geonamescache import GeonamesCache

class GeoDataManager:
    def __init__(self):
        self.gc = GeonamesCache()
        
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
