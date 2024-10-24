import json
from vars import terms, careers

professor_master_list = {}

for term in terms:
    for career in careers:
        with open(f"professors/{term} {career} professor_departments.json") as json_file:
            professor_departments = json.load(json_file)

        keys = professor_departments.keys()
        for key in keys:
            if key not in professor_master_list:
                professor_master_list[key] = {
                    "professor_count": 0,
                    "professors": []
                }
            professor_list = professor_departments[key]["professors"]
            for prof in professor_list:
                if prof not in professor_master_list[key]["professors"]:
                    professor_master_list[key]["professors"].append(prof)
                    professor_master_list[key]["professor_count"] += 1

for pd in professor_master_list:
    professor_master_list[pd]["professors"] = sorted(professor_master_list[pd]["professors"])

keys = list(professor_master_list.keys())
keys.sort()
sorted_master_list = {i: professor_master_list[i] for i in keys}

with open("professor_departments_master_list.json", "w") as json_file:
    json.dump(sorted_master_list, json_file, indent=4)

with open("KU_codes_master.json", "r") as json_file:
    department_codes = json.load(json_file)

matched_departments = set()
unmatched_departments = set()

for pd in professor_master_list:
    if pd in department_codes.keys():
        matched_departments.add(pd + " | " + department_codes[pd])
    else:
        unmatched_departments.add(pd + " | " + "[UNMATCHED]")

with open("departments_matching_master_list.txt", "w") as file:
    file.write("-"*50 + "\n")
    file.write("MATCHED DEPARTMENTS\n")
    file.write("-"*50 + "\n")
    for dept in sorted(matched_departments):
        file.write(dept + "\n")
    file.write("-"*50 + "\n")
    file.write("UNMATCHED DEPARTMENTS\n")
    file.write("-"*50 + "\n")
    for dept in sorted(unmatched_departments):
        file.write(dept + "\n")

    file.write("-"*50 + "\n")
    file.write("STATISTICS:")
    file.write("-"*50 + "\n")
    file.write(f"NUMBER OF MATCHED DEPARTMENTS: {len(matched_departments)}\n")
    file.write(f"PERCENTAGE OF MATCHED: {len(matched_departments)}/{len(professor_master_list)} = {(len(matched_departments)/(len(professor_master_list)) * 100):.2f}%\n")
    file.write(f"NUMBER OF UNMATCHED DEPARTMENTS: {len(unmatched_departments)}\n")
    file.write(f"PERCENTAGE OF UNMATCHED: {len(unmatched_departments)}/{len(professor_master_list)} = {(len(unmatched_departments)/(len(professor_master_list)) * 100):.2f}%\n")

print(f"Number of Departments: {len(professor_master_list)}")
print(f"Number of Matched: {len(matched_departments)}")
print(f"Number of Unmatched: {len(unmatched_departments)}")