import json

undergrad_file_path = "professors/undergrad_professors_copy.txt"
graduate_file_path = "professors/undergrad_professors_copy.txt"

def read_professor_data(filepath):
    data = []
    with open(filepath, "r") as file:
        for line in file:
            # Remove any leading/trailing whitespace and split by comma
            parts = line.strip().split(',')
            
            # Ensure the line has the required number of parts (name, email, departments)
            if len(parts) >= 3:
                entry = {
                    'full_name': parts[0].strip(),
                    'email': parts[1].strip(),
                    'departments': [dept.strip() for dept in parts[2].split('|')]  # Splitting by "|"
                }
                data.append(entry)

    return data

# department_codes = {}
# current_department = None

# with open('departmentKey.txt', 'r', encoding='utf-8') as file:
#     for line in file:
#         line = line.strip()  # Remove any leading/trailing whitespace

#         if line and not line.startswith('●'):
#             # Parse main department with code
#             if '(' in line and ')' in line:
#                 department_name, department_code = line.rsplit('(', 1)
#                 department_name = department_name.strip()
#                 department_code = department_code.strip(')')
#                 current_department = department_name
#                 department_codes[current_department] = {
#                     'department_code': department_code,
#                     'sub_departments': {}
#                 }
#             else:
#                 # Parse main department without sub-departments
#                 current_department = line
#                 department_codes[current_department] = {
#                     'department_code': None,
#                     'sub_departments': {}
#                 }
#         elif line.startswith('●') and current_department:
#             # Parse sub-departments
#             sub_department = line.lstrip('●').strip()
#             if '(' in sub_department and ')' in sub_department:
#                 sub_name, sub_code = sub_department.rsplit('(', 1)
#                 sub_name = sub_name.strip()
#                 sub_code = sub_code.strip(')')
#                 department_codes[current_department]['sub_departments'][sub_name] = sub_code
#             else:
#                 department_codes[current_department]['sub_departments'][sub_department] = None

# Print the parsed data as a dictionary
# print(department_codes)

undergrad_professors = read_professor_data(undergrad_file_path)
graduate_professors = read_professor_data(graduate_file_path)

# parse the names of the professors, limit it to first and last name (first and last index split by spaces)
# if the name is the same as another name (common name), keep the middle names
# assign department codes to the department names for each professor

clean_undergrad_professors = []   
for prof in undergrad_professors:
    names = prof["full_name"].split()
    cleaned_name = prof["full_name"]
    if len(names) >= 2:
        first_name = names[0]
        last_name = names[-1]
        cleaned_name = first_name + " " + last_name

    if cleaned_name not in clean_undergrad_professors and prof["email"] != "[MISSING EMAIL]":
        clean_undergrad_professors.append(cleaned_name)
    else:
        print(f"COMMON NAME FOUND: {cleaned_name}, USING FULL NAME: {prof["full_name"]}")
        clean_undergrad_professors.append(prof["full_name"])
        


# # Dumping to JSON files
# with open('department_keys.json', 'w') as file:
#     json.dump(department_codes, file, indent=4)

# clean up professors names to be just first and last name