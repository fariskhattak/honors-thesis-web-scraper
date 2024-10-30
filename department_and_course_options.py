import json
from bs4 import BeautifulSoup

# Path to the file
file_path = "soups/Fall 2024 Undergraduate Soup.txt"

# Dictionary to store options
dept_dict = {}
subject_dict = {}

# Read and parse the HTML file with utf-8 encoding
with open(file_path, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

    # Find the select tag with id "classesSearchDept"
    dept_select_tag = soup.find("select", id="classesSearchDept")

    # if select_tag:
    #     # Extract all option values and names
    #     option_values = [option.get("value") for option in select_tag.find_all("option") if option.get("value")]
    #     option_names = [option.text.strip() for option in select_tag.find_all("option") if option.get("value")]
        
    #     # Store in dictionary with names as keys and values as arrays of values
    #     options_dict = {name: [value] for name, value in zip(option_names, option_values)}

    if dept_select_tag:
        # Extract all option values and names
        for option in dept_select_tag.find_all("option"):
            option_value = option.get("value")
            option_name = option.text.strip()
            if option_value:  # Ignore options without a value
                dept_dict[option_name] = option_value


    # Subject Codes
    subject_select_tag = soup.find('select', {'id': 'classesSearchSubject'})
    subject_options = subject_select_tag.find_all('option')
    for option in subject_options:
        if option.text != "- Any subject -":
            subject_string = ' '.join(option.text.split()[1:])
            subject_dict[option['value']] = subject_string

    

# Dump the dictionary into a JSON file
with open("department_options.json", "w", encoding="utf-8") as json_file:
    json.dump(dept_dict, json_file, ensure_ascii=False, indent=4)
# Dump the dictionary into a JSON file
with open("subject_options.json", "w", encoding="utf-8") as json_file:
    json.dump(subject_dict, json_file, ensure_ascii=False, indent=4)

print(f"Dept dictionary has been saved to department_options.json")
print(f"Subject dictionary has been saved to subject_options.json")
