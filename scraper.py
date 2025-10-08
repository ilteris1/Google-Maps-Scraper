import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import requests
import zipfile
import stat
from config import IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT, SCROLL_PAUSE_TIME, MAX_SCROLL_ATTEMPTS, CHROME_BINARY_PATH, MAX_PLACES_PER_CITY, EXTRACT_WAIT_TIME

class GoogleMapsScraper:
    def __init__(self, headless=True, browser='auto'):
        self.driver = self._setup_driver(headless, browser)
        
    def _setup_driver(self, headless, browser):
        if browser == 'auto':
            try:
                return self._setup_chrome(headless)
            except:
                try:
                    return self._setup_firefox(headless)
                except:
                    raise Exception("No browser found. Install Chrome or Firefox.")
        elif browser == 'chrome':
            return self._setup_chrome(headless)
        elif browser == 'firefox':
            return self._setup_firefox(headless)
    
    def _setup_chrome(self, headless):
        import os
        import subprocess
        options = ChromeOptions()
        if headless:
            options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-images')
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})
        
        if CHROME_BINARY_PATH and os.path.exists(CHROME_BINARY_PATH):
            options.binary_location = CHROME_BINARY_PATH
        
        driver_path = self._get_chromedriver()
        service = ChromeService(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(IMPLICIT_WAIT)
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        return driver
    
    def _get_chromedriver(self):
        import os
        import subprocess
        import shutil
        import platform
        
        is_windows = platform.system() == 'Windows'
        driver_dir = os.path.expanduser('~/.chromedriver')
        driver_name = 'chromedriver.exe' if is_windows else 'chromedriver'
        driver_path = os.path.join(driver_dir, driver_name)
        
        # Get Chrome version
        if is_windows:
            chrome_paths = [
                'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
                'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
                os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe')
            ]
            chrome_path = next((p for p in chrome_paths if os.path.exists(p)), chrome_paths[0])
        else:
            chrome_path = CHROME_BINARY_PATH or '/usr/bin/google-chrome'
        
        result = subprocess.run([chrome_path, '--version'], capture_output=True, text=True)
        chrome_version = result.stdout.strip().split()[-1].split('.')[0]
        
        # Check if we have the right driver
        if os.path.exists(driver_path):
            result = subprocess.run([driver_path, '--version'], capture_output=True, text=True)
            if chrome_version in result.stdout:
                return driver_path
            os.remove(driver_path)
        
        os.makedirs(driver_dir, exist_ok=True)
        
        # Get latest version for this major version
        versions_url = f'https://googlechromelabs.github.io/chrome-for-testing/latest-versions-per-milestone-with-downloads.json'
        response = requests.get(versions_url)
        data = response.json()
        version = data['milestones'][chrome_version]['version']
        
        # Download for correct platform
        if is_windows:
            url = f'https://storage.googleapis.com/chrome-for-testing-public/{version}/win64/chromedriver-win64.zip'
            folder_name = 'chromedriver-win64'
        else:
            url = f'https://storage.googleapis.com/chrome-for-testing-public/{version}/linux64/chromedriver-linux64.zip'
            folder_name = 'chromedriver-linux64'
        
        zip_path = os.path.join(driver_dir, 'chromedriver.zip')
        response = requests.get(url, stream=True)
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(driver_dir)
        
        extracted_driver = os.path.join(driver_dir, folder_name, driver_name)
        shutil.move(extracted_driver, driver_path)
        if not is_windows:
            os.chmod(driver_path, stat.S_IRWXU)
        os.remove(zip_path)
        shutil.rmtree(os.path.join(driver_dir, folder_name), ignore_errors=True)
        
        return driver_path
    
    def _setup_firefox(self, headless):
        raise Exception("Firefox not supported. Use Chrome.")
    
    def search_places(self, query, city, country):
        search_query = f"{query} in {city}, {country}"
        url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
        
        try:
            self.driver.get(url)
            time.sleep(1.5)
            self._scroll_results()
            links = self._extract_place_links()
            if MAX_PLACES_PER_CITY:
                return links[:MAX_PLACES_PER_CITY]
            return links
        except Exception as e:
            return []
    
    def _scroll_results(self):
        try:
            scrollable_div = self.driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
            last_height = self.driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
            
            for _ in range(MAX_SCROLL_ATTEMPTS):
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
                time.sleep(SCROLL_PAUSE_TIME)
                new_height = self.driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
                
                if new_height == last_height:
                    break
                last_height = new_height
        except Exception as e:
            print(f"Scroll error: {e}")
    
    def _extract_place_links(self):
        links = []
        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*="/maps/place/"]')
            for element in elements:
                href = element.get_attribute('href')
                if href and '/maps/place/' in href and href not in links:
                    links.append(href)
        except Exception as e:
            print(f"Error extracting links: {e}")
        return links
    
    def extract_place_data(self, url):
        max_retries = 2
        for attempt in range(max_retries):
            try:
                self.driver.get(url)
                time.sleep(EXTRACT_WAIT_TIME)
                
                try:
                    self.driver.execute_script("window.scrollTo(0, 300);")
                    time.sleep(0.3)
                except:
                    pass
                
                data = {
                    'title': self._safe_extract(self._get_title),
                    'rating': self._safe_extract(self._get_rating),
                    'reviews': self._safe_extract(self._get_reviews),
                    'category': self._safe_extract(self._get_category),
                    'address': self._safe_extract(self._get_address),
                    'website': self._safe_extract(self._get_website),
                    'phone': self._safe_extract(self._get_phone),
                    'link': url
                }
                return data
            except Exception as e:
                if 'tab crashed' in str(e) or 'session' in str(e).lower():
                    if attempt < max_retries - 1:
                        print(f"Tab crashed, restarting browser...")
                        self._restart_driver()
                        time.sleep(2)
                        continue
                return None
        return None
    
    def _restart_driver(self):
        try:
            self.driver.quit()
        except:
            pass
        time.sleep(1)
        self.driver = self._setup_driver(True, 'chrome')
    
    def _safe_extract(self, func):
        try:
            return func()
        except:
            return None
    
    def _get_title(self):
        return self.driver.find_element(By.CSS_SELECTOR, 'h1.DUwDvf').text
    
    def _get_rating(self):
        rating_elem = self.driver.find_element(By.CSS_SELECTOR, 'div.F7nice span[aria-hidden="true"]')
        return rating_elem.text
    
    def _get_reviews(self):
        reviews_elem = self.driver.find_element(By.CSS_SELECTOR, 'div.F7nice span[aria-label*="reviews"]')
        aria_label = reviews_elem.get_attribute('aria-label')
        return aria_label.split()[0].replace(',', '')
    
    def _get_category(self):
        return self.driver.find_element(By.CSS_SELECTOR, 'button.DkEaL').text
    
    def _get_address(self):
        # Try multiple selectors
        selectors = [
            'button[data-item-id="address"]',
            'button[data-tooltip="Copy address"]',
            '[data-item-id="address"] div.fontBodyMedium'
        ]
        
        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for elem in elements:
                    aria_label = elem.get_attribute('aria-label')
                    if aria_label:
                        if 'Address:' in aria_label:
                            return aria_label.replace('Address:', '').strip()
                        if 'Adres:' in aria_label:
                            return aria_label.replace('Adres:', '').strip()
                    text = elem.text
                    if text and len(text) > 10:
                        return text
            except:
                continue
        return None
    
    def _get_website(self):
        selectors = [
            'a[data-item-id="authority"]',
            'a[data-tooltip="Open website"]',
            'a[aria-label*="Website"]',
            'a[aria-label*="İnternet sitesi"]'
        ]
        
        for selector in selectors:
            try:
                links = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for link in links:
                    href = link.get_attribute('href')
                    if href and 'google.com' not in href:
                        return href
            except:
                continue
        return None
    
    def _get_phone(self):
        selectors = [
            'button[data-item-id*="phone"]',
            'button[data-tooltip="Copy phone number"]',
            '[data-item-id*="phone"] div.fontBodyMedium',
            'button[aria-label*="Phone"]',
            'button[aria-label*="Telefon"]'
        ]
        
        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for elem in elements:
                    aria_label = elem.get_attribute('aria-label')
                    if aria_label:
                        if 'Phone:' in aria_label:
                            return aria_label.replace('Phone:', '').strip()
                        if 'Telefon:' in aria_label:
                            return aria_label.replace('Telefon:', '').strip()
                    text = elem.text
                    if text and ('+' in text or text.replace(' ', '').replace('-', '').isdigit()):
                        return text
            except:
                continue
        return None
    
    def close(self):
        if self.driver:
            self.driver.quit()
