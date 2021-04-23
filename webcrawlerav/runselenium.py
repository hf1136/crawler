#-*-coding:utf-8-*-



from selenium import webdriver

drive = webdriver.Chrome('./')

drive.get('https://www.baidu.com')

html = drive.page_source()

print(html)