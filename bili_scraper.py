from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException,TimeoutException 

        
def login(driver, url, username, password):
    # 打开登录页面
    driver.get(url)
    try:
        # 等待登录弹窗按钮出现并点击
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "go-login-btn"))
        )
        login_button.click()

        # 等待账号、密码输入框出现
        username_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='请输入账号']"))
        )
        password_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='请输入密码']"))
        )
        # 输入用户名和密码
        username_input.send_keys(username)
        password_input.send_keys(password)

        # 点击登录按钮提交表单
        # 等待登录按钮出现并点击
        login_submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "div.btn_primary"))
        )
        login_submit_button.click()


        # 等待登录过程中可能出现的验证码
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "geetest_panel_next"))
            )
            print("检测到验证码，请手动完成验证。")
            WebDriverWait(driver, 300).until(
                lambda d: d.switch_to.alert and d.switch_to.alert.text == "请完成人机验证"
            ).dismiss()
            print("验证码已手动处理，继续执行脚本。")
        except TimeoutException:
            # 如果没有验证码，继续执行
            pass
        
        # 等待某个登录成功后的元素出现，例如用户头像或用户名
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "bili-avatar"))
        )
        print("登录成功")
        return True
        
    except TimeoutException:
        print("登录过程中某个元素加载超时")
        return False

def get_id_by_JS(driver, url):
    # 打开页面
    driver.get(url)

    # 等待页面加载完成
    driver.implicitly_wait(5)  # 隐式等待，最多等待5秒
   
    # 查找所有具有 data-aid 属性的 <li> 元素
    elements = driver.find_elements(By.CSS_SELECTOR, 'li[data-aid]')

    # 遍历所有找到的元素，并获取它们的 data-aid 属性值
    data_aid_value = []
    for element in elements:
        data_aid_value.append(element.get_attribute('data-aid'))

    # 去除重复id
    ids = list(set(data_aid_value))

    # 返回b站视频id列表
    return ids

def get_all_pages(driver, base_url, username, password):
    base_url = base_url+"?tid=0&keyword=&order=pubdate"
    
    video_ids = []
    current_page = 1
    
    # 登录并获取第一页
    login(driver, base_url, username, password)
    print(f"正在获取第 {current_page} 页的视频ID...")
    video_ids.extend(get_id_by_JS(driver, f'{base_url}&pn={current_page}'))
    
    while True:
        try:
            current_page += 1
              
            # 等待“下一页”按钮元素DOM可见
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "be-pager-next"))
            )
            next_button = driver.find_element(By.CLASS_NAME, "be-pager-next")
            # 检查“下一页”按钮是否禁用
            if "be-pager-disabled" in next_button.get_attribute("class"):
                print("所有页面已获取")
                break
                
            # 获取当前页面的视频ID
            print(f"正在获取第 {current_page} 页的视频ID...")
            video_ids.extend(get_id_by_JS(driver, f'{base_url}&pn={current_page}'))
                
            # 添加延时以避免请求频率过高
            time.sleep(1)  
            # 点击“下一页”按钮
            next_button.click()

        except (NoSuchElementException,TimeoutException):
            # 如果没有找到“下一页”按钮，或者按钮不可点击，则退出循环
            print("未找到下一页按钮或已达到最后一页")
            break
    
    return video_ids
    

