import shutil
import time , random

from random_headers import get_random_User_Agent

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# wrote these functions with the help of AI, it checks if any of common browsers are installed
def is_chrome_installed() -> bool:
    names = ["google-chrome", "chrome", "chromium", "chromium-browser"]
    return any(shutil.which(name) for name in names)

def is_firefox_installed() -> bool:
    names = ["firefox", "firefox-developer-edition", "firefox-nightly"]
    return any(shutil.which(name) for name in names)

def is_edge_installed() -> bool:
    names = ["microsoft-edge", "edge", "microsoft-edge-dev", "microsoft-edge-beta", "microsoft-edge-canary"]
    return any(shutil.which(name) for name in names)


# Check for installed browsers and set up the WebDriver accordingly, with fallback to mirror URLs for ChromeDriver if installation fails

chrome_mirrors = [
    "https://registry.npmmirror.com/-/binary/chromedriver", 
    "https://npmmirror.com/mirrors/chromedriver",
    "https://cdn.npmmirror.com/binaries/chromedriver",
    "https://registry.npmmirror.com/-/binary/chrome-for-testing", 
]
firefox_mirrors = [
    "https://registry.npmmirror.com/-/binary/geckodriver",
    "https://sourceforge.net/projects/geckodriver.mirror/files",
]
edge_mirrors = [
    "https://registry.npmmirror.com/-/binary/edgedriver",
    "https://npmmirror.com/mirrors/edgedriver",
    "https://mirrors.huaweicloud.com/edgedriver",
]

# args for driver options 
chrome_args = [
    # "--headless=new",                        # Modern headless mode
    "--window-size=1920,1080",               
    "--no-sandbox",                          # Often required in containers/Linux
    "--disable-dev-shm-usage",               # Memory stability in restricted envs
    "--disable-gpu",                         
    "--disable-software-rasterizer",
    "--disable-blink-features=AutomationControlled",  # Reduce basic bot detection
    "--force-device-scale-factor=0.4",                                                   # this one zoomes out 
    f"user-agent={get_random_User_Agent()}",
]
firefox_args = [
    "--headless",             
    "--width=1920",
    "--height=1080",          
]
edge_args = [
    # "--headless=new",                        
    "--window-size=1920,1080",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    "--disable-software-rasterizer",
    "--disable-blink-features=AutomationControlled",
    "--force-device-scale-factor=0.4",
    f"user-agent={get_random_User_Agent()}",
]

driver = None
def setup_webdriver():
    if is_chrome_installed():
        #add options :
        options = ChromeOptions()
        for arg in chrome_args:
            options.add_argument(arg)
        
        for mirror_url in chrome_mirrors:
            # install the driver via the default method first, if it fails, try the mirror urls
            try:
                driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
                break  # Stop on first success
            except Exception:
                service = ChromeService(ChromeDriverManager(url=mirror_url).install())
                driver = webdriver.Chrome(service=service)
                break 
            except Exception:
                continue  # Try the next mirror if this one fails
    
    elif is_firefox_installed():
        options = FirefoxOptions()
        for arg in chrome_args:
            options.add_argument(arg)
    
        for mirror_url in firefox_mirrors:
            try:
                driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
                break
            except Exception:
                service = FirefoxService(GeckoDriverManager(url=mirror_url).install())
                driver = webdriver.Firefox(service=service, options=options)
                break
            except Exception:
                continue

    elif is_edge_installed():
        options = EdgeOptions()
        for arg in chrome_args:
            options.add_argument(arg)

        for mirror_url in edge_mirrors:
            try:
                driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
                break
            except Exception:
                service = EdgeService(EdgeChromiumDriverManager(url=mirror_url).install())
                driver = webdriver.Edge(service=service, options=options)
                break
            except Exception:
                continue
    return driver

def scrape_links_divar(url):
    
    driver = setup_webdriver()
    driver.get(url)

    # Wait until at least some cards are loaded
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "kt-post-card__action")))

    links_set = set() 
    for _ in range(20) :
        driver.execute_script("window.scrollBy(0, 1600);")
        time.sleep(random.uniform(1.2, 2.8))

        try:
            elements = driver.find_elements(By.CLASS_NAME, 'kt-post-card__action')
            for element in elements:
                href = element.get_attribute('href')
                links_set.add(href)
        except Exception as e :
            print(e)

    driver.quit()
    return list(links_set)

if __name__ == "__main__":
    test_links = scrape_links_divar("https://divar.ir/s/iran/auto")
    print(f"Total links scraped: {len(test_links)}")
    # send it to data base