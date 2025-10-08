import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from config import IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT, SCROLL_PAUSE_TIME, MAX_SCROLL_ATTEMPTS, MAX_PLACES_PER_CITY, CHROME_BINARY_PATH, EXTRACT_WAIT_TIME
import os
import subprocess
import requests
import zipfile
import stat
import shutil

class YandexMapsScraper:
    def __init__(self, headless=True):
        self.driver = self._setup_driver(headless)
    
    def _setup_driver(self, headless):
        options = ChromeOptions()
        if headless:
            options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')
        
        if CHROME_BINARY_PATH and os.path.exists(CHROME_BINARY_PATH):
            options.binary_location = CHROME_BINARY_PATH
        
        driver_path = self._get_chromedriver()
        service = ChromeService(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(IMPLICIT_WAIT)
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        return driver
    
    def _get_chromedriver(self):
        driver_dir = os.path.expanduser('~/.chromedriver')
        driver_path = os.path.join(driver_dir, 'chromedriver')
        
        if os.path.exists(driver_path):
            return driver_path
        
        chrome_path = CHROME_BINARY_PATH or '/usr/bin/google-chrome'
        result = subprocess.run([chrome_path, '--version'], capture_output=True, text=True)
        chrome_version = result.stdout.strip().split()[-1].split('.')[0]
        
        os.makedirs(driver_dir, exist_ok=True)
        
        versions_url = f'https://googlechromelabs.github.io/chrome-for-testing/latest-versions-per-milestone-with-downloads.json'
        response = requests.get(versions_url)
        data = response.json()
        version = data['milestones'][chrome_version]['version']
        
        url = f'https://storage.googleapis.com/chrome-for-testing-public/{version}/linux64/chromedriver-linux64.zip'
        
        zip_path = os.path.join(driver_dir, 'chromedriver.zip')
        response = requests.get(url, stream=True)
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(driver_dir)
        
        extracted_driver = os.path.join(driver_dir, 'chromedriver-linux64', 'chromedriver')
        shutil.move(extracted_driver, driver_path)
        os.chmod(driver_path, stat.S_IRWXU)
        os.remove(zip_path)
        shutil.rmtree(os.path.join(driver_dir, 'chromedriver-linux64'), ignore_errors=True)
        
        return driver_path
    
    def search_places(self, query, city, country):
        search_query = f"{query} {city}"
        url = f"https://yandex.ru/maps/?text={search_query.replace(' ', '+')}"
        
        try:
            self.driver.get(url)
            time.sleep(3)
            self._scroll_results()
            return self._extract_place_links()
        except Exception as e:
            return []
    
    def _scroll_results(self):
        try:
            scrollable = self.driver.find_elements(By.CSS_SELECTOR, 'div[class*="scroll"]')
            if scrollable:
                for _ in range(MAX_SCROLL_ATTEMPTS):
                    self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable[0])
                    time.sleep(SCROLL_PAUSE_TIME)
            else:
                for _ in range(MAX_SCROLL_ATTEMPTS):
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(SCROLL_PAUSE_TIME)
        except Exception as e:
            pass
    
    def _extract_place_links(self):
        links = []
        try:
            selectors = [
                'a[href*="/org/"]',
                'a[href*="maps.yandex"]',
                'div[class*="search-snippet"] a'
            ]
            
            for selector in selectors:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    href = element.get_attribute('href')
                    if href and ('/org/' in href or 'yandex' in href) and href not in links:
                        if '?' in href:
                            href = href.split('?')[0]
                        links.append(href)
            
            if MAX_PLACES_PER_CITY:
                return links[:MAX_PLACES_PER_CITY]
            return links
        except Exception as e:
            return []
    
    def extract_place_data(self, url):
        try:
            self.driver.get(url)
            time.sleep(EXTRACT_WAIT_TIME)
            
            self.driver.execute_script("window.scrollTo(0, 300);")
            time.sleep(0.3)
            
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
            return None
    
    def _safe_extract(self, func):
        try:
            return func()
        except:
            return None
    
    def _get_title(self):
        selectors = ['h1.orgpage-header-view__header', 'h1[class*="title"]']
        for selector in selectors:
            try:
                return self.driver.find_element(By.CSS_SELECTOR, selector).text
            except:
                continue
        return None
    
    def _get_rating(self):
        selectors = ['span[class*="rating-badge"]', 'div[class*="rating"]']
        for selector in selectors:
            try:
                elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                text = elem.text
                if text and any(c.isdigit() for c in text):
                    return text.split()[0]
            except:
                continue
        return None
    
    def _get_reviews(self):
        selectors = ['span[class*="reviews"]', 'a[class*="reviews"]']
        for selector in selectors:
            try:
                elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                text = elem.text
                if text and any(c.isdigit() for c in text):
                    return ''.join(filter(str.isdigit, text))
            except:
                continue
        return None
    
    def _get_category(self):
        selectors = ['div[class*="rubric"]', 'span[class*="category"]']
        for selector in selectors:
            try:
                return self.driver.find_element(By.CSS_SELECTOR, selector).text
            except:
                continue
        return None
    
    def _get_address(self):
        selectors = ['a[class*="address"]', 'div[class*="address"]', 'span[class*="address"]']
        for selector in selectors:
            try:
                elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                text = elem.text
                if text and len(text) > 10:
                    return text
            except:
                continue
        return None
    
    def _get_website(self):
        selectors = ['a[class*="link"][href*="http"]', 'a[class*="website"]']
        for selector in selectors:
            try:
                links = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for link in links:
                    href = link.get_attribute('href')
                    if href and 'yandex' not in href and 'http' in href:
                        return href
            except:
                continue
        return None
    
    def _get_phone(self):
        selectors = ['a[href^="tel:"]', 'span[class*="phone"]', 'div[class*="phone"]']
        for selector in selectors:
            try:
                elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                if selector.startswith('a[href^="tel:"]'):
                    return elem.get_attribute('href').replace('tel:', '')
                text = elem.text
                if text and ('+' in text or any(c.isdigit() for c in text)):
                    return text
            except:
                continue
        return None
    
    def close(self):
        if self.driver:
            self.driver.quit()
