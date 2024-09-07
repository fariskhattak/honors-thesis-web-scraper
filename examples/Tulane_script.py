import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from string import Template
#driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='All Courses']")
# Setup webdriver
driver = webdriver.Chrome()

# URL of the page you want to scrape
url = "https://classschedule.tulane.edu/Search.aspx"
driver.get(url)

#'202410' '202420'
#terms = ['202430', '202310', '202320', '202330']

term = '202430'

wait = WebDriverWait(driver, 10)
select_term = Select(wait.until(EC.presence_of_element_located((By.ID, "ddlterm"))))
select_term.select_by_value(term)

select_subject = Select(wait.until(EC.presence_of_element_located((By.ID, "ddlsubject"))))

#167
options = select_subject.options

for index in range(10, len(options) - 1):
    select_subject.select_by_index(index)
    search_button = wait.until(EC.presence_of_element_located((By.ID, 'btnSearchAll')))
    search_button.click()


    #get the department's first page
    time.sleep(20)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    #get the number of pages
    matches = re.findall(r"Page\$\d", str(soup))
    myset = sorted(set(matches))
   # print(myset)

    with open(f'{term}Soup.txt', 'a', encoding='utf-8') as f:
        f.write(str(soup))

    #if there are other pages
    if len(myset) > 0:
        index = 2
        while index <= len(myset)+1:
            time.sleep(10)
            WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='"+str(index)+"' and contains(@href, 'Page$" + str(index) + "')]"))).click()
            time.sleep(20)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            with open(f'{term}Soup.txt', 'a', encoding='utf-8') as f:
                f.write(str(soup))
            index = index + 1

    url = "https://classschedule.tulane.edu/Search.aspx"
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    select_term = Select(wait.until(EC.presence_of_element_located((By.ID, "ddlterm"))))
    select_term.select_by_value(term)
    select_subject = Select(wait.until(EC.presence_of_element_located((By.ID, "ddlsubject"))))