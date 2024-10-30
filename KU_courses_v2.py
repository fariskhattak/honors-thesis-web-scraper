import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm

# from vars import courses_urls

# Array to store courses information
full_name_courses = []

# Initialize WebDriver
driver = webdriver.Chrome()
start_time = time.time()

# URL of the page you want to scrape
# driver.get(courses_urls[0])
driver.get("https://catalog.ku.edu/course-search/")

time.sleep(3)

wait = WebDriverWait(driver, 10)

# Store the current/main window handle for the driver to return back to
main_window_handle = None
while not main_window_handle:
    main_window_handle = driver.current_window_handle

# Array to store the options and their values
subject_options = []

try:
    # Locate the select element by its id
    select_element = driver.find_element(By.ID, "crit-subject")
    select = Select(select_element)

    # Loop through each option in the select element and get its value
    for option in select.options:
        option_text = option.text
        option_value = option.get_attribute("value")

        # Store the option text and value as a tuple
        subject_options.append((option_text, option_value))

    hours_select_element = driver.find_element(By.ID, "crit-hours_max")
    hours_select = Select(hours_select_element)
    hours_select.select_by_value("1")

    # Locate the search button and click it
    search_button = driver.find_element(By.ID, "search-button")
    search_button.click()

    # Wait for the panel to load
    time.sleep(5)  # Adjust based on load time

    # Find the panel body containing the results
    panel_bodies = driver.find_elements(By.CLASS_NAME, "panel__body")
    panel_body = panel_bodies[1]

    # Find all course result elements
    results = panel_body.find_elements(By.CLASS_NAME, "result--group-start")

    # Loop through each result and extract the code and title
    for result in tqdm(results):
        code = result.find_element(By.CLASS_NAME, "result__code").text.split()[0]
        num = result.find_element(By.CLASS_NAME, "result__code").text.split()[1]
        title = result.find_element(By.CLASS_NAME, "result__title").text

        # Store the code and title in a dictionary
        course_info = {"code": code, "num": num, "title": title}

        # Append the course info to the courses list
        full_name_courses.append(course_info)
        # print(course_info)

finally:
    # Close the browser
    driver.quit()

full_name_courses = sorted(
    full_name_courses, key=lambda x: (x["code"], x["num"], x["title"])
)

# Write undergrad courses (num < 500)
with open("courses/full_name_undergrad_courses.txt", "w") as file:
    for course in full_name_courses:
        try:
            if int(course["num"]) < 500:
                full_name = f"{course['code']} {course['num']} {course['title']}"
                file.write(full_name + "\n")
        except ValueError:
            # Skip this course if "num" is not an integer
            continue

# Write graduate courses (num >= 500)
with open("courses/full_name_graduate_courses.txt", "w") as file:
    for course in full_name_courses:
        try:
            if int(course["num"]) >= 500:
                full_name = f"{course['code']} {course['num']} {course['title']}"
                file.write(full_name + "\n")
        except ValueError:
            full_name = f"{course['code']} {course['num']} {course['title']}"
            file.write(full_name + "\n")
