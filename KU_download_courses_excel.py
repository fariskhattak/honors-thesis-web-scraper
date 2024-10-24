import time
import os
import shutil
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

download_folder = "/Users/FarisKhattak/Documents/Github/honors-thesis-web-scraper"
download_name = "ClassSearchResults.xlsx"
file_name = "Undergrad_Fall2024_ClassSearchResults.xlsx"

download_path = os.path.join(download_folder, download_name)
file_path = os.path.join(download_folder, file_name)

# Check if the file already exists and delete it if it does
if os.path.exists(file_path):
    os.remove(file_path)
    print(f"Deleted existing file: {file_path}")

# Set up Chrome options to download files to a specific folder
chrome_options = Options()
prefs = {
    "download.default_directory": download_folder,  # Set download folder
    "download.prompt_for_download": False,          # No download prompt
    "download.directory_upgrade": True,             # Auto-overwrite files
    "safebrowsing.enabled": True                    # Enable safe browsing
}
chrome_options.add_experimental_option("prefs", prefs)

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

# URL of the page you want to scrape
url = "https://classes.ku.edu/"
driver.get(url)
format = "XLS-multiple"

wait = WebDriverWait(driver, 10)

if not os.path.exists(file_path):

    options_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "moreOptionsButton")))
    options_button.click()

    select_results_format = Select(wait.until(EC.visibility_of_element_located((By.ID, "classesDisplayResultsFormat"))))
    select_results_format.select_by_value(format)

    search_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "classSearchButton")))
    search_button.click()

    # Poll the download folder until the file is fully downloaded
    while not os.path.exists(download_path) or download_path.endswith('.part'):
        print("Downloading file...")
        time.sleep(1)  # Wait and check again

    print("Finished download!")

    driver.close()

    if os.path.exists(download_path):
        shutil.move(download_path, file_path)
        print(f"Renamed {download_name} to {file_name}")