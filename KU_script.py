import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from vars import terms, careers

format = "WEB"

total_execution_time = 0

for term in terms:
    for career in careers:
        time.sleep(10)
        # Initialize WebDriver
        driver = webdriver.Chrome()
        start_time = time.time()
        # URL of the page you want to scrape
        url = "https://classes.ku.edu/"
        driver.get(url)

        wait = WebDriverWait(driver, 10)

        # Store the current/main window handle for the driver to return back to
        main_window_handle = None
        while not main_window_handle:
            main_window_handle = driver.current_window_handle

        # Find the term selection and select the specified term
        term_select = Select(wait.until(EC.visibility_of_element_located((By.NAME, "searchCareer"))))
        term_select.select_by_visible_text(career)

        # Find the term selection and select the specified term
        term_select = Select(wait.until(EC.visibility_of_element_located((By.NAME, "searchTerm"))))
        term_select.select_by_visible_text(term)

        # Find and click the more options button
        options_button = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "moreOptionsButton"))
        )
        options_button.click()

        # Find and select the specific format to scrape content as (WEB vs. Excel)
        select_results_format = Select(
            wait.until(EC.visibility_of_element_located((By.ID, "classesDisplayResultsFormat")))
        )
        select_results_format.select_by_value(format)

        # Find and click the search button to find the list of course info
        search_button = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "classSearchButton"))
        )
        search_button.click()

        alert = driver.switch_to.alert
        alert.accept()

        driver.switch_to.window(main_window_handle)

        WebDriverWait(driver, timeout=200).until(
            EC.presence_of_element_located((By.CLASS_NAME, "class_list"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")

        with open(f"soups/{term} {career} Soup.txt", "w", encoding="utf-8") as file:
            file.write(str(soup))

        end_time = time.time()
        execution_time = end_time - start_time
        total_execution_time += execution_time

        print(f"Scraping html content of all courses for {term} {career} took: {execution_time:.2f} seconds")
        time.sleep(2)
        driver.close()

print(f"Scraping html content of all courses for all terms took: {total_execution_time:.2f} seconds")