from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize the WebDriver (no need for the specific path)
driver = webdriver.Chrome()

# Open the target URL (UH directory URL)
driver.get("https://www.uh.edu/directory/index.php?emplid=ODAyMTAxNw==&loc=HR730&dpt=H0090")

# Read names from the text file into an array
with open('uh_professors.txt', 'r') as file:
    names = file.readlines()

# Arrays to store professor email addresses and departments
professor_emails = []
professor_departments = []

# Loop through each name in the list
for name in names:
    name = name.strip()  # Remove any extra spaces or newlines
    
    try:
        # Find the input field with id "uh_phonebook_q" and set the text to the current name
        input_field = driver.find_element(By.ID, 'uh_phonebook_q')
        input_field.clear()  # Clear the input field if there's any previous text
        input_field.send_keys(name)
        
        # Find the submit button and click it
        submit_button = driver.find_element(By.NAME, 'submit')
        submit_button.click()
        
        # Wait for the results to load
        time.sleep(2)  # Adjust time as necessary, or use WebDriverWait for more precise handling
        
        # Find the div with id "uhspn_search_results"
        search_results_div = driver.find_element(By.ID, 'uhspn_search_results')
        
        # Find all <dt> elements inside the search results
        search_results = search_results_div.find_elements(By.TAG_NAME, 'dt')
        
        # Loop through each search result
        for result in search_results:
            try:
                # Find the <a> inside the <dt> and get the text
                professor_link = result.find_element(By.TAG_NAME, 'a')
                professor_name = professor_link.text.strip()
                
                # Split the name into last name, first name
                last_name, first_name = professor_name.split(',', 1)
                last_name = last_name.strip()
                first_name = first_name.strip()
                
                # If the current name has more than 3 words, take the first and last words as the first and last name
                name_parts = name.split()
                if len(name_parts) > 3:
                    current_last_name = name_parts[-1]
                    current_first_name = name_parts[0]
                else:
                    # Otherwise, use the first and last name as usual
                    current_last_name = name_parts[-1]
                    current_first_name = name_parts[0]
                
                # Compare the extracted name with the current name
                if current_last_name.lower() == last_name.lower() and current_first_name.lower() == first_name.lower():
                    # If they match, click the link
                    professor_link.click()
                    
                    # Wait for the new result to load
                    time.sleep(3)  # Adjust time as necessary
                    
                    # Find the table with class "vcard"
                    vcard_table = driver.find_element(By.CLASS_NAME, 'vcard')
                    
                    # Find all <tr> elements in the table
                    rows = vcard_table.find_elements(By.TAG_NAME, 'tr')
                    
                    # Variables to hold email and department
                    email_found = False
                    department_found = False
                    
                    # Loop through each row to find the email and department
                    for row in rows:
                        try:
                            # Find the <th> and check if it contains the text "E-mail:"
                            th = row.find_element(By.TAG_NAME, 'th')
                            if th.text.strip() == "E-mail:":
                                # Find the <a> tag with the email address
                                email_link = row.find_element(By.TAG_NAME, 'a')
                                email_address = email_link.text.strip()
                                
                                # Add the email to the professor_emails array
                                professor_emails.append(email_address)
                                
                                # Print the found email and associated professor name
                                print(f"Found email for {name}: {email_address}")
                                email_found = True
                                break  # Exit the loop once the email is found
                            
                            # Find the <th> and check if it contains the text "Department:"
                            if th.text.strip() == "Department:":
                                # Find the <td> containing the department name
                                department_td = row.find_element(By.TAG_NAME, 'td')
                                department_name = department_td.text.strip()
                                
                                # Add the department to the professor_departments array
                                professor_departments.append(department_name)
                                
                                # Print the found department and associated professor name
                                print(f"Found department for {name}: {department_name}")
                                department_found = True
                                break  # Exit the loop once the department is found
                        except Exception as e:
                            print(f"Error processing <tr>: {e}")
                    
                    # If no email was found, append "N/A"
                    if not email_found:
                        professor_emails.append("N/A")
                    
                    # If no department was found, append "N/A"
                    if not department_found:
                        professor_departments.append("N/A")
                    
                    break  # Stop looping through results if a match is found
            except Exception as e:
                print(f"Error processing a search result: {e}")
                
    except Exception as e:
        print(f"Error processing {name}: {e}")

# Write the professor emails and departments to a text file
with open('uh_professor_emails.txt', 'w') as email_file, open('uh_professor_departments.txt', 'w') as department_file:
    for email in professor_emails:
        email_file.write(f"{email}\n")
    for department in professor_departments:
        department_file.write(f"{department}\n")

# Print the list of professor emails and departments
print("Professor emails have been saved to 'uh_professor_emails.txt'.")
print("Professor departments have been saved to 'uh_professor_departments.txt'.")

# Close the browser after the loop
driver.quit()
