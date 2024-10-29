# Parse the undergrad_courses.txt file to extract course codes and store them in course_codes.txt

input_file_path = 'courses/undergrad_courses.txt'
output_file_path = 'course_codes.txt'

# List to store course codes
course_codes = set()

# Read the file and extract the course code from each line
with open(input_file_path, 'r') as file:
    for line in file:
        # Split line by spaces
        parts = line.strip().split()
        
        # If there are parts, take the first index as the course code
        if parts:
            course_code = parts[0]
            course_codes.add(course_code)

# Write the extracted course codes to the output file
with open(output_file_path, 'w') as output_file:
    for code in sorted(course_codes):
        output_file.write(code + '\n')
