import requests
import time

# Replace with your ScraperAPI key
SCRAPERAPI_KEY = 'c155a579d27cfd4e381ea719081dfe02'

# ScraperAPI proxy URL
SCRAPERAPI_PROXY = f"http://scraperapi:{SCRAPERAPI_KEY}@proxy-server.scraperapi.com:8001"

# Function to get the IP address used for the request
def get_ip_address():
    proxies = {
        "http": SCRAPERAPI_PROXY,
        "https": SCRAPERAPI_PROXY,
    }
    response = requests.get('https://httpbin.org/ip', proxies=proxies, verify=False)
    ip_data = response.text
    return ip_data

# Check the IP address multiple times
def check_ip_changes(num_checks=5, delay=5):
    ip_addresses = []
    for _ in range(num_checks):
        ip_address = get_ip_address()
        ip_addresses.append(ip_address)
        print(f"IP Address used for the request: {ip_address}")
        time.sleep(delay)  # Wait for a specified delay before the next check

    return ip_addresses

# Perform the IP address checks
ip_addresses = check_ip_changes()

# Check for IP address changes
if len(set(ip_addresses)) > 1:
    print("IP address is changing.")
else:
    print("IP address is not changing.")

