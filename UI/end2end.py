from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
import os
from datetime import datetime

baseURL = "http://localhost:3000/"

#Connections
browser = webdriver.Chrome("./chromedriver.exe")
browser.maximize_window()
html = browser.page_source
action = webdriver.ActionChains(browser)

def test_end2end():
    
    browser.get(baseURL)
    time.sleep(5)
    login_to_page()
    select_subject()

def login_to_page():
  
    #Getting Username and Password fields
    try:
        username_block = browser.find_element_by_xpath("//*[@id='email']")
        #print(username_block)
    except:
        print("Error occured during getting username field")
    try:
        password_block = browser.find_element_by_xpath("//*[@id='password']")
        #print(password_block)
    except:
        print("Error occured during getting password field")

    username_block.send_keys("ABC")
    password_block.send_keys("12345")

    browser.find_element_by_xpath("//*[@id='root']/div/main/div[2]/form/button").click()
    time.sleep(5)

    
        

def select_subject():
    try:
        subject_block = browser.find_element_by_xpath("//*[@id='root']/div/div/div[2]/div[2]/div/div[1]/div/button")
    except:
        print("Error occured during getting subject field")

    subject_block.click()
    time.sleep(1)

    try:
        select = browser.find_element_by_xpath("//*[@id='root']/div/div/div[2]/div[2]/div/div[1]/div/ul/li[1]/a")
    except:
        print("Error occured during getting select field")
    
    select.click()
    time.sleep(1)

    try:
        graph = browser.find_element_by_xpath("//*[@id='root']/div/div/div[2]/div[2]/div/div[3]/div/div[1]/div[2]/div/button[2]")
    except:
        print("Error occured during getting graph field")
    
    graph.click()
    time.sleep(1)

   

    count = 0
    while():
        try:
            heat = browser.find_element_by_xpath("//*[@id='JSCharting_19497']/svg/g/g[3]")
            print("found")
            break
        except:
            print("Error occured during getting heatmap")
            count+=1
            print(count)


    try:
        account = browser.find_element_by_xpath('//*[@id="root"]/div/div/div[2]/div[1]/div[1]/ul[3]/li/a')
    except:
        print("Error occured during getting account field")
    
    account.click()
    time.sleep(1)

    try:
        logout = browser.find_element_by_xpath('//*[@id="root"]/div/div/div[2]/div[1]/div[1]/ul[3]/li/ul/li[2]/a')
    except:
        print("Error occured during getting logout field")

    logout.click()
    time.sleep(1)

test_end2end()