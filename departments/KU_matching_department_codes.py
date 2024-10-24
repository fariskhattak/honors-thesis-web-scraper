import json

with open("departments/professor_departments.json", "r") as json_file:
    professor_departments = json.load(json_file)

with open("departments/KU_codes_master.json", "r") as json_file:
    codes = json.load(json_file)

matches = set()
unmatched = set()
department_keys = professor_departments.keys()
code_keys = codes.keys()

for key in department_keys:
    if key in code_keys:
        matches.add(f"{key} | {codes[key][0]}")
    else:
        unmatched.add(f"{key} | [UNMATCHED DEPARTMENT]")

with open("departments/department_names.txt", "w") as file:
    for match in matches:
        file.write(match + "\n")

    file.write("-"*50 + "\n")

    for unmatch in unmatched:
        file.write(unmatch + "\n")

    file.write("-"*50 + "\n")
    file.write(f"NUMBER OF MATCHED DEPARTMENTS: {len(matches)}\n")
    file.write(f"PERCENTAGE OF MATCHED: {len(matches)}/{len(professor_departments)} = {(len(matches)/(len(professor_departments)) * 100):.2f}%\n")
    file.write(f"NUMBER OF UNMATCHED DEPARTMENTS: {len(unmatched)}\n")
    file.write(f"PERCENTAGE OF UNMATCHED: {len(unmatched)}/{len(professor_departments)} = {(len(unmatched)/(len(professor_departments)) * 100):.2f}%\n")