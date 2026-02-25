import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import csv

visited = set()
to_visit = set(["https://www.thgingenuity.com"])
broken_links = []

while to_visit:
    url = to_visit.pop()

    if url in visited:
        continue

    visited.add(url)

    try:
        response = requests.get(url, timeout=5)
        print(f"Checking: {url} -> {response.status_code}")

        if response.status_code == 404:
            broken_links.append(url)
            continue

        if "text/html" in response.headers.get("Content-Type", ""):
            soup = BeautifulSoup(response.text, "html.parser")

            for link in soup.find_all("a", href=True):
                full_url = urljoin(url, link["href"])
                parsed = urlparse(full_url)

                # Only crawl same domain
                if parsed.netloc == urlparse("https://www.thgingenuity.com").netloc:
                    to_visit.add(full_url)

    except Exception as e:
        print(f"Error checking {url}: {e}")

print("\nBroken Links:")
for link in broken_links:
    print(link)

# ✅ Export to CSV at the end
filename = "404_report.csv"

with open(filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Broken URL"])
    
    for link in broken_links:
        writer.writerow([link])

print(f"\n📁 404 report exported successfully to {filename}")