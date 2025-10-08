import pandas as pd
from datetime import datetime
from colorama import Fore, Style, init
from tqdm import tqdm
from scraper import GoogleMapsScraper
from geo_data import GeoDataManager

init(autoreset=True)

def print_banner():
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}  Google Maps Scraper - Global Edition")
    print(f"{Fore.CYAN}  All Countries | Population-Based Cities | Custom Queries")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

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

def get_city_count():
    while True:
        try:
            count = int(input(f"\n{Fore.CYAN}How many top cities to scrape? (1-100): {Style.RESET_ALL}"))
            if 1 <= count <= 100:
                return count
            print(f"{Fore.RED}Enter a number between 1 and 100.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")

def get_search_query():
    print(f"\n{Fore.YELLOW}Enter search queries in ANY language (one per line):{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Tip: Use broad terms. Example for diesel services:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  - auto repair{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  - автосервис{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  - truck repair{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  - ремонт грузовиков{Style.RESET_ALL}\n")
    
    queries = []
    while True:
        query = input(f"{Fore.CYAN}Query {len(queries)+1} (or Enter to finish): {Style.RESET_ALL}").strip()
        if not query:
            if queries:
                break
            print(f"{Fore.RED}Enter at least one query{Style.RESET_ALL}")
            continue
        queries.append(query)
    
    return queries

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

def save_data(data, format_choice, country_name, search_query):
    if not data:
        print(f"{Fore.RED}No data to save.{Style.RESET_ALL}")
        return
    
    df = pd.DataFrame(data)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_country = country_name.replace(' ', '_')
    safe_query = search_query.replace(' ', '_')
    
    if format_choice in [1, 3]:
        csv_file = f"{safe_country}_{safe_query}_{timestamp}.csv"
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        print(f"{Fore.GREEN}✓ Saved: {csv_file}{Style.RESET_ALL}")
    
    if format_choice in [2, 3]:
        json_file = f"{safe_country}_{safe_query}_{timestamp}.json"
        df.to_json(json_file, orient='records', indent=2, force_ascii=False)
        print(f"{Fore.GREEN}✓ Saved: {json_file}{Style.RESET_ALL}")

def main():
    print_banner()
    
    geo = GeoDataManager()
    
    country_name, country_code = select_country(geo)
    city_count = get_city_count()
    
    cities = geo.get_top_cities(country_code, city_count)
    
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
    
    scraper = GoogleMapsScraper(headless=True)
    all_data = []
    seen_links = set()
    
    try:
        for city in tqdm(cities, desc="Cities", colour="green"):
            for search_query in search_queries:
                print(f"\n{Fore.CYAN}Scraping: {city}, {country_name} - '{search_query}'{Style.RESET_ALL}")
                
                place_links = scraper.search_places(search_query, city, country_name)
                new_links = [link for link in place_links if link not in seen_links]
                print(f"Found {len(new_links)} new places")
                
                for link in tqdm(new_links, desc=f"{city}", leave=False, colour="blue"):
                    place_data = scraper.extract_place_data(link)
                    if place_data:
                        place_data['city'] = city
                        place_data['country'] = country_name
                        place_data['search_query'] = search_query
                        all_data.append(place_data)
                        seen_links.add(link)
        
        print(f"\n{Fore.GREEN}✓ Completed!{Style.RESET_ALL}")
        print(f"Total places: {Fore.CYAN}{len(all_data)}{Style.RESET_ALL}")
        
        save_data(all_data, output_format, country_name, '_'.join(search_queries))
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Interrupted. Saving collected data...{Style.RESET_ALL}")
        if all_data:
            save_data(all_data, output_format, country_name, '_'.join(search_queries))
    except Exception as e:
        print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")
        if all_data:
            save_data(all_data, output_format, country_name, '_'.join(search_queries))
    finally:
        scraper.close()

if __name__ == "__main__":
    main()
