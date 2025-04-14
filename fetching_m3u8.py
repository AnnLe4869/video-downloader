from seleniumwire import webdriver  # This lets us intercept network requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# -------- Configuration --------
CHROMEDRIVER_PATH = './chromedriver.exe'  # Update this!
WAIT_TIME = 5  # Seconds to wait for page activity
# --------------------------------

def extract_m3u8_requests(driver):
    m3u8_urls = set()
    for request in driver.requests:
        if request.response and ".m3u8" in request.url:
            m3u8_urls.add(request.url)
    return list(m3u8_urls)

def fetching_m3u8_requests(url: str):
    options = Options()
    options.add_argument("--headless")  # Run in background
    options.add_argument("--disable-gpu")
    
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    print(f"Loading: {url}")
    driver.get(url)
    
    print(f"Waiting {WAIT_TIME} seconds for network requests...")
    time.sleep(WAIT_TIME)

    m3u8_files = extract_m3u8_requests(driver)
    
    print("\n🎯 Found .m3u8 URLs:")
    for url in m3u8_files:
        print(url)

    driver.quit()
    return m3u8_files
