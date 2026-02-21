import time ,random ,threading
from tqdm import tqdm
from browser_instaled_check import *

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

def get_driver_options(browser: str):
    user_agent = get_random_User_Agent()
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")           # Modern headless (less detectable)
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"--user-agent={user_agent}")
        return options

    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        # i need to find a way to add user-agents to firefox options 
        return options

    elif browser == "edge":
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")        
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"--user-agent={user_agent}")
        return options
    

driver = None
def setup_webdriver(driver=str):
    if driver == "chrome" :
        try:
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=get_driver_options("chrome")) 
        except Exception:
            for mirror_url in chrome_mirrors:
                service = ChromeService(ChromeDriverManager(url=mirror_url).install())
                driver = webdriver.Chrome(service=service,options=get_driver_options("chrome"))

                if driver != None :
                    break
        except:
            pass

    elif driver == "firefox":
        for mirror_url in firefox_mirrors:
            try:
                driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=get_driver_options("firefox"))
                break
            except Exception:
                service = FirefoxService(GeckoDriverManager(url=mirror_url).install())
                driver = webdriver.Firefox(service=service, options=get_driver_options("firefox"))
                break
            except Exception:
                continue

    elif driver == "edge":
        for mirror_url in edge_mirrors:
            try:
                driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=get_driver_options("edge"))
                break
            except Exception:
                service = EdgeService(EdgeChromiumDriverManager(url=mirror_url).install())
                driver = webdriver.Edge(service=service, options=get_driver_options("edge"))
                break
            except Exception:
                continue
    return driver

def scrape_links_divar(url):
    
    if is_chrome_installed() :
        browser = "chrome"
    elif is_firefox_installed :
        browser = "firefox"
    elif is_edge_installed :
        browser = "edge"
    
    driver = setup_webdriver(browser)
    driver.get(url)

    # Wait until at least some cards are loaded
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "kt-post-card__action")))

    links_set = set() 
    for _ in range(40) :
        driver.execute_script("window.scrollBy(0, 1600);")
        time.sleep(random.uniform(1.2, 2.8))

        try:
            elements = driver.find_elements(By.CLASS_NAME, 'kt-post-card__action')
            for element in elements:
                href = element.get_attribute('href')
                links_set.add(href)
        except Exception as e :
            print(e)
        
        try:
            button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/main/div[2]/div[2]/div/button"))
            )
            button.click()
        except:
            pass

        if len(links_set) >= 800 :
            break

    driver.quit()
    return list(links_set)

def background_timer(duration, stop_event):
    """Runs a progress bar in background until duration or stop_event is set."""
    with tqdm(total=duration, desc="scraping links(it takes about 3 minutes)", unit="s") as pbar:
        for i in range(duration):
            if stop_event.is_set():      
                pbar.update(duration - i)    # Fill the bar to 100%
                break
            time.sleep(1)
            pbar.update(1)



if __name__ == "__main__":
    
    script_start = time.time()
    stop_event = threading.Event()

    progress_thread = threading.Thread(target=background_timer, args=(300, stop_event))
    progress_thread.start()

    test_links = scrape_links_divar("https://divar.ir/s/iran/auto")
    stop_event.set()

    progress_thread.join()
    script_end = time.time()
    execution_time = script_end - script_start

    print(f"Script completed in {execution_time:.2f} seconds")
    print(f"Total links scraped: {len(test_links)}")
    
    # send it to data base