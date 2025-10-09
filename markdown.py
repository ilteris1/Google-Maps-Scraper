import pandas as pd
import glob
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

def list_csv_files():
    csv_files = glob.glob("*.csv")
    if not csv_files:
        print(f"{Fore.RED}No CSV files found in current directory.{Style.RESET_ALL}")
        return None
    
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}  Available CSV Files")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    for idx, file in enumerate(csv_files, 1):
        print(f"{Fore.GREEN}{idx}.{Style.RESET_ALL} {file}")
    
    while True:
        try:
            choice = int(input(f"\n{Fore.CYAN}Select file (1-{len(csv_files)}): {Style.RESET_ALL}"))
            if 1 <= choice <= len(csv_files):
                return csv_files[choice - 1]
        except ValueError:
            pass
        print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")

def generate_markdown(csv_file):
    df = pd.read_csv(csv_file)
    
    print(f"\n{Fore.YELLOW}Select language for labels:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}1.{Style.RESET_ALL} English")
    print(f"{Fore.GREEN}2.{Style.RESET_ALL} Turkish")
    
    while True:
        try:
            lang_choice = int(input(f"\n{Fore.CYAN}Select (1-2): {Style.RESET_ALL}"))
            if lang_choice in [1, 2]:
                break
        except ValueError:
            pass
        print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
    
    if lang_choice == 1:
        labels = {
            'header': '# 📋 Business Directory',
            'source': 'Source',
            'generated': 'Generated',
            'total': 'Total Records',
            'rating': 'Rating',
            'reviews': 'reviews',
            'category': 'Category',
            'phone': 'Phone',
            'address': 'Address',
            'city': 'City',
            'website': 'Website',
            'map': 'Map',
            'view_map': 'View on Map',
            'source_label': 'Source'
        }
    else:
        labels = {
            'header': '# 📋 İşletme Rehberi',
            'source': 'Kaynak',
            'generated': 'Oluşturulma',
            'total': 'Toplam Kayıt',
            'rating': 'Değerlendirme',
            'reviews': 'yorum',
            'category': 'Kategori',
            'phone': 'Telefon',
            'address': 'Adres',
            'city': 'Şehir',
            'website': 'Web Sitesi',
            'map': 'Harita',
            'view_map': 'Haritada Görüntüle',
            'source_label': 'Kaynak'
        }
    
    print(f"\n{Fore.YELLOW}Generating Markdown file...{Style.RESET_ALL}")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    md_file = f"report_{csv_file.replace('.csv', '')}_{timestamp}.md"
    
    with open(md_file, 'w', encoding='utf-8') as f:
        # Header
        f.write(f"{labels['header']}\n\n")
        f.write(f"**{labels['source']}:** {csv_file}  \n")
        f.write(f"**{labels['generated']}:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
        f.write(f"**{labels['total']}:** {len(df)}\n\n")
        f.write("---\n\n")
        
        # Business listings
        for idx, row in df.iterrows():
            f.write(f"## {idx + 1}. {row.get('title', 'N/A')}\n\n")
            
            # Rating
            try:
                rating = float(str(row.get('rating', '0')).replace(',', '.'))
                reviews = row.get('reviews', '0')
                f.write(f"⭐ **{labels['rating']}:** {rating} ({reviews} {labels['reviews']})  \n")
            except:
                pass
            
            # Category
            if pd.notna(row.get('category')):
                f.write(f"📂 **{labels['category']}:** {row.get('category')}  \n")
            
            # Phone
            if pd.notna(row.get('phone')):
                f.write(f"📞 **{labels['phone']}:** {row.get('phone')}  \n")
            
            # Address
            if pd.notna(row.get('address')):
                f.write(f"📍 **{labels['address']}:** {row.get('address')}  \n")
            
            # City
            if pd.notna(row.get('city')):
                f.write(f"🏙️ **{labels['city']}:** {row.get('city')}, {row.get('country', '')}  \n")
            
            # Website
            if pd.notna(row.get('website')):
                f.write(f"🌐 **{labels['website']}:** [{row.get('website')}]({row.get('website')})  \n")
            
            # Map Link
            if pd.notna(row.get('link')):
                f.write(f"🗺️ **{labels['map']}:** [{labels['view_map']}]({row.get('link')})  \n")
            
            # Source
            if pd.notna(row.get('source')):
                f.write(f"🔍 **{labels['source_label']}:** {row.get('source')}  \n")
            
            f.write("\n---\n\n")
    
    print(f"\n{Fore.GREEN}✓ Markdown generated: {md_file}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Open with any markdown viewer or GitHub{Style.RESET_ALL}")

if __name__ == "__main__":
    csv_file = list_csv_files()
    if csv_file:
        generate_markdown(csv_file)
