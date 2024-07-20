import undetected_chromedriver as uc
from fake_useragent import UserAgent
import time
import random
from bs4 import BeautifulSoup as bs


class WEBCONTENT:

    def __init__(self, link, proxies):
        self.ua = UserAgent()
        self.options = uc.ChromeOptions()
        if proxies:
            self.options.add_argument(f"--proxy-server={proxies['http']}")
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = uc.Chrome(options=self.options, version_main = 113)
        self.url = link

    def check_captcha(self, html):
        soup = bs(html, 'html.parser')
        if soup.find(text=lambda t: 'captcha' in t.lower()):
            return True
        return False
            
    def parse(self):
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride',
                                    {"userAgent": '{0}'.format(self.ua.chrome)})
        
        self.driver.get(self.url)
        
        time.sleep(random.randint(4, 7))
        
        page_source = self.driver.page_source

        if page_source:
            if self.check_captcha(page_source):
                print("Captcha detected. Unable to scrape the page.")

                page_source = None

        self.driver.quit()

        return page_source
