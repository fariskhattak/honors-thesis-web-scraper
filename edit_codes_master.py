import json

with open("departments/KU_codes_master.json", "r") as json_file:
    codes = json.load(json_file)

for code in codes:
    code_list = codes[code]
    c = code_list[0]
    if "-DEPT" in c:
        split_c = c.split("-")
        c = split_c[0]

    codes[code] = c

with open("departments/KU_codes_master.json", "w") as json_file:
    json.dump(codes, json_file, indent=4)