import time
import json
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from vars import terms, careers

total_execution_time = 0
# term = "Fall 2024"
# career = "Graduate"

department_codes_file_path = "departments/KU_codes_master.json"

with open(department_codes_file_path, "r") as json_file:
    department_codes = json.load(json_file)

for term in terms:
    for career in careers:

        start_time = time.time()

        with open(f"soups/{term} {career} Soup.txt", "r", encoding="utf-8") as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, "html.parser")

        all_professors = set()
        unavailable_professors = set()
        departments = {}

        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, 10)

        unavailable_professors = set()

        a_professors = set(soup.find_all("a", title="Click here to get instructor info"))
        total_professors = len(a_professors)

        unmatched_dept_codes_count = 0
        unmatched_dept_codes = set()

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
                name = professor_soup.find("h2").text
                tr_tags = professor_soup.find_all("tr")
                
                dept_name = ""
                for tr_tag in tr_tags:
                    th_tag = tr_tag.find("th")
                    # Check if <th> contains "Department:" or "Email:"
                    if th_tag and "Department:" in th_tag.text:
                        # Get the text of the corresponding <td> element
                        td_tag = tr_tag.find("td")
                        temp_dept_name = re.sub(r'\s*\(.*?\)', '', td_tag.text).strip()
                        # Check if the department already exists in the dictionary
                        if temp_dept_name in departments:
                            if name not in departments[temp_dept_name]['professors']:
                                # If the department exists, add the professor to the list and increment the count
                                departments[temp_dept_name]['professors'].append(name)
                                departments[temp_dept_name]['professor_count'] += 1
                        else:
                            # If the department does not exist, initialize it in the dictionary
                            departments[temp_dept_name] = {
                                'professor_count': 1,  # Start with a count of 1 for the first professor
                                'professors': [name]  # Initialize with the first professor
                            }
                        # dept_name = td_tag.text.strip()
                        if dept_name == "":
                            dept_name = re.sub(r'\s*\(.*?\)', '', td_tag.text).strip()
                        else:
                            dept_name += " | " + re.sub(r'\s*\(.*?\)', '', td_tag.text).strip()
                    elif th_tag and "Email:" in th_tag.text:
                        # Get the text of the corresponding <td> element
                        td_tag = tr_tag.find("td")
                        a_email = td_tag.find("a")

                dept = dept_name

                if a_email is not None:
                    print("FOUND EMAIL")
                    email = a_email.text
                else:
                    print("UNABLE TO FIND EMAIL")
                    email = f"[MISSING EMAIL], {url}"

                full_professor_info = f"{name.title()}, {email.lower()}, {dept}"
                print(full_professor_info)
                all_professors.add(full_professor_info)

        keys = list(departments.keys())
        keys.sort()
        sorted_departments = {i: departments[i] for i in keys}

        with open(f"professors/{term} {career} professor_departments.json", "w") as json_file:
            json.dump(sorted_departments, json_file, indent=4)

        with open(f"professors/ {term} {career.lower()}_professors.txt", "w") as file:
            file.write(f"AVAILABLE PROFESSOR INFO ({len(all_professors)}):\n")
            file.write("-------------------------------------------------\n")
            for professor in sorted(all_professors):
                file.write(f"{professor}\n")

            file.write("-------------------------------------------------\n")
            file.write(f"UNAVAILABLE PROFESSOR INFO ({len(unavailable_professors)}):\n")
            for professor in sorted(unavailable_professors):
                file.write(f"{professor}\n")

            file.write("-------------------------------------------------\n")
            file.write(f"UNMATCHED DEPT CODES ({len(unmatched_dept_codes)}):\n")
            for dept_codes in sorted(unmatched_dept_codes):
                file.write(f"{dept_codes}\n")

            found_info_percentage = len(all_professors) / total_professors * 100
            unavailable_info_percentage = len(unavailable_professors) / total_professors * 100
            unmatched_dept_code_percentage = unmatched_dept_codes_count / total_professors * 100
            file.write("-------------------------------------------------\n")
            file.write(
                f"""STATISTICS:\nFOUND PROFESSOR BIO: {len(all_professors)}/{total_professors} = {found_info_percentage:.2f}%
        UNAVAILABLE BIO (MISSING EMAIL, DEPT): {len(unavailable_professors)}/{total_professors} = {unavailable_info_percentage:.2f}%
        UNMATCHED PROFESSOR (MISSING DEPT): {unmatched_dept_codes_count}/{total_professors} = {unmatched_dept_code_percentage:.2f}%"""
            )

            
        end_time = time.time()
        execution_time = end_time - start_time
        total_execution_time += execution_time
        print(f"Finding {term} {career} professors took {execution_time:.2f} seconds to run")

print(f"Finding all professors took {total_execution_time:.2f} seconds to run")