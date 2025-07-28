import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import os
import re
from urllib.parse import urljoin

page_url = input("Enter Koofr public share URL: ").strip()
base_url = "https://app.koofr.net"
media_extensions = ['.mp4', '.jpg', '.jpeg', '.png']

options = uc.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--window-size=1920,3000")
driver = uc.Chrome(options=options)

def sanitise_filename(name):
    return re.sub(r'[\\\\/*?:"<>|]', "_", name.strip())

def try_click_reveal_button():
    try:
        button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "l-link-throttled-notice__button"))
        )
        button.click()
        time.sleep(6)
        return True
    except:
        return False

def scroll_to_bottom(max_scrolls=15, pause_time=1.5):
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(max_scrolls):
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def extract_media_links():
    elements = driver.find_elements(By.XPATH, "//a[contains(@href, '.mp4') or contains(@href, '.jpg') or contains(@href, '.jpeg') or contains(@href, '.png')]")
    media_links = set()
    for element in elements:
        href = element.get_attribute("href")
        if href:
            if href.startswith("/"):
                href = urljoin(base_url, href)
            if any(ext in href.lower() for ext in media_extensions):
                media_links.add(href)
    return media_links

def download_file(link, filename, folder, retries=3):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': page_url
    }
    path = os.path.join(folder, filename)
    for attempt in range(retries):
        try:
            response = requests.get(link, headers=headers, stream=True, timeout=40)
            if response.status_code == 200:
                with open(path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return
        except:
            time.sleep(2)

try:
    driver.get(page_url)
    time.sleep(6)

    try_click_reveal_button()
    scroll_to_bottom()

    try:
        folder_name_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "l-navbar-breadcrumbs__link--text"))
        )
        folder_name = sanitise_filename(folder_name_element.text)
    except:
        folder_name = "koofr_downloads"

    os.makedirs(folder_name, exist_ok=True)

    media_links = extract_media_links()
    driver.quit()

    if not media_links:
        print("No media links found.")
        exit()

    print(f"Downloading {len(media_links)} file(s) to folder: {folder_name}")
    for link in media_links:
        filename = os.path.basename(link.split("?")[0])
        download_file(link, filename, folder_name)
        time.sleep(2)

except Exception as e:
    print(f"Error: {e}")
    driver.quit()