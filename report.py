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

def generate_report(csv_file):
    df = pd.read_csv(csv_file)
    
    print(f"\n{Fore.YELLOW}Generating HTML report...{Style.RESET_ALL}")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_file = f"report_{csv_file.replace('.csv', '')}_{timestamp}.html"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Business Directory - {csv_file}</title>
        <style>
            @media print {{
                body {{ margin: 0; }}
                table {{ page-break-inside: auto; }}
                tr {{ page-break-inside: avoid; page-break-after: auto; }}
            }}
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .header {{ text-align: center; margin-bottom: 30px; padding: 20px; background: #f8f9fa; border-bottom: 3px solid #333; }}
            .header h1 {{ margin: 0; color: #333; }}
            .header p {{ margin: 5px 0; color: #666; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th {{ background: #333; color: white; padding: 12px 8px; text-align: left; font-size: 12px; border: 1px solid #ddd; }}
            td {{ padding: 10px 8px; border: 1px solid #ddd; font-size: 11px; vertical-align: top; }}
            tr:nth-child(even) {{ background: #f8f9fa; }}
            .rating {{ font-weight: bold; color: #f39c12; }}
            .phone {{ font-weight: bold; color: #27ae60; }}
            .source {{ background: #3498db; color: white; padding: 2px 6px; border-radius: 3px; font-size: 10px; }}
            .source.yandex {{ background: #ff0000; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Business Directory Report</h1>
            <p><strong>Source:</strong> {csv_file}</p>
            <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Total Records:</strong> {len(df)}</p>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Business Name</th>
                    <th>Phone</th>
                    <th>Address</th>
                    <th>City</th>
                    <th>Rating</th>
                    <th>Category</th>
                    <th>Website</th>
                    <th>Source</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for idx, row in df.iterrows():
        title = row.get('title', 'N/A')
        phone = row.get('phone', '-')
        address = row.get('address', '-')
        city = row.get('city', '-')
        category = row.get('category', '-')
        website = row.get('website', '-')
        source = row.get('source', '-')
        
        try:
            rating = float(str(row.get('rating', '0')).replace(',', '.'))
            reviews = row.get('reviews', '0')
            rating_display = f"<span class='rating'>⭐ {rating}</span> ({reviews})"
        except:
            rating_display = '-'
        
        source_class = source.lower() if pd.notna(source) else ''
        
        html += f"""
            <tr>
                <td>{idx + 1}</td>
                <td><strong>{title}</strong></td>
                <td class="phone">{phone}</td>
                <td>{address}</td>
                <td>{city}</td>
                <td>{rating_display}</td>
                <td>{category}</td>
                <td>{website if len(str(website)) < 40 else str(website)[:37] + '...'}</td>
                <td><span class="source {source_class}">{source}</span></td>
            </tr>
        """
    
    html += """
            </tbody>
        </table>
    </body>
    </html>
    """
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n{Fore.GREEN}✓ Report generated: {html_file}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Open in browser and print to PDF (Ctrl+P){Style.RESET_ALL}")

if __name__ == "__main__":
    csv_file = list_csv_files()
    if csv_file:
        generate_report(csv_file)
