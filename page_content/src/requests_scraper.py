import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs

class RequestScraper:
    def __init__(self, proxies=None):
        self.ua = UserAgent()
        self.proxies = proxies

    def get_session(self):
        session = requests.Session()
        session.headers.update({"User-Agent": self.ua.chrome})
        if self.proxies:
            session.proxies.update(self.proxies)
        return session

    def get_html(self, url):
        try:
            session = self.get_session()
            response = session.get(url, verify=False)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def check_captcha(self, html):
        soup = bs(html, 'html.parser')
        if soup.find(text=lambda t: 'captcha' in t.lower()):
            return True
        return False

    def scrape(self, url):
        html = self.get_html(url)
        if html:
            if self.check_captcha(html):
                print("Captcha detected. Unable to scrape the page.")
                return None
            return html
        return None
