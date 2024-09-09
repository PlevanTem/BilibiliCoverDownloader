from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os

def get_cover_url(driver, video_id):
    base_url = 'https://www.jijidown.com/video/'
    driver.get(base_url+format_video_id(video_id))
    
     # 等待iframe元素可见
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "iframe"))
    )
    
    # 切换到iframe
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)
    
    # 等待封面下载链接元素可见
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "a.download"))
    )
    
    # 获取封面链接
    download_link = driver.find_element(By.CSS_SELECTOR, "a.download").get_attribute('href')
    
    return download_link

def download_covers(video_ids, save_dir):
    try:
        response = requests.get(cover_url)
        if response.status_code == 200:
            filename = f'{format_video_id(video_id)}.jpg'
            filepath = os.path.join(save_dir, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"封面已保存到 {filepath}")
        else:
            print(f"封面下载失败，状态码：{response.status_code}")
    except requests.RequestException as e:
        print(f"封面下载过程中发生错误：{e}")