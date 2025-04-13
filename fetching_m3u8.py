from seleniumwire import webdriver  # Intercepts network traffic
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time

# -------- Configuration --------
GECKODRIVER_PATH = './geckodriver.exe'  # Update this!
TARGET_URL = 'https://www.miruro.tv/watch?id=153518&ep=1'  # Replace with your target site
WAIT_TIME = 10  # Wait for this many seconds after page load
# --------------------------------

def get_m3u8_requests(driver):
    m3u8_urls = set()
    for request in driver.requests:
        if request.response and ".m3u8" in request.url:
            m3u8_urls.add(request.url)
    return list(m3u8_urls)

def main():
    options = Options()
    options.headless = True  # Run in headless mode

    service = Service(executable_path=GECKODRIVER_PATH)
    driver = webdriver.Firefox(service=service, options=options)

    print(f"Loading: {TARGET_URL}")
    driver.get(TARGET_URL)

    print(f"Waiting {WAIT_TIME} seconds for network requests...")
    time.sleep(WAIT_TIME)

    m3u8_files = get_m3u8_requests(driver)

    print("\n🎯 Found .m3u8 URLs:")
    for url in m3u8_files:
        print(url)

    driver.quit()

if __name__ == "__main__":
    main()
