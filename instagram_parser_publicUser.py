from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import requests
import getpass
import re
from urllib.request import urlopen
import json
import pdb
from pandas.io.json import json_normalize
import pandas as pd, numpy as np
from urllib.request import urlopen
from urllib import  request
import csv
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
import pandas as pd
import datetime
import maya



username = 'cbx.photo'

user_post_link = []
numofbetages_row = ''
allPageContent_list = []
allPageContentlike_list = []
allleavemessageContent_list = []
allleavemessageContent_list2 = []
allleavemessageContent = ''

post_time_list = []
one_monthpost_count = 0
userNumofposts = []
userNumoffollowers = []
userNumoffollows = []

count_response = 0

base_url = 'https://www.instagram.com'
browser = webdriver.Chrome('chromedriver')
browser.implicitly_wait(3)
user_url = 'https://www.instagram.com/'+username+'/?hl=en'
browser.get(user_url)
time.sleep(1)
body = browser.page_source
data=bs(body, 'html.parser')
user = base_url+data.find('a', class_="_9VEo1 T-jvg").get('href')
#print(user)

#寫入CSV檔
def writeFile():
    csv_rows = zip(allPageContent_list,allleavemessageContent_list2,allPageContentlike_list,post_time_list)
    # 開啟輸出的 CSV 檔案
    with open("./instagram account/"+username+".csv","w+", encoding = 'utf_8') as my_csv:
        writer = csv.writer(my_csv)
        writer.writerow(['post content','leavemessage content','num of content likes','post_time','num of posts','num of followers','num of follows','num of tags','avg response','one month posts'])
        for row in csv_rows:
            writer.writerow(row)
            
#寫入CSV檔，num of posts、num of followers、num of follows
def writeFile2():
    df = pd.read_csv("./instagram account/"+username+".csv",encoding = 'utf_8_sig')
    column = df.columns
    for col in column:
        if col == 'num of posts':
            df['num of posts'] = userNumofposts[0]
        elif col == 'num of followers':
            df['num of followers'] = userNumoffollowers[0]
        elif col == 'num of follows':
            df['num of follows'] = userNumoffollows[0]
        elif col == 'avg response':
            df['avg response'] = int(count_response/len(allPageContent_list))
        elif col == 'last_post_time':
            df['last_post_time'] = last_post_time
        elif col == 'one month posts':
            df['one month posts'] = one_monthpost_count
        elif col == 'num of tags':
            df['num of tags'] = 6
    df.to_csv("./instagram account/"+username+".csv", encoding = 'utf_8_sig', index=False)

#拿取使用者所有的post_link
def getUserallpostlink():
    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.clientHeight);")
#     Wait to load page
    time.sleep(1)
    soup = bs(browser.page_source, "html.parser")
    body = soup.find('body')
    #post
    artical_row = body.find_all('div', class_="Nnq7C weEfm")
    for i in artical_row:
        for j in i:
            try:
                print("https://www.instagram.com"+j.find('a').get('href'))
                user_post_link.append("https://www.instagram.com"+j.find('a').get('href'))
            except Exception as e: print(e)
    time.sleep(3)
    for i in range(1,20):
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(1)
        
    soup = bs(browser.page_source, "html.parser")
    body = soup.find('body')
    #post
    artical_row = body.find_all('div', class_="Nnq7C weEfm")
    for i in artical_row:
        for j in i:
            try:
                print("https://www.instagram.com"+j.find('a').get('href'))
                user_post_link.append("https://www.instagram.com"+j.find('a').get('href'))
            except Exception as e: print(e)
            
    return user_post_link 

def login():
    username = '85.photo'
    password = 'a654852654852'
    
    getdriver = ("https://www.instagram.com/accounts/login/")

    browser = webdriver.Chrome('chromedriver')
    browser.implicitly_wait(3)
    browser.get(getdriver)   
    browser.find_element_by_xpath("//input[@name='username']").send_keys(username)
    browser.find_element_by_xpath("//input[@name='password']").send_keys(password)
    browser.find_element_by_xpath("//button//div[text()='登入']").click()
#被標註總數
#def getUserNumofbetages():
#    global numofbetages_row
#    user_betages_url = 'https://www.instagram.com/'+username+'/tagged/?hl=en'
#
#    print(browser.page_source)
#    for i in range(1,1):
#        browser.execute_script('window.scrollTo(0,document.body.scrollHeight);')
#        time.sleep(1)
#    soup = bs(browser.page_source, "html.parser")
#    body = soup.find('body')
#    #被標註
#    numofbetages_row = body.find_all('div', class_="v1Nh3 kIKUG  _bz0w")
#    print(len(numofbetages_row))
#拿取使用者post總數，拿取使用者的(被追蹤)總數，拿取使用者(追蹤)的總數 
def getUserNumofposts():
    user_url2 = user_url
    browser.get(user_url2)
#    print(user_url)
#    time.sleep(1)
    path = '//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/a'
    text = browser.find_element_by_xpath(path).text
#    print(re.sub("\D", "", text))
    userNumofposts.append(re.sub("\D", "", text))
    
    path = '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a'
    text = browser.find_element_by_xpath(path).text
#    print(re.sub("\D", "", text))
    userNumoffollowers.append(re.sub("\D", "", text))
    
    path = '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a'
    text = browser.find_element_by_xpath(path).text
#    print(re.sub("\D", "", text))
    userNumoffollows.append(re.sub("\D", "", text))
       
    return (userNumofposts,userNumoffollowers,userNumoffollows)



#拿取使用者的所有post內文(content)與第i篇post的留言內文(content)與post hasgtags最新一個月內post
def getUserpostcontent():
    global count_response
    global last_post_time
    global one_monthpost_count
    
    
    for page_link in user_post_link:
        post_url = page_link
        browser.get(post_url)
        time.sleep(1)
    #post內文
        try:
            path = '//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul/div/li/div/div/div[2]/span'
            text = browser.find_element_by_xpath(path).text
            allPageContent_list.append(text)
        except Exception as error:
           print(error)
        
    #最新post內文日期
#        datetime = response.xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul/div/li/div/div/div[2]/div/div/time"]/@datetime').extract_first()
#        time = response.xpath('//time[@class="review-date--tooltip-target"]/text()').extract_first()
        try:
            path = '//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul/div/li/div/div/div[2]/div/div/time'
            text = browser.find_element_by_xpath(path).get_attribute("datetime")
        except Exception as error:
           print(error)
        #判斷日期大於一個月之前
        try:
            dt = maya.parse(text).datetime()
            post_time = dt.date()
            post_time_list.append(post_time)
            now = datetime.date.today()
            if(now.__sub__(post_time_list[0]).days < 30):
                one_monthpost_count+=1
#            print(type(last_post_time))
#            print(dt.date())
    #        print(dt.time())
    #        print(dt.tzinfo)
        except Exception as error:
           print(error)
        
    #post按讚數
        #圖片檔post有按讚數
        try:
            text = browser.find_element_by_class_name('Nm9Fw').text
            allPageContentlike_list.append(re.sub("\D", "", text))
        #影片檔post沒有按讚數
        except Exception as error:
            print(error)
            
        
    #留言內文
        all_leave_message = browser.find_elements(By.CLASS_NAME, 'C4VMK')
    
    #初始化每篇post留言
        allleavemessageContent_list = []
        allleavemessageContent=''
    #存取每篇post留言
        for option in all_leave_message[1:]:
#            print(option.text)
#            print('\n\n')
            allleavemessageContent_list.append(option.text)
            #統計留言總數
            count_response += 1
        allleavemessageContent = '\n'.join(allleavemessageContent_list)
        allleavemessageContent_list2.append(allleavemessageContent)
#        print(allleavemessageContent_list2)
#        print('\n\n\n')
        
        
        
    return (allPageContent_list,allleavemessageContent_list2,allPageContentlike_list,count_response,post_time_list,one_monthpost_count)
    





getUserNumofposts()        
getUserallpostlink()
getUserpostcontent()
writeFile()
time.sleep(2)
writeFile2()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        