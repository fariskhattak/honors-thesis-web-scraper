import os

# Directory containing the .txt files
directory = 'courses/semester_specific'

# Lists to store extracted course data
undergrad_courses = []
graduate_courses = []

# Helper function to check if a course already exists in the list
def course_exists(course_list, course_code, course_num, course_name):
    for course in course_list:
        if (course['course_code'] == course_code and
            course['course_num'] == course_num and
            course['course_name'] == course_name):
            return True
    return False

# Loop through each file in the 'courses' directory
for filename in os.listdir(directory):
    # Process only .txt files
    if filename.endswith('.txt'):
        filepath = os.path.join(directory, filename)
        
        # Determine if the file is undergrad or graduate
        if 'undergrad' in filename.lower():
            course_list = undergrad_courses
        elif 'graduate' in filename.lower():
            course_list = graduate_courses
        else:
            continue  # Skip files that don't match criteria
        
        # Open and read the file
        with open(filepath, 'r') as file:
            # Read each line in the file
            for line in file:
                # Split line by spaces
                parts = line.strip().split()
                
                # Check if line has enough parts to unpack
                if len(parts) >= 2:
                    course_code = parts[0]
                    course_num = parts[1]
                    course_name = ' '.join(parts[2:])
                    
                    # Insert into course list if it doesn't already exist
                    if not course_exists(course_list, course_code, course_num, course_name):
                        course_list.append({
                            'course_code': course_code,
                            'course_num': course_num,
                            'course_name': course_name
                        })

undergrad_courses.sort(key=lambda x: (x['course_code'], x['course_num']))
graduate_courses.sort(key=lambda x: (x['course_code'], x['course_num']))

with open(f'courses/undergrad_courses.txt', 'w') as file:
    for course in undergrad_courses:
        file.write(f"{course["course_code"]} {course["course_num"]} {course["course_name"]}\n")
with open(f'courses/graduate_courses.txt', 'w') as file:
    for course in graduate_courses:
        file.write(f"{course["course_code"]} {course["course_num"]} {course["course_name"]}\n")

# Output the extracted course data
print("Undergrad Courses:")
for course in undergrad_courses:
    print(course)

print("\nGraduate Courses:")
for course in graduate_courses:
    print(course)
