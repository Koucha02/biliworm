import os
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


def download_avatar(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, 'wb') as f:
            f.write(response.content)


def get_user_avatar(driver, user_id):
    try:
        driver.get(f'https://space.bilibili.com/{user_id}')
        try:
            fan_count_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "p.n-data-v.space-fans"))
            )
            fan_count = int(fan_count_element.text.strip())
            if fan_count < 100:
                avatar_element = driver.find_element(By.CSS_SELECTOR, "img.bili-avatar-img")
                avatar_url = avatar_element.get_attribute('src')
                if avatar_url:
                    return avatar_url
        except TimeoutException:
            print(f"超时{user_id}")
        except NoSuchElementException:
            print(f"没这个用户{user_id}")
    except Exception as e:
        print(f"发生错误，不可访问{user_id}: {e}")
    return None


def main(num_users, download_folder):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.set_page_load_timeout(20)

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    count = 0
    while count < num_users:
        user_id = random.randint(1, 10000000)# 假设b站uid的范围
        avatar_url = get_user_avatar(driver, user_id)
        if avatar_url:
            file_path = os.path.join(download_folder, f'{user_id}.jpg')
            download_avatar(avatar_url, file_path)
            print(f"成功下载{user_id}，路径: {file_path}")
            count += 1
        driver.delete_all_cookies()

    driver.quit()


num_users = 10 #想要访问的数量
download_folder = './img'
main(num_users, download_folder)
