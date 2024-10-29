import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from vars import courses_urls

# Array to store courses information
courses = []

# Initialize WebDriver
driver = webdriver.Chrome()
start_time = time.time()

# URL of the page you want to scrape
driver.get(courses_urls[0])

time.sleep(5)

wait = WebDriverWait(driver, 10)

# Store the current/main window handle for the driver to return back to
main_window_handle = None
while not main_window_handle:
    main_window_handle = driver.current_window_handle

try:
    # Find all buttons with the specified class
    buttons = driver.find_elements(By.CLASS_NAME, "accordion.ku-courses-accordion.card-header")

    # Loop through each button, parse and store h3 text
    for button in buttons:
        # Find the h3 element inside the button
        h3_element = button.find_element(By.TAG_NAME, "h3")
        
        # Get the text content of the h3 element
        course_info = h3_element.text.strip()
        
        if "_" not in course_info:
            # Append to the courses list
            courses.append(course_info)

finally:
    # Close the browser
    driver.quit()

# Write courses to a file
with open("courses_info.txt", "w") as file:
    for course in courses:
        file.write(course + "\n")

print("Course information saved to courses_info.txt")
