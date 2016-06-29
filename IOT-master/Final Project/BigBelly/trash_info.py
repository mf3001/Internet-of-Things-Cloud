USERNAME = "Jschneider"
PASSWORD = "downtownny"
LOGIN_URL = "https://clean.bigbelly.com/login.jsp"
URL = "https://clean.bigbelly.com/fleet-status.jsp?account=567"
FILENAME = "realTrash.csv"

import requests
from lxml import html
from xml.etree import ElementTree
from selenium import webdriver
import time
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import csv 



class trash_info(object):
    """docstring for trash_info"""
    def __init__(self, filename):
        super(trash_info, self).__init__()
        self.filename = filename

    def updateCsv(self, FILENAME):
        driver = webdriver.PhantomJS()
        driver.cookiesEnabled = 'True'
        driver.set_window_size(1366,768)

        # Perform login
        driver.get(LOGIN_URL)
        username = driver.find_element_by_id("email-input")
        password = driver.find_element_by_id("password-input")
        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)
        form = driver.find_element_by_name('form')
        form.submit()
        driver.implicitly_wait(20) # gives an implicit wait for 20 seconds
        content = driver.find_element_by_id("content")

        # Scrape url
        driver.get(URL)
        driver.implicitly_wait(20) # gives an implicit wait for 20 seconds
        tab = driver.find_element_by_link_text("List")
        tab.click()
        driver.implicitly_wait(20) # gives an implicit wait for 20 seconds
        
        # deal with html element with dynamic id
        select = Select(driver.find_element_by_xpath("//div[@id='content']//div[@id='tabs']//div[@id='compactor-table']//div[@id='yui-dt13-paginator0']//select[starts-with(@id,'yui-pg0-0-rpp')]"))
        driver.implicitly_wait(20) # gives an implicit wait for 20 seconds
        select.select_by_visible_text("Show All")
        driver.implicitly_wait(20) # gives an implicit wait for 20 seconds

        num = 25
        index = 'yui-rec'+str(num)
        try:
            os.remove(FILENAME)
        except:
            pass
            
        c = csv.writer(open(FILENAME, "wb"))
        c.writerow(['SerialNumber','Component','Waste Stream','Description','FullnessLevel','FullnessAge','Group'])
        try:
            while (driver.find_element_by_id(index)!=None):
                line = []
                index = 'yui-rec'+str(num)
                content2 = driver.find_element_by_id(index)
                content3 = content2.text
                line.append(content3)
                content4 = line[0].encode("utf-8").split("\n")   #list
                #print content4
                c.writerow(content4)
                num = num + 1
                index = 'yui-rec'+str(num)
        except:
            pass

        driver.close()


if __name__ == '__main__':

    test_trash = trash_info(FILENAME)
    test_trash.updateCsv(FILENAME)

