# SIMILAR TO KU_departments_codes.py but using different source
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

term = "Fall 2024"
codes_file_path = "KU_codes.json"

with open(f"{term} Soup.txt", "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "html.parser")

codes_dict = {}

# School Codes
school_select_tag = soup.find('select', {'id': 'classesSearchSchool'})
school_options = school_select_tag.find_all('option')
for option in school_options:
    if option.text != "- Any school -":
        codes_dict[option.text] = [option['value']]

# Dept Codes
dept_select_tag = soup.find('select', {'id': 'classesSearchDept'})
dept_options = dept_select_tag.find_all('option')
for option in dept_options:
    if option.text != "- Any dept -":
        dept_codes = option['value'].split(',')
        codes_dict[option.text] = dept_codes

# Subject Codes
subject_select_tag = soup.find('select', {'id': 'classesSearchSubject'})
subject_options = subject_select_tag.find_all('option')
for option in subject_options:
    if option.text != "- Any subject -":
        subject_string = ' '.join(option.text.split()[1:])
        codes_dict[subject_string] = [option['value']]

core_select_tag = soup.find('select', {'id': 'classesSearchCode'})
core_options = core_select_tag.find_all('option')
for option in core_options:
    if option.text != "- Any KU Core/Core 34 course code -":
        core_string = ' '.join(option.text.split()[1:])
        codes_dict[core_string] = [option['value']]

# URL of the page you want to scrape
url = "https://sis.ku.edu/course-catalog-codes-subject"
driver = webdriver.Chrome()
driver.get(url)

wait = WebDriverWait(driver, 10)

# Store the current/main window handle for the driver to return back to
main_window_handle = None
while not main_window_handle:
    main_window_handle = driver.current_window_handle

table_option = "-1"  # Show all entries in course catalog table

select_results_format = Select(
    wait.until(EC.visibility_of_element_located((By.NAME, "DataTables_Table_0_length")))
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

    dept_code = td_tags[0].text
    match = re.search(r'\((.*?)\)', td_tags[1].text)
    if match:
        dept_name = match.group(1)
    else:
        dept_name = td_tags[1]

    if dept_name not in codes_dict:
        codes_dict[dept_name] = [dept_code]

code_keys = list(codes_dict.keys())
code_keys.sort()
sorted_codes = {i: codes_dict[i] for i in code_keys}
with open(codes_file_path, "w") as json_file:
    json.dump(sorted_codes, json_file, indent=4)

print(sorted_codes)
    
end_time = time.time()
execution_time = end_time - start_time

print(f"Finding all KU codes took {execution_time:.2f} seconds to run")