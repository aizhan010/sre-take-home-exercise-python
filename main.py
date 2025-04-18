import yaml
import requests
import time
import sys
from urllib.parse import urlparse
from collections import defaultdict

# Function to load configuration from the YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def get_domain(url):
    parsed = urlparse(url)
    return parsed.hostname

# Function to perform health checks
def check_endpoint(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET')
    headers = endpoint.get('headers')
    body = endpoint.get('body')

    try:
        start = time.time()
        response = requests.request(method, url, headers=headers, data=body, timeout=0.5)
        elapsed = (time.time() - start) * 1000

        if 200 <= response.status_code < 300 and elapsed <= 500:
            return True
    except requests.RequestException:
        pass

    return False

# Main function to monitor endpoints
def monitor(config_path):
    endpoints = load_config(config_path)
    stats = defaultdict(lambda: {"up": 0, "total": 0})

    while True:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Running checks...")

        for ep in endpoints:
            domain = get_domain(ep['url'])
            is_up = check_endpoint(ep)

            stats[domain]["total"] += 1
            if is_up:
                stats[domain]["up"] += 1

        for domain, data in stats.items():
            availability = round((data["up"] / data["total"]) * 100)
            print(f"  {domain} - {availability}% availability")

        print("-" * 40)
        time.sleep(15)

# Entry point of the program
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python monitor.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")