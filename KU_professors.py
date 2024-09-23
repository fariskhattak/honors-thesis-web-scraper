import time
import re
import random as rand
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from string import Template

start_time = time.time()

term = "Fall 2024"

with open(f"{term} Soup.txt", "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "html.parser")

all_professors = set()
unavailable_professors = set()

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

# unavailable_urls = [
#     'https://directory.ku.edu/details/_UEhSjF_vKFrWrXvFcaQJw',
#     'https://directory.ku.edu/details/obQPi6jib65KnUjMtvZJSQ',
#     'https://directory.ku.edu/details/K4XNR5_doQhGqHFMecmmiw',
#     'https://directory.ku.edu/details/o_QBDPxQxUWD52u_kzBR5Q',
#     'https://directory.ku.edu/details/CPhSRpF4OWsf8t4IKtLFjg',
#     'https://directory.ku.edu/details/e9k9iZWqp5Y1xiC9Zw-_eg'
# ]

unavailable_professors = set()

a_professors = set(soup.find_all("a", title="Click here to get instructor info"))
total_professors = len(a_professors)
for index, a in enumerate(a_professors):
    # time.sleep(.5)
    url = a["href"]
    print(f"Trying to access url {index + 1}/{total_professors}: {url}")
    driver.get(url)
    content = wait.until(
        EC.any_of(
            EC.visibility_of_element_located(
                (By.ID, "peepDeets")
            ),  # Professor details if authorized
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'form[action="unauthorized"]')
            ),  # Unauthorized form
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'form[action="notfound"]')
            ),  # Not found form
        )
    )
    professor_soup = BeautifulSoup(driver.page_source, "html.parser")
    forms = professor_soup.find_all("form")
    if len(forms) > 0 and (
        forms[0]["action"] == "notfound" or forms[0]["action"] == "unauthorized"
    ):
        full_name = a.text.split(",")
        first = full_name[1]
        last = full_name[0]
        correct_full_name = f"{first} {last}".title()

        unavailable_professors.add(f"{correct_full_name}, [MISSING EMAIL], {url}")
        print(f"Unable to get information on {correct_full_name} from {url}")
    else:
        # print(professor_soup)
        name = professor_soup.find("h2").text
        tr_tags = professor_soup.find_all("tr")

        for tr_tag in tr_tags:
            th_tag = tr_tag.find("th")
            
            # Check if <th> contains "Department:" or "Email:"
            if th_tag and "Department:" in th_tag.text:
                # Get the text of the corresponding <td> element
                td_tag = tr_tag.find("td")
                dept = td_tag.text.strip()
            elif th_tag and "Email:" in th_tag.text:
                # Get the text of the corresponding <td> element
                td_tag = tr_tag.find("td")
                a_email = td_tag.find("a")

        if a_email is not None:
            email = a_email.text
            full_professor_info = f"{name.title()}, {email.lower()}, {dept}"
            all_professors.add(full_professor_info)
        else:
            email = f"[MISSING EMAIL], {url}"
            full_professor_info = f"{name.title()}, {email.lower()}"
            unavailable_professors.add(full_professor_info)


with open("undergrad_professors.txt", "w") as file:
    file.write(f"AVAILABLE PROFESSOR INFO ({len(all_professors)}):\n")
    file.write("-------------------------------------------------\n")
    for professor in sorted(all_professors):
        file.write(f"{professor}\n")

    file.write("-------------------------------------------------\n")
    file.write(f"UNAVAILABLE PROFESSOR INFO ({len(unavailable_professors)}):\n")
    for professor in sorted(unavailable_professors):
        file.write(f"{professor}\n")

    found_info_percentage = len(all_professors) / total_professors * 100
    unavailable_info_percentage = len(unavailable_professors) / total_professors * 100
    file.write("-------------------------------------------------\n")
    file.write(
        f"STATISTICS:\nFOUND: {found_info_percentage:.2f}%\nUNAVAILABLE (MISSING EMAIL): {unavailable_info_percentage:.2f}%"
    )

end_time = time.time()
execution_time = end_time - start_time

print(f"Program took {execution_time:.2f} seconds to run")