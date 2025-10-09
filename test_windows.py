import platform
print(f"OS: {platform.system()}")

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time
    
    print("Setting up Chrome...")
    options = ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    driver = webdriver.Chrome(options=options)
    print("Chrome started successfully!")
    
    print("Loading Google Maps...")
    driver.get("https://www.google.com/maps/search/restaurants+in+New+York")
    
    print("Waiting for page to load...")
    time.sleep(5)
    
    print("Looking for results feed...")
    try:
        wait = WebDriverWait(driver, 15)
        feed = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]')))
        print(f"✓ Found feed element!")
        
        links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/maps/place/"]')
        print(f"✓ Found {len(links)} place links")
        
        if links:
            print(f"First link: {links[0].get_attribute('href')[:100]}")
    except Exception as e:
        print(f"✗ Error: {e}")
        print(f"Current URL: {driver.current_url}")
        print(f"Page title: {driver.title}")
    
    input("Press Enter to close browser...")
    driver.quit()
    print("Test completed!")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
