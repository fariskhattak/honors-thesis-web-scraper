import time
import time
from tqdm.auto import tqdm
from bs4 import BeautifulSoup
from vars import terms, careers

total_courses = 0
start_time = time.time()

# term = "Fall 2024"
for term in terms:
    for career in careers:
        print("-"*40)
        print(f"Finding courses in {term}...")
        with open(f"soups/{term} {career} Soup.txt", "r", encoding="utf-8") as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, "html.parser")

        # Writing courses to file
        courses = set()

        # Get the table with all the course information
        all_courses_table = soup.find_all("table")[1]
        tds = all_courses_table.find_all("td")

        i = 0
        # Using a while loop to iterate through the rows in groups of three
        while i < len(tds) - 2:
            # Row 1: Course name
            h3 = tds[i].find("h3")
            if h3 is not None:
                course_number = h3.text.strip()
                full_text = tds[i].text.replace(course_number, '').strip()
                course_title = full_text.split(' - ', 1)[1].split('(', 1)[0].strip()
                course_info = f"{course_number} {course_title}"

                # Row 3: Class list (assuming it exists and can be handled if needed)
                class_list = tds[i + 2].find("table", class_="class_list")
                topics = []
                if class_list is not None:
                    # Step 4: Loop through each `td` tag to find topic names.
                    for td in class_list.find_all("td"):
                        text = td.text.strip()
                        if "Topic: " in text:
                            # Extract the topic name after "Topic: ".
                            topic_name = td.text.strip().splitlines()[0].replace("Topic:", "").strip()
                            topics.append(topic_name)

                if len(topics) > 0:
                    for topic in topics:
                        full_course = course_info + " " + topic
                        courses.add(full_course)
                else:
                    courses.add(course_info)

            # Move to the next group of three rows
            i += 1

        if career == "Undergraduate":
            with open(f'courses/{term} undergrad_courses.txt', 'w') as file:
                for course in sorted(courses):
                    file.write(f"{course}\n")
        elif career == "Graduate":
            with open(f'courses/{term} graduate_courses.txt', 'w') as file:
                for course in sorted(courses):
                    file.write(f"{course}\n")

        end_time = time.time()
        execution_time = end_time - start_time

        print(f"Total Courses in {term} {career}: {len(courses)}")
        total_courses += len(courses)

print("-"*40)
print(f"Total Courses in all terms: {total_courses}")
print(f"Parsing of KU courses took {execution_time:.2f} seconds")
