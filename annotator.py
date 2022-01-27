from itsdangerous import exc
from selenium import webdriver
import time
import os

driver=webdriver.Chrome()
dir_list=os.listdir('shivam')
for name in dir_list:
        print(name)
        driver.get('https://tecoholic.github.io/ner-annotator/')
        driver.maximize_window()
        name='\\'+name
        # Loop here
        driver.find_element_by_xpath('//input[@name="textfile"]').send_keys(r'C:\Users\Shivam Thakkar\Desktop\Coding\Deep Blue\shivam'+name)

        driver.find_element_by_xpath('//select[@name="split_type"]').click()

        driver.find_element_by_xpath('//option[@value="custom"]').click()

        l=['PERSON','LOCATION','SKILLS','CONTACT','EMAIL','ROLE','ORGANISATION','DURATION','CERTIFICATE','PROJECTS','EDUCATION','INSTITUTION']
        time.sleep(5)
        for i in l:
                try:
                        driver.find_element_by_xpath('//input[@placeholder="NER TAG"]').send_keys(i)
                        driver.find_element_by_xpath('//button[contains(text(),"Add")]').click()
                        driver.find_element_by_xpath('//span[@class="icon"]').click()
                except:
                        pass

        i=input('If done the put c')
        if i=='c':
                pass
