import pandas as pd
import glob
from datetime import datetime
from colorama import Fore, Style, init
from tqdm import tqdm
from scraper import GoogleMapsScraper
from yandex_scraper import YandexMapsScraper
from geo_data import GeoDataManager

init(autoreset=True)

def print_banner():
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}  Maps Scraper - Global Edition")
    print(f"{Fore.CYAN}  Google Maps & Yandex Maps | All Countries")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

def select_map_service():
    print(f"{Fore.YELLOW}Select map service:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}1.{Style.RESET_ALL} Google Maps (worldwide)")
    print(f"{Fore.GREEN}2.{Style.RESET_ALL} Yandex Maps (best for Russia/CIS)")
    print(f"{Fore.GREEN}3.{Style.RESET_ALL} Both (Google first, then Yandex)")
    
    while True:
        try:
            choice = int(input(f"\n{Fore.CYAN}Select (1-3): {Style.RESET_ALL}"))
            if choice in [1, 2, 3]:
                return choice
        except ValueError:
            pass
        print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")

def select_country(geo):
    print(f"{Fore.YELLOW}Enter country name (or part of it):{Style.RESET_ALL}")
    query = input(f"{Fore.CYAN}> {Style.RESET_ALL}").strip()
    
    matches = geo.search_country(query)
    
    if not matches:
        print(f"{Fore.RED}No countries found. Try again.{Style.RESET_ALL}")
        return select_country(geo)
    
    if len(matches) == 1:
        print(f"{Fore.GREEN}Selected: {matches[0][0]}{Style.RESET_ALL}")
        return matches[0]
    
    print(f"\n{Fore.YELLOW}Multiple matches found:{Style.RESET_ALL}")
    for idx, (name, code) in enumerate(matches[:20], 1):
        print(f"{Fore.GREEN}{idx}.{Style.RESET_ALL} {name}")
    
    while True:
        try:
            choice = int(input(f"\n{Fore.CYAN}Select (1-{min(len(matches), 20)}): {Style.RESET_ALL}"))
            if 1 <= choice <= min(len(matches), 20):
                return matches[choice - 1]
        except ValueError:
            pass
        print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")

def get_cities_selection(geo, country_code, country_name):
    # Check if US for state selection
    if country_code == 'US':
        print(f"\n{Fore.YELLOW}Location Selection for USA:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1.{Style.RESET_ALL} Select by states")
        print(f"{Fore.GREEN}2.{Style.RESET_ALL} Select by cities")
        
        while True:
            try:
                choice = int(input(f"\n{Fore.CYAN}Select (1-2): {Style.RESET_ALL}"))
                if choice in [1, 2]:
                    break
            except ValueError:
                pass
            print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
        
        if choice == 1:
            return get_state_selection(geo)
    
    print(f"\n{Fore.YELLOW}City Selection:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}1.{Style.RESET_ALL} Enter number of top cities (by population)")
    print(f"{Fore.GREEN}2.{Style.RESET_ALL} Manually select from top 100 cities")
    print(f"{Fore.GREEN}3.{Style.RESET_ALL} All cities in {country_name}")
    
    while True:
        try:
            choice = int(input(f"\n{Fore.CYAN}Select (1-3): {Style.RESET_ALL}"))
            if choice in [1, 2, 3]:
                break
        except ValueError:
            pass
        print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
    
    if choice == 3:
        all_cities = geo.get_all_cities_in_country(country_code)
        print(f"\n{Fore.GREEN}Total cities to scrape: {len(all_cities)}{Style.RESET_ALL}")
        return all_cities
    
    if choice == 1:
        while True:
            try:
                count = int(input(f"\n{Fore.CYAN}How many top cities? (1-200): {Style.RESET_ALL}"))
                if 1 <= count <= 200:
                    return geo.get_top_cities(country_code, count)
                print(f"{Fore.RED}Enter a number between 1 and 200.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
    else:
        top_cities = geo.get_top_cities(country_code, 100)
        if not top_cities:
            print(f"{Fore.RED}No cities found.{Style.RESET_ALL}")
            return []
        
        print(f"\n{Fore.YELLOW}Top 100 cities in {country_name}:{Style.RESET_ALL}")
        for idx, city in enumerate(top_cities, 1):
            print(f"{Fore.GREEN}{idx:2d}.{Style.RESET_ALL} {city}")
        
        print(f"\n{Fore.CYAN}Enter city numbers separated by comma (e.g., 1,3,5,7) or 'all' for all 100:{Style.RESET_ALL}")
        selection = input(f"{Fore.CYAN}> {Style.RESET_ALL}").strip()
        
        if selection.lower() == 'all':
            return top_cities
        
        try:
            indices = [int(x.strip()) for x in selection.split(',')]
            selected = [top_cities[i-1] for i in indices if 1 <= i <= len(top_cities)]
            if selected:
                print(f"\n{Fore.GREEN}Selected {len(selected)} cities{Style.RESET_ALL}")
                return selected
            print(f"{Fore.RED}No valid cities selected.{Style.RESET_ALL}")
            return []
        except:
            print(f"{Fore.RED}Invalid input.{Style.RESET_ALL}")
            return []

def get_state_selection(geo):
    states = [
        'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
        'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
        'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
        'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico',
        'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
        'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
        'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
    ]
    
    print(f"\n{Fore.YELLOW}US States:{Style.RESET_ALL}")
    for idx, state in enumerate(states, 1):
        print(f"{Fore.GREEN}{idx:2d}.{Style.RESET_ALL} {state}")
    
    print(f"\n{Fore.CYAN}Enter state numbers separated by comma (e.g., 1,5,10) or 'all' for all states:{Style.RESET_ALL}")
    selection = input(f"{Fore.CYAN}> {Style.RESET_ALL}").strip()
    
    selected_states = []
    if selection.lower() == 'all':
        selected_states = states
    else:
        try:
            indices = [int(x.strip()) for x in selection.split(',')]
            selected_states = [states[i-1] for i in indices if 1 <= i <= len(states)]
        except:
            print(f"{Fore.RED}Invalid input.{Style.RESET_ALL}")
            return []
    
    if not selected_states:
        print(f"{Fore.RED}No valid states selected.{Style.RESET_ALL}")
        return []
    
    print(f"\n{Fore.GREEN}Selected {len(selected_states)} states{Style.RESET_ALL}")
    
    # Get cities per state
    while True:
        try:
            cities_per_state = int(input(f"\n{Fore.CYAN}How many top cities per state? (1-100, or 0 for all): {Style.RESET_ALL}"))
            if 0 <= cities_per_state <= 100:
                break
            print(f"{Fore.RED}Enter a number between 0 and 100.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
    
    if cities_per_state == 0:
        cities_per_state = 1000  # Get all cities
    
    # Get cities for each state
    all_cities = []
    for state in selected_states:
        state_cities = geo.get_cities_by_state('US', state, cities_per_state)
        print(f"{Fore.CYAN}{state}: {len(state_cities)} cities{Style.RESET_ALL}")
        all_cities.extend(state_cities)
    
    print(f"\n{Fore.GREEN}Total cities to scrape: {len(all_cities)}{Style.RESET_ALL}")
    return all_cities

def get_search_query():
    print(f"\n{Fore.YELLOW}Enter search queries (comma-separated):{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Example: diesel repair shop, diesel mechanic, ремонт дизеля{Style.RESET_ALL}\n")
    
    while True:
        input_text = input(f"{Fore.CYAN}Queries: {Style.RESET_ALL}").strip()
        if input_text:
            queries = [q.strip() for q in input_text.split(',') if q.strip()]
            if queries:
                print(f"\n{Fore.GREEN}✓ {len(queries)} queries entered{Style.RESET_ALL}")
                return queries
        print(f"{Fore.RED}Enter at least one query{Style.RESET_ALL}")

def select_output_format():
    print(f"\n{Fore.YELLOW}Output format:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}1.{Style.RESET_ALL} CSV")
    print(f"{Fore.GREEN}2.{Style.RESET_ALL} JSON")
    print(f"{Fore.GREEN}3.{Style.RESET_ALL} Both")
    
    while True:
        try:
            choice = int(input(f"\n{Fore.CYAN}Select (1-3): {Style.RESET_ALL}"))
            if choice in [1, 2, 3]:
                return choice
        except ValueError:
            pass
        print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")

def group_by_phone(data):
    """Group results by phone number - Yandex rows come after Google rows with same phone"""
    phone_map = {}
    no_phone = []
    
    for item in data:
        phone = item.get('phone')
        if phone:
            if phone not in phone_map:
                phone_map[phone] = []
            phone_map[phone].append(item)
        else:
            no_phone.append(item)
    
    # Sort each phone group: Google first, then Yandex
    result = []
    for phone, items in phone_map.items():
        items.sort(key=lambda x: 0 if x['source'] == 'Google' else 1)
        result.extend(items)
    
    result.extend(no_phone)
    return result

def save_data(data, format_choice, country_name, first_query):
    if not data:
        print(f"{Fore.RED}No data to save.{Style.RESET_ALL}")
        return
    
    df = pd.DataFrame(data)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_country = country_name.replace(' ', '_')[:30]
    safe_query = first_query.replace(' ', '_')[:30]
    
    if format_choice in [1, 3]:
        csv_file = f"{safe_country}_{safe_query}_{timestamp}.csv"
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        print(f"{Fore.GREEN}✓ Saved: {csv_file} ({len(data)} records){Style.RESET_ALL}")
    
    if format_choice in [2, 3]:
        json_file = f"{safe_country}_{safe_query}_{timestamp}.json"
        df.to_json(json_file, orient='records', indent=2, force_ascii=False)
        print(f"{Fore.GREEN}✓ Saved: {json_file} ({len(data)} records){Style.RESET_ALL}")

def select_mode():
    print(f"{Fore.YELLOW}Select mode:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}1.{Style.RESET_ALL} Start new research")
    print(f"{Fore.GREEN}2.{Style.RESET_ALL} Continue from existing CSV")
    
    while True:
        try:
            choice = int(input(f"\n{Fore.CYAN}Select (1-2): {Style.RESET_ALL}"))
            if choice in [1, 2]:
                return choice
        except ValueError:
            pass
        print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")

def load_existing_csv():
    csv_files = glob.glob("*.csv")
    if not csv_files:
        print(f"{Fore.RED}No CSV files found. Starting new research.{Style.RESET_ALL}")
        return None, set(), set()
    
    print(f"\n{Fore.YELLOW}Available CSV files:{Style.RESET_ALL}")
    for idx, file in enumerate(csv_files, 1):
        print(f"{Fore.GREEN}{idx}.{Style.RESET_ALL} {file}")
    
    while True:
        try:
            choice = int(input(f"\n{Fore.CYAN}Select file (1-{len(csv_files)}): {Style.RESET_ALL}"))
            if 1 <= choice <= len(csv_files):
                selected_file = csv_files[choice - 1]
                df = pd.read_csv(selected_file)
                
                # Extract seen businesses and links
                seen_businesses = set()
                seen_links = set()
                
                for _, row in df.iterrows():
                    unique_key = f"{row.get('title', '')}|{row.get('phone', '')}|{row.get('address', '')}"
                    seen_businesses.add(unique_key)
                    if pd.notna(row.get('link')):
                        seen_links.add(row.get('link'))
                
                print(f"\n{Fore.GREEN}✓ Loaded {len(df)} existing records{Style.RESET_ALL}")
                print(f"{Fore.CYAN}New results will be added to this dataset{Style.RESET_ALL}")
                
                return df.to_dict('records'), seen_businesses, seen_links
        except ValueError:
            pass
        print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")

def main():
    print_banner()
    
    mode = select_mode()
    
    if mode == 2:
        existing_data, existing_businesses, existing_links = load_existing_csv()
        if existing_data is None:
            mode = 1
    else:
        existing_data = []
        existing_businesses = set()
        existing_links = set()
    
    map_service = select_map_service()
    
    geo = GeoDataManager()
    
    country_name, country_code = select_country(geo)
    cities = get_cities_selection(geo, country_code, country_name)
    
    if not cities:
        print(f"{Fore.RED}No cities found for {country_name}. Try another country.{Style.RESET_ALL}")
        return
    
    search_queries = get_search_query()
    output_format = select_output_format()
    
    print(f"\n{Fore.YELLOW}Configuration:{Style.RESET_ALL}")
    print(f"Country: {Fore.CYAN}{country_name}{Style.RESET_ALL}")
    print(f"Cities: {Fore.CYAN}{len(cities)} (by population){Style.RESET_ALL}")
    print(f"Queries: {Fore.CYAN}{', '.join(search_queries)}{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}Cities to scrape:{Style.RESET_ALL} {', '.join(cities[:5])}{'...' if len(cities) > 5 else ''}")
    
    input(f"\n{Fore.GREEN}Press Enter to start...{Style.RESET_ALL}")
    
    all_data = existing_data if mode == 2 else []
    seen_businesses = existing_businesses if mode == 2 else set()
    seen_links = set()  # Always track links to skip duplicates across queries
    
    # Determine which scrapers to use
    scrapers_to_use = []
    if map_service == 1:
        scrapers_to_use = [('Google', GoogleMapsScraper)]
    elif map_service == 2:
        scrapers_to_use = [('Yandex', YandexMapsScraper)]
    else:  # Both
        scrapers_to_use = [('Google', GoogleMapsScraper), ('Yandex', YandexMapsScraper)]
    
    try:
        for service_name, ScraperClass in scrapers_to_use:
            print(f"\n{Fore.CYAN}{'='*60}")
            print(f"{Fore.CYAN}Starting {service_name} Maps scraping...")
            print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
            
            scraper = ScraperClass(headless=True)
            
            try:
                for city in tqdm(cities, desc=f"{service_name} Cities", colour="green"):
                    for search_query in search_queries:
                        print(f"\n{Fore.CYAN}[{service_name}] Scraping: {city}, {country_name} - '{search_query}'{Style.RESET_ALL}")
                        
                        place_links = scraper.search_places(search_query, city, country_name)
                        if seen_links is not None:
                            new_links = [link for link in place_links if link not in seen_links]
                        else:
                            new_links = place_links
                        print(f"Found {len(place_links)} places, {len(new_links)} new")
                        
                        new_count = 0
                        for link in tqdm(new_links, desc=f"{city}", leave=False, colour="blue"):
                            if seen_links is not None:
                                seen_links.add(link)
                            
                            if service_name == 'Yandex':
                                place_data = scraper.extract_place_data(link, city=city, country=country_name)
                            else:
                                place_data = scraper.extract_place_data(link)
                            
                            if place_data:
                                unique_key = f"{place_data.get('title', '')}|{place_data.get('phone', '')}|{place_data.get('address', '')}"
                                
                                if unique_key not in seen_businesses:
                                    place_data['city'] = city
                                    place_data['country'] = country_name
                                    place_data['search_query'] = search_query
                                    place_data['source'] = service_name
                                    all_data.append(place_data)
                                    seen_businesses.add(unique_key)
                                    new_count += 1
                                
                                if len(all_data) % 50 == 0:
                                    save_data(all_data, output_format, country_name, search_queries[0])
                                    print(f"\n{Fore.YELLOW}Auto-saved {len(all_data)} records{Style.RESET_ALL}")
                        
                        print(f"{Fore.GREEN}Added {new_count} new businesses{Style.RESET_ALL}")
            finally:
                scraper.close()
                print(f"\n{Fore.GREEN}✓ {service_name} completed! Total so far: {len(all_data)}{Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}✓ All scraping completed!{Style.RESET_ALL}")
        print(f"Total places: {Fore.CYAN}{len(all_data)}{Style.RESET_ALL}")
        
        # If Both option, group by phone number
        if map_service == 3:
            all_data = group_by_phone(all_data)
            print(f"{Fore.YELLOW}Grouped by phone number{Style.RESET_ALL}")
        
        save_data(all_data, output_format, country_name, search_queries[0])
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Interrupted. Saving collected data...{Style.RESET_ALL}")
        if all_data:
            save_data(all_data, output_format, country_name, search_queries[0])
    except Exception as e:
        print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")
        if all_data:
            save_data(all_data, output_format, country_name, search_queries[0])

if __name__ == "__main__":
    main()
