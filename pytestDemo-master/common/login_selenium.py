from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from api.user import api_fe_url
import threading


def login_page(account,password):
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        brower = Chrome(chrome_options=chrome_options)
        brower.get(api_fe_url)
        sleep(3)
        login_username = brower.find_element_by_xpath('//login//div/ul/li/input[@type="text"]')
        login_username.send_keys(account)
        login_passwd = brower.find_element_by_xpath('//login//div/ul/li/input[@type="password"]')
        login_passwd.send_keys(password)
        brower.find_element_by_xpath('//div//ul/li//span').click()
        sleep(30)
        brower.close()
    except Exception as e:
        print("登录错误，错误是：", e)

def thread_login():
    user_list = ["镭速,leisu1,leisu_test_1@email.com",
                 "镭速,leisu2,leisu_test_2@email.com",
                 "镭速,leisu3,leisu_test_3@email.com",
                 "镭速,leisu4,leisu_test_4@email.com",
                 "镭速测试,leisu5,leisu_test_5@email.com"]
    thread_list = []
    for i in user_list:
        account = i.split(",")[1]
        t = threading.Thread(target=login_page, args=(account, "Test!123",))
        thread_list.append(t)
    for i in thread_list:
        i.start()


if __name__ == "__main__":
    thread_login()