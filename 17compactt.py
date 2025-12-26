from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import networkx as nx
import matplotlib.pyplot as plt
from urllib.parse import urlparse
import time

LIMIT = 10
MAX_DEPTH = 2  # Change this to control recursion depth
FILTER_DOMAIN = True  # Set to False to allow external links

# Set Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

# Initialize driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Extract last path segment from URL
def lsr(ln):
    try:
        path = urlparse(ln).path
        return path.strip('/').split('/')[-1] or "root"
    except:
        return "unknown"

# Extract domain from URL
def get_domain(url):
    return urlparse(url).netloc

# Get links from a page
def get_link(url, limit):
    lst = []
    if url.endswith('/'):
        url = url[:-1]
    print(f"visiting {url} ....")

    try:
        driver.get(url)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "a")))
        elements = driver.find_elements(By.TAG_NAME, "a")
        for a in elements:
            try:
                href = a.get_attribute("href")
                if href:
                    if FILTER_DOMAIN and get_domain(href) != get_domain(url):
                        continue
                    lst.append(href)
                    if len(lst) >= limit:
                        break
            except:
                continue
    except Exception as e:
        print(f"Error visiting {url}: {e}")
    return lst

# Recursive crawler with depth control
def crawl(url, depth, visited=None):
    if visited is None:
        visited = set()
    if depth > MAX_DEPTH or url in visited:
        return {}

    visited.add(url)
    children = get_link(url, LIMIT)
    tree = {url: children}

    for child in children:
        if child not in visited:
            subtree = crawl(child, depth + 1, visited)
            tree.update(subtree)
    return tree

# Build and visualize graph
def matwork(murl, dicto):
    print("building graph...")
    time.sleep(2)
    G = nx.DiGraph()
    root = lsr(murl)
    G.add_node(root)

    for parent_url, children in dicto.items():
        parent = lsr(parent_url)
        G.add_node(parent)
        G.add_edge(root, parent)
        for child_url in children:
            child = lsr(child_url)
            G.add_node(child)
            G.add_edge(parent, child)

    pos = nx.spring_layout(G, k=0.5)
    nx.draw(G, pos, with_labels=True, node_size=1100, font_size=6, arrows=True)
    plt.title("Recursive Site Connectivity Map")
    plt.show()
# Main function
def main():
    try:
        url = input("Enter URL of website: ").strip()
        if not url.startswith("http"):
            url = "https://" + url
        site_map = crawl(url, depth=0)
        mod(site_map)
        #matwork(url, site_map)
    finally:
        driver.quit()

main()

