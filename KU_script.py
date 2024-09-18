import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from string import Template

start_time = time.time()

# Initialize WebDriver
driver = webdriver.Chrome()

# URL of the page you want to scrape
url = 'https://classes.ku.edu/'
driver.get(url)
format = 'WEB'

term = 'Fall 2024' 
term_option_value = '4249' # option value for Fall 2024

wait = WebDriverWait(driver, 10)

# Store the current/main window handle for the driver to return back to
main_window_handle = None
while not main_window_handle:
    main_window_handle = driver.current_window_handle

options_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'moreOptionsButton')))
options_button.click()

select_results_format = Select(wait.until(EC.visibility_of_element_located((By.ID, 'classesDisplayResultsFormat'))))
select_results_format.select_by_value(format)

search_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'classSearchButton')))
search_button.click()

alert = driver.switch_to.alert
alert.accept()

driver.switch_to.window(main_window_handle)

WebDriverWait(driver, timeout=120).until(EC.presence_of_element_located((By.CLASS_NAME, 'class_list')))

# time.sleep(120)

soup = BeautifulSoup(driver.page_source, 'html.parser')

with open(f'{term} Soup.txt', 'w', encoding='utf-8') as file:
    file.write(str(soup))

end_time = time.time()

print(f"Scraping html content of all courses took: {end_time - start_time} seconds")