from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
import json


# helper functions
def read_from_json(json_path):
    obj = {}
    with open(json_path, 'r') as f:
        obj = json.load(f)
        try:
            obj["Date"] = str(obj["Date"])
        except TypeError as e:
            print("Date 다음에는 큰 따옴표로 감싸진 8자리 숫자만 넣어 주세요. 예시: \"20200101\"")
        try:
            obj["Departure_time"] = str(obj["Departure_time"])
        except TypeError as e:
            print("Departure_time 다음에는 큰 따옴표로 감싸진 2 자리 짝수 숫자만 넣어 주세요. 예시: \"00\", \"02\", \"00\",\"18\"")
        try:
            obj["phone_number"] = str(obj["phone_number"])
        except TypeError as e:
            print("phone_number 다음에는 큰 따옴표로 감싸진 전화번호만 넣어 주세요. 그리고 -를 쓰지 마세요. 예시: \"01012345678\"")
    return obj


def xpath_gen(kind_seat, place_num):
    if kind_seat == 'standard':
        xpath = f'//*[@id="result-form"]/fieldset/div[6]/table/tbody/tr[{place_num + 1}]/td[7]/a'
    elif kind_seat == 'special':
        xpath = f'//*[@id="result-form"]/fieldset/div[6]/table/tbody/tr[{place_num + 1}]/td[6]/a'
    else:
        print('wrong input')

    return xpath


def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


# ================== Initial Settings ===========================
# basic configuration
reservation_site_add = 'https://etk.srail.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000'
site_add = 'https://etk.srail.kr/cmc/01/selectLoginForm.do?pageId=TK0701000000'
driver_path = './chromedriver'

config_path = "./config.txt"
config = read_from_json(config_path)
# User info
phone_number = config["phone_number"]
passwd = config['passwd']

# Travel info ==================================
city_from = config['From']
city_to = config["To"]
date = config["Date"]
departure_time = config["Departure_time"]
from_item = config["From_item"]
num_items = config["num_item"]



# =============================================
def goto_reserv_site():
    driver.get(reservation_site_add)
    departure = driver.find_element(By.XPATH, '//*[@id="dptRsStnCdNm"]')
    arrival = driver.find_element(By.XPATH, '//*[@id="arvRsStnCdNm"]')

    departure.clear()
    departure.send_keys(city_from)
    arrival.clear()
    arrival.send_keys(city_to)

    departure_date_selector = Select(driver.find_element(By.XPATH, '//*[@id="dptDt"]'))
    departure_date_selector.select_by_value(date)

    departure_time_selector = Select(driver.find_element(By.XPATH, '//*[@id="dptTm"]'))
    departure_time_selector.select_by_visible_text(departure_time)

    querry_btn = driver.find_element(By.XPATH, '//*[@id="search_top_tag"]/input')
    querry_btn.submit()


if __name__ == '__main__':
    # load driver
    chrome_options = Options()
    driver = Chrome(options=chrome_options, executable_path= driver_path)

    # open login site
    driver.get(site_add)
    print('dones')

    # print(driver.current_url)
    # login

    phone_num_login = driver.find_element(By.ID, 'srchDvCd3')
    phone_num_login.click()
    print('clicked')

    input_phone_num = driver.find_element(By.CSS_SELECTOR, 'input#srchDvNm03.input')
    print('found phone num input')
    input_phone_num.send_keys(phone_number)

    input_passwd = driver.find_element(By.CSS_SELECTOR, 'input#hmpgPwdCphd03.input')
    input_passwd.send_keys(passwd)

    submit_btn = driver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[1]/div[1]/div[4]/div/div[2]/input')
    submit_btn.submit()

    goto_reserv_site()
    xpath_list = [xpath_gen('standard', i) for i in range(from_item, from_item + num_items)]
    # print(xpath_list)
    prev_address = driver.current_url
    print(driver.current_url)

    while (1):
        for xpath in xpath_list:
            if check_exists_by_xpath(driver, xpath):
                # print('XPATH AVAILABLE---------------------------')
                driver.find_element(By.XPATH, xpath).click()

        # print('prev add: ', prev_address)
        # print('curr add: ', driver.current_url)

        if (prev_address == driver.current_url) or ((prev_address + '#none') == driver.current_url):
            print('not reserved')
            time.sleep(0.4)
            driver.refresh()

        else:
            print('=' * 30)
            print('--------------------- Reservation complete! --------------------------')
            print('=' * 30)
            time.sleep(60 * 10)
            goto_reserv_site()
            prev_address = driver.current_url
            print(driver.current_url)
            print("Retry Reservation...")
