import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from vars import terms, careers
import json

# term = "Fall 2024"
# career = "Undergrad & Graduate"
# format = "WEB"

# # Initialize WebDriver
# driver = webdriver.Chrome()
# start_time = time.time()
# # URL of the page you want to scrape
# url = "https://classes.ku.edu/"
# driver.get(url)

# wait = WebDriverWait(driver, 10)

# # Store the current/main window handle for the driver to return back to
# main_window_handle = None
# while not main_window_handle:
#     main_window_handle = driver.current_window_handle

# # Find the term selection and select the specified term
# term_select = Select(
#     wait.until(EC.visibility_of_element_located((By.NAME, "searchCareer")))
# )
# term_select.select_by_visible_text(career)

# # Find the term selection and select the specified term
# term_select = Select(
#     wait.until(EC.visibility_of_element_located((By.NAME, "searchTerm")))
# )
# term_select.select_by_visible_text(term)

# # Find and click the more options button
# options_button = wait.until(
#     EC.element_to_be_clickable((By.CLASS_NAME, "moreOptionsButton"))
# )
# options_button.click()

# # Locate the select element with id "classesSearchDept"
# select_dept = Select(driver.find_element(By.ID, "classesSearchDept"))
# # Retrieve all options and store their values and text in a dictionary
# dept_option_values = [
#     option.get_attribute("value")
#     for option in select_dept.options
#     if option.get_attribute("value") != ""
# ]

# # Find and select the specific format to scrape content as (WEB vs. Excel)
# select_results_format = Select(
#     wait.until(EC.visibility_of_element_located((By.ID, "classesDisplayResultsFormat")))
# )
# select_results_format.select_by_value(format)

# for dept_option in dept_option_values:
#     select_dept.select_by_value(dept_option)

#     # Find and click the search button to find the list of course info
#     search_button = wait.until(
#         EC.element_to_be_clickable((By.CLASS_NAME, "classSearchButton"))
#     )
#     search_button.click()

#     try:
#         wait.until(
#             EC.presence_of_element_located((By.CLASS_NAME, "class_list"))
#         )

#         soup = BeautifulSoup(driver.page_source, "html.parser")
#         time.sleep(2)
#     except:
#         continue

with open("department_options.json") as json_file:
    department_options = json.load(json_file)

with open("subject_options.json") as json_file:
    subject_options = json.load(json_file)

with open("auto_departmentKey.txt", "w") as file:
    for dept in department_options:
        dept_codes = department_options[dept].split(",")
        main_dept_code = dept_codes[0].split("-")[0]
        file.write(dept + f" ({main_dept_code})\n")
        if len(dept_codes) > 1:
            codes = dept_codes[1:]
            for code in codes:
                if code in subject_options and subject_options[code] != dept:
                    file.write("* " + subject_options[code] + f" ({code})\n")

    