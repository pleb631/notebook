from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from pyquery import PyQuery as pq
import requests
import re
import pyautogui
import random
import os
import threading

def judge(browser): #滑动窗口的页面版
    try:
        span_background = browser.find_element(By.XPATH,'//*[@id="nc_1__scale_text"]/span')
        span_background_size = span_background.size
        print(span_background_size)
        
        # 获取滑块的位置
        button = browser.find_element(By.XPATH,'//*[@id="nc_1_n1z"]')
        button_location = button.location
        print(button_location)
        
        # 拖动操作：drag_and_drop_by_offset
        # 将滑块的位置由初始位置，右移一个滑动条长度（即为x坐标在滑块位置基础上，加上滑动条的长度，y坐标保持滑块的坐标位置）
        x_location = span_background_size["width"]
        y_location = button_location["y"]
        print(x_location, y_location)
        action = ActionChains(browser)
        source = browser.find_element(By.XPATH,'//*[@id="nc_1_n1z"]')
        action.click_and_hold(source).perform()
        action.move_by_offset(300, 0)
        action.release().perform()
        print("judge0 success")
    finally:
        time.sleep(3)
        return 0

def judge1(browser): #滑动窗口的弹窗版，遇到就直接叉掉弹窗
    try:
        browser.find_element(By.XPATH,'/html/body/div[11]/div[2]/div').click()
        print("judge1 success")
        time.sleep(2)
    finally:
        return 1


def RandMouseMove():#模拟鼠标轨迹，多线程异步执行，反 反爬虫，，有一定效果，单独用可以从最大爬4个淘宝网页扩大到19个
    while(1):
        BaseTime = 1.5
        BaseScroll = 100
    
        ratio =  random.random()
        h,w = pyautogui.size()
        if ratio>0.5:
            pyautogui.moveTo(random.random()*h, random.random()*w, random.random()*BaseTime,pyautogui.easeInQuad)
        elif ratio>0.25:           
            pyautogui.scroll(int(BaseScroll*random.random()))
        else:
            pyautogui.scroll(int(-BaseScroll*random.random()))
        time.sleep(BaseTime)
    
    
def get_products(browser):
    """
    提取商品主视频
    """
    pattern = r'/(\w*\.mp4)'
    html = browser.page_source
    doc = pq(html)
    items = doc('div.pic-box-inner div.pic a').items() #获取商品

    for item in list(items):
        href = item.attr('data-href')
        if href ==None:
            continue
        if href.startswith(r'//'):
                href = 'http:'+href
        time.sleep(0.5)
        browser.execute_script('window.open("","_blank");') #新建页面，并转入具体商店主页面
        browser.switch_to.window(browser.window_handles[1])
        browser.get(href)
        time.sleep(3)
    
        judge(browser)    #判断滑块验证码
        judge1(browser)
        
        html1 = browser.page_source
        doc1 = pq(html1)
        item1 = list(doc1('div.lib-video video').items())  #获取所有视频所在源代码       
        
        if len(item1)>0 and item1[0].attr('src')==None: #不同页面源码结构不一样，所以提取两次
            item1 = list(doc1('div.lib-video video.lib-video source').items())
            if item1[0].attr('src')==None:
                continue
            
        for v in item1:
            video_url= v.attr('src')
            if video_url.startswith(r'//'):
                video_url = 'http:'+video_url
                
                
            try:#request 访问并下载
                r=requests.get(video_url)
                save_path =re.findall(pattern,video_url)[0]
                os.makedirs('out',exist_ok=True)
                with open("out/"+save_path,'wb') as fp:
	                fp.write(r.content)
                print(f"downloading success with {video_url}")
            finally:
                judge1(browser)
                continue
            
        browser.close()
        browser.switch_to.window(browser.window_handles[0]) 



        

        #save_to_mongo(product)

t1 = threading.Thread(target=RandMouseMove, args=())
t1.setDaemon(True)  #父线进程结束，自动关闭子线程
#t1.start()

n=1   #爬取页面个数
key = '双肩包'

option = webdriver.ChromeOptions()
option.add_argument("--disable-blink-features=AutomationControlled")  #隐藏webdriver
driver = webdriver.Chrome(options=option)
driver.maximize_window()

#登录
driver.get("https://login.taobao.com/member/login.jhtml?spm=3696s.jianhua.0.0.5af911d9M3L3nc&f=top&redirectURL=https%3A%2F%2Fwww.taobao.com%2F")
time.sleep(0.5)
driver.find_element(By.NAME,"fm-login-id").clear()
driver.find_element(By.NAME,"fm-login-id").send_keys('xxxx')
time.sleep(0.5)
driver.find_element(By.NAME,"fm-login-password").clear()
driver.find_element(By.NAME,"fm-login-password").send_keys('xxxx')
time.sleep(0.5)
judge(driver)
driver.find_element(By.XPATH,"//*[@id='login-form']/div[4]/button").click()
time.sleep(10)


driver.find_element(By.NAME,"q").clear()
driver.find_element(By.NAME,"q").send_keys(key)
driver.find_element(By.XPATH,"//*[@id='J_TSearchForm']/div[1]/button").click()

for i in range(n):
    print(f'start page {i+1}')
    get_products(driver)
    time.sleep(5)    
    if i<n-1:
        driver.find_element(By.XPATH,'//*[@id="mainsrp-pager"]/div/div/div/ul/li[8]/a').click()
time.sleep(30)