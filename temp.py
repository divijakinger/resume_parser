from selenium import webdriver
import time

driver=webdriver.Chrome()

driver.get('https://tecoholic.github.io/ner-annotator/')
driver.maximize_window()

# Loop here

driver.find_element_by_xpath('//input[@name="textfile"]').send_keys(r'C:\Users\Shivam Thakkar\Desktop\Coding\Deep Blue\1.txt')

driver.find_element_by_xpath('//select[@name="split_type"]').click()

driver.find_element_by_xpath('//option[@value="emptyline"]').click()

l=['PERSON','LOCATION','SKILLS','CONTACT','EMAIL','ROLE','ORGANISATION','DURATION','CERTIFICATE','PROJECTS','EDUCATION','INSTITUTION']

for i in l:
        driver.find_element_by_xpath('//input[@type="text"]').send_keys(i)
        driver.find_element_by_xpath('//button[contains(text(),"Add")]').click()
        driver.find_element_by_xpath('//span[@class="icon"]').click()

time.sleep(300)
