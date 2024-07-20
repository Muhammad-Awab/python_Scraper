from flask import Flask, jsonify, request
import logging
from page_html import WEBCONTENT
from requests_scraper import RequestScraper

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# ScraperAPI key
SCRAPERAPI_KEY = 'c155a579d27cfd4e381ea719081dfe02'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/page_content', methods=['GET'])
def page_content():
    link = request.args.get('url')
    proxies = {
        'http': f'http://scraperapi:{SCRAPERAPI_KEY}@proxy-server.scraperapi.com:8001',
        'https': f'http://scraperapi:{SCRAPERAPI_KEY}@proxy-server.scraperapi.com:8001'
    }

    try:
        scraper = RequestScraper(proxies={})
        html_content = scraper.scrape(link)
    except Exception as e:
        logger.error(f"Error during initial scraping attempt: {e}")
        html_content = ""

    if html_content:
        logger.info("Requests page successfully scraped. HTML content retrieved.")
    else:
        logger.info("Requests failed to scrape the page or captcha detected, trying with proxy")
        try:
            scraper = RequestScraper(proxies=proxies)
            html_content = scraper.scrape(link)
        except Exception as e:
            logger.error(f"Error during scraping with proxy: {e}")
            html_content = ""

    if not html_content:
        logger.info("Requests failed to scrape the page or captcha detected, trying with Selenium")
        try:
            web_content = WEBCONTENT(link, proxies={})
            html_content = web_content.parse()

            if html_content:
                logger.info("Selenium page successfully scraped. HTML content retrieved.")
            else:
                logger.info("Requests failed to scrape the page or captcha detected, trying selenium with proxy")
                web_content = WEBCONTENT(link, proxies=proxies)
                html_content = web_content.parse()
        except Exception as e:
            logger.error(f"Error during Selenium scraping: {e}")
            html_content = ""

    if not html_content:
        html_content = "Error"

    return jsonify({"Response": html_content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9190)
