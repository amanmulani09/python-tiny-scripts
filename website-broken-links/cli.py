import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import csv
import threading
import itertools
import sys
import time
from colorama import Fore, Style, init

init(autoreset=True)

# =============================
# Hacker Style Banner
# =============================
print(Fore.GREEN + """
==========================================
      404 SCANNER v1.0 - DARK MODE
      Initializing Web Intrusion...
==========================================
""" + Style.RESET_ALL)

visited = set()
to_visit = set(["https://www.thgingenuity.com"])
broken_links = []

# =============================
# Spinner Animation
# =============================
stop_spinner = False

def spinner():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if stop_spinner:
            break
        sys.stdout.write(Fore.CYAN + f'\rScanning... {c} ')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rScan complete!      \n')

spinner_thread = threading.Thread(target=spinner)
spinner_thread.start()

# =============================
# Crawling Logic (UNCHANGED)
# =============================
while to_visit:
    url = to_visit.pop()

    if url in visited:
        continue

    visited.add(url)

    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 404:
            print(Fore.RED + f"\n[404 DETECTED] {url}")
            broken_links.append(url)
            continue
        else:
            print(Fore.GREEN + f"\n[OK {response.status_code}] {url}")

        if "text/html" in response.headers.get("Content-Type", ""):
            soup = BeautifulSoup(response.text, "html.parser")

            for link in soup.find_all("a", href=True):
                full_url = urljoin(url, link["href"])
                parsed = urlparse(full_url)

                if parsed.netloc == urlparse("https://www.thgingenuity.com").netloc:
                    to_visit.add(full_url)

    except Exception as e:
        print(Fore.YELLOW + f"\n[ERROR] {url} -> {e}")

# Stop spinner
stop_spinner = True
spinner_thread.join()

# =============================
# Results
# =============================
print(Fore.MAGENTA + "\n========= SCAN SUMMARY =========")
print(Fore.CYAN + f"Total Pages Scanned: {len(visited)}")
print(Fore.RED + f"Total 404 Found: {len(broken_links)}")

# =============================
# Export CSV
# =============================
filename = "404_report.csv"

with open(filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Broken URL"])

    for link in broken_links:
        writer.writerow([link])

print(Fore.GREEN + f"\n📁 Report exported successfully: {filename}")
print(Fore.GREEN + "Mission Complete ✔")