import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import os
import re
from tqdm import tqdm

# ---------- CONFIG ---------- #
page_url = input("Enter Koofr public share URL: ").strip()
base_url = "https://app.koofr.net"
media_extensions = ['.mp4', '.jpg', '.jpeg', '.png']
scroll_timeout = 120
# ---------------------------- #

# ---------- CHROME SETUP ---------- #
options = uc.ChromeOptions()
# Comment out next line to see browser while debugging
options.add_argument("--headless")  
options.add_argument("--window-size=1920,3000")
driver = uc.Chrome(options=options)
# ---------------------------------- #

def sanitise_filename(name):
    return re.sub(r'[\\\\/*?:"<>|]', "_", name.strip())

def try_click_reveal_button():
    try:
        button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "l-link-throttled-notice__button"))
        )
        button.click()
        print("Clicked reveal button.")
        time.sleep(6)
        return True
    except:
        return False

def scroll_until_all_links_loaded(timeout=90):
    print("Scrolling to load all files...")
    seen_links = set()
    start_time = time.time()

    while True:
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(2)

        anchors = driver.find_elements(By.XPATH, "//a[contains(@href, '/files/get/')]")
        current_links = set()
        for a in anchors:
            href = a.get_attribute("href")
            if href and any(href.lower().endswith(ext) for ext in media_extensions):
                current_links.add(href)

        # Update the total set
        previous_count = len(seen_links)
        seen_links.update(current_links)

        print(f"Collected {len(seen_links)} unique file(s) so far...")

        if len(seen_links) == previous_count:
            print("No new files found, assuming all are loaded.")
            break

        if time.time() - start_time > timeout:
            print("Reached scroll timeout.")
            break

    return seen_links

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
                total = int(response.headers.get('content-length', 0))
                with open(path, 'wb') as f, tqdm(
                    desc=filename,
                    total=total,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                    leave=True
                ) as bar:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            bar.update(len(chunk))
                return
            else:
                print(f"Failed with status code {response.status_code}")
        except Exception as e:
            print(f"Download error ({attempt+1}/{retries}): {e}")
            time.sleep(2)

# ---------- MAIN EXECUTION ---------- #
try:
    driver.get(page_url)
    time.sleep(6)

    try_click_reveal_button()

    # Get folder name from UI if available
    try:
        folder_name_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "l-navbar-breadcrumbs__link--text"))
        )
        folder_name = sanitise_filename(folder_name_element.text)
    except:
        folder_name = "koofr_downloads"

    os.makedirs(folder_name, exist_ok=True)

    # SCROLL AND COLLECT DOWNLOAD LINKS
    media_links = scroll_until_all_links_loaded(timeout=scroll_timeout)
    driver.quit()

    if not media_links:
        print("No media links found.")
        exit()

    print(f"Downloading {len(media_links)} file(s) to folder: {folder_name}")
    for link in media_links:
        filename = os.path.basename(link.split("?")[0])
        download_file(link, filename, folder_name)
        time.sleep(2)  # Optional: avoid rate limits

except Exception as e:
    print(f"Fatal error: {e}")
    driver.quit()