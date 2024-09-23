import time
import os
import shutil
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import pandas as pd

start_time = time.time()

# Set up Chrome options to download files to a specific folder
download_folder = "/Users/FarisKhattak/Documents/Github/honors-thesis-web-scraper"
download_name = "ClassSearchResults.xlsx"
file_name = "Undergrad_Fall2024_ClassSearchResults.xlsx"
download_path = os.path.join(download_folder, download_name)
file_path = os.path.join(download_folder, file_name)

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
        time.sleep(1)  # Wait and check again

    driver.close()

    if os.path.exists(download_path):
        shutil.move(download_path, file_path)


df = pd.read_excel(file_name)

# Writing courses to file
courses_set = set()

with open('undergrad_courses.txt', 'w') as file:
    # Iterate through the rows using itertuples() for better performance
    for row in df.itertuples(index=False):
        # Access the values of specific columns by their names
        course = getattr(row, "Course")
        number = getattr(row, "Number")
        course_title = getattr(row, "_3")
        course_topic = getattr(row, "_4")
        full_course = ""

        if pd.notna(number) and pd.isna(course_topic):
            full_course = f"{course} {number} {course_title}"
        elif pd.notna(course_topic):
            full_course = f"{course} {number} {course_title} {course_topic}"

        if not full_course in courses_set:
            courses_set.add(full_course)
            file.write(f"{full_course}\n")

end_time = time.time()
execution_time = end_time - start_time

print(f"Total Courses: {len(courses_set)}")
print(f"Parsing of KU courses took {execution_time:.2f} seconds")