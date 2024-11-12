from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import time
import os

# Set up Chrome options
options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,3000")  # Increased viewport height
driver = webdriver.Chrome(options=options)

# Open the page containing media files
url = ""
driver.get(url)
time.sleep(5)  # Initial wait for page to start loading

# Incremental scrolling to load all content
scroll_pause_time = 2
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(scroll_pause_time)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Extract links to media files
media_links = set()
elements = driver.find_elements("xpath", "//a[contains(@href, '.JPG') or contains(@href, '.mp4') or contains(@href, '.jpg') or contains(@href, '.png')]")

for element in elements:
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)
        webdriver.ActionChains(driver).move_to_element(element).perform()
        time.sleep(0.5)
        link = element.get_attribute("href")
        if link:
            media_links.add(link)
    except Exception as e:
        print(f"Error interacting with element: {e}")

driver.quit()

# Display found media links
print("Found media links:")
for link in media_links:
    print(link)

# Set headers for requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Referer': url,
}

# Define a download function with retries
def download_file(link, filename, retries=3, timeout=40):
    attempt = 0
    while attempt < retries:
        try:
            print(f"Attempting to download {filename} (Attempt {attempt + 1})...")
            response = requests.get(link, headers=headers, stream=True, timeout=timeout)
            
            if response.status_code == 200:
                with open(filename, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                print(f"Downloaded {filename}")
                return  # Exit function on success
            else:
                print(f"Failed to download {filename}: Status {response.status_code}")
                break  # Exit on non-200 status
        except requests.exceptions.Timeout:
            print(f"Timeout for {filename}, retrying...")
            attempt += 1
            time.sleep(2)  # Short delay before retry
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {filename} due to network error: {e}")
            break  # Exit if it's a different network issue

# Download each media file
for link in media_links:
    filename = os.path.basename(link.split("?")[0])  # Extract filename from URL
    download_file(link, filename)
    time.sleep(3)  # Short delay between downloads to avoid throttling
