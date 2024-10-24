import time
import json
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

start_time = time.time()

# Initialize WebDriver
driver = webdriver.Chrome()

departments_file_path = "KU_department_names.json"

# URL of the page you want to scrape
url = "https://directory.ku.edu/departments"
driver.get(url)

wait = WebDriverWait(driver, 10)

# Store the current/main window handle for the driver to return back to
main_window_handle = None
while not main_window_handle:
    main_window_handle = driver.current_window_handle

table_option = "-1"  # Show all entries in course catalog table

select_results_format = Select(
    wait.until(EC.visibility_of_element_located((By.NAME, "personResults_length")))
)
select_results_format.select_by_value(table_option)

time.sleep(2)

soup = BeautifulSoup(driver.page_source, "html.parser")
tbody_tag = soup.find("tbody")

with open(f"Course Catalog Soup.txt", "w", encoding="utf-8") as file:
    file.write(str(soup))

tr_tags = tbody_tag.find_all("tr")

departments = {}

for tr_tag in tr_tags:
    td_tags = tr_tag.find_all("td")

    dept_name = td_tags[0].text
    dept_number = td_tags[1].text

    print(f"{dept_name} | {dept_number}")
    departments[dept_name] = dept_number

with open(departments_file_path, "w") as json_file:
    json.dump(departments, json_file, indent=4)


end_time = time.time()
execution_time = end_time - start_time

print(f"Scraping html content of all department names took: {execution_time:.2f} seconds")
