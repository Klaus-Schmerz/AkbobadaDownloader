import pickle
import argparse
import requests
import os
import time
import random
import sys

import multiprocessing
from functools import partial

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

parser = argparse.ArgumentParser()
parser.add_argument("-mode", help="append 모드일 시 로그인할 계정 추가 가능.")
parser.add_argument("-recovery", help="복구모드. 계정에 상관없이 전체 악보 다운로드함.")
args = parser.parse_args()

login_data = []
isRecoveryMode = False
system = os.name

PROXY = ("221.162.70.124:3129", "64.110.83.145:3128")


class akbo:
    def __init__(self, title, maker, position, id, username):
        self.title = title
        self.maker = maker
        self.position = position
        self.id = id
        self.username = username

    def __str__(self):
        return f"{self.title} - {self.maker} / {self.position} / {self.id}"

    def __eq__(self, other):
        return self.id == other.id

    def make_url(self):
        return f"https://www.akbobada.com/home/akbobada/archive/order/pdf/{self.id}{self.username}.pdf"

    def make_file_name(self):
        return f"{self.title} - {self.maker} {self.position} ({self.id}).pdf"


def get_proxy():
    s = requests.Session()
    response = s.get("http://free-proxy.cz/en/proxylist/country/KR/https/ping/all")
    time.sleep(1)



def make_base_path(filename, resp: str):
    if resp == "save":
        return "./"+filename
    elif resp == "local":
        if system == "nt":
            if not os.path.isdir(os.getenv('LOCALAPPDATA')+"/skymj/"):
                os.makedirs(os.getenv('LOCALAPPDATA')+"/skymj/")
            return os.getenv('LOCALAPPDATA')+"/skymj/"+filename
        if system == "posix":
            if not os.path.isdir(os.path.join(os.path.expanduser('~'), '.local', 'share')+"/skymj"):
                os.makedirs(os.path.join(os.path.expanduser('~'), '.local', 'share')+"/skymj")
            return os.path.join(os.path.expanduser('~'), '.local', 'share')+"/skymj/"+filename
    else:
        return "./"+filename


def main(argv, args):
    global login_data
    global isRecoveryMode

    if not os.path.isfile(make_base_path("login_data.p", "local")):
        id = input("아이디를 입력해 주세요: ")
        pw = input("비밀번호를 입력해 주세요: ")

        login_data.append({"id": id, "pw": pw})

        with open(make_base_path("login_data.p", "local"), "wb") as f:
            pickle.dump(login_data, f)

    with open(make_base_path("login_data.p", "local"), 'rb') as f:
        data = pickle.load(f)
        if len(data) == 0:
            id = input("아이디를 입력해 주세요: ")
            pw = input("비밀번호를 입력해 주세요: ")

            login_data.append({"id": id, "pw": pw})

            with open(make_base_path("login_data.p", "local"), "wb") as f:
                pickle.dump(login_data, f)

    # 만약 추가 모드로 실행된다면
    if args.mode == "append":
        with open(make_base_path("login_data.p", "local"), "rb") as f:
            login_data = pickle.load(f)

        id = input("아이디를 입력해 주세요: ")
        pw = input("비밀번호를 입력해 주세요: ")

        login_data.append({"id": id, "pw": pw})

        with open(make_base_path("login_data.p", "local"), "wb") as f:
            pickle.dump(login_data, f)

    elif args.mode == "delete":
        with open(make_base_path("login_data.p", "local"), "rb") as f:
            login_data = pickle.load(f)
        id = input("삭제할 아이디를 입력해 주세요: ")

        for user in login_data:
            if user["id"] == id:
                del login_data[login_data.index(user)]

                with open(make_base_path("login_data.p", "local"), "wb") as f:
                    pickle.dump(login_data, f)
                return
        print("해당하는 아이디를 찾을 수 없습니다.")
        return
    else:
        with open(make_base_path("login_data.p", "local"), "rb") as f:
            login_data = pickle.load(f)

    if args.recovery == "1":
        print("복구모드 진행")
        isRecoveryMode = True

    print(isRecoveryMode)

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(partial(AkbobadaDownloader, isRecoveryMode=isRecoveryMode), login_data)

    print(results)


def create_driver():
    options = Options()
    options.add_argument("headless")

    service = Service(ChromeDriverManager().install())
    # proxy = random.choice(PROXY)
    # webdriver.DesiredCapabilities.CHROME['proxy'] = {
    #     "httpProxy": proxy,
    #     "ftpProxy": proxy,
    #     "httpsProxy": proxy,
    #     "sslProxy": proxy,
    #     "proxyType": "MANUAL"
    # }
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1280, 720)
    return driver


def multiFinding(driver: webdriver, username, isRecoveryMode: bool):
    driver.get("https://www.akbobada.com/mypage/my_order.html")
    wait = WebDriverWait(driver, 2)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

    cookies = driver.get_cookies()
    last_score = None
    if os.path.isfile(make_base_path(f"{username}_last.p", "local")):
        with open(make_base_path(f"{username}_last.p", "local"), 'rb') as f:
            last_score = pickle.load(f)
    else:
        with open(make_base_path(f"{username}_last.p", "local"), 'wb') as f:
            pickle.dump(akbo("test", "test", "bass", "0", username), f)

    scoreList = []

    counter = 1
    while True:
        time.sleep(2)

        driver.execute_script("window.scrollTo(document.documentElement.scrollWidth, 0);")

        entry = driver.find_element(By.TAG_NAME, "table")
        for table in entry.find_elements(By.TAG_NAME, "tbody"):
            title = str()
            maker = str()

            for tag in table.find_elements(By.TAG_NAME, "tr"):
                if tag.get_attribute("class") == "order":
                    title = tag.find_elements(By.TAG_NAME, "td")[1].text
                    maker = tag.find_elements(By.TAG_NAME, "td")[2].text
                elif tag.get_attribute("class") == "sub":
                    spans = [span.text for span in tag.find_elements(By.TAG_NAME, "span")]
                    for span in spans:
                        if span != "B" and 1 < len(span) < 7:
                            position = span
                    id = tag.find_element(By.TAG_NAME, "button").get_attribute("onclick")[8:-1].split(',')[0]
                    score = akbo(title, maker, position, id, username)
                    scoreList.append(score)

                    if not isRecoveryMode:
                        if not last_score:
                            last_score = score
                            with open(make_base_path(f"{username}_last.p", "local"), 'wb') as f:
                                pickle.dump(last_score, f)
                        else:
                            if score == last_score:
                                with open(make_base_path(f"{username}_last.p", "local"), 'wb') as f:
                                    pickle.dump(scoreList[0], f)
                                return
                    else:
                        with open(make_base_path(f"{username}_last.p", "local"), 'wb') as f:
                            pickle.dump(scoreList[0], f)

                    print(score)

                    button = tag.find_element(By.TAG_NAME, "button")
                    actions = ActionChains(driver).move_to_element(button).click()
                    actions.perform()

                    time.sleep(3)
                    popup_windows = driver.window_handles
                    for window in popup_windows:
                        if window != popup_windows[0]:
                            driver.switch_to.window(window)
                            driver.close()
                    driver.switch_to.window(popup_windows[0])

                    download(cookies, username, score)
                else:
                    print("Error:", tag)

        next_button = driver.find_element(By.CLASS_NAME, "btn_next")
        if next_button.get_attribute("class").split(" ")[-1] == "disabled":
            break

        counter += 1
        driver.execute_script(f"showakbo2({str(counter)}, 1, 0)")

    driver.quit()


def download(cookies, username, target: akbo):
    s = requests.Session()
    for cookie in cookies:
        c = {cookie['name']: cookie['value']}
        s.cookies.update(c)

    print(target.id)

    response = s.get(target.make_url(), verify=False)
    time.sleep(4)

    if not os.path.isdir(make_base_path("", "save")+target.position):
        os.mkdir(make_base_path("", "save")+target.position)

    try:
        with open(make_base_path("", "save")+f"{target.position}/"+target.make_file_name(), "wb") as f:
            f.write(response.content)
        print(f"{str(target)} downloaded")
    except Exception as e:
        print(f"Error: {target} - {e}")


def AkbobadaDownloader(user: dict, isRecoveryMode: bool):
    start_time = time.time()
    print(user['id'])
    login_data = user

    driver = create_driver()

    wait = WebDriverWait(driver, 2)

    USERNAME = login_data['id']
    PASSWORD = login_data['pw']

    driver.get("https://www.akbobada.com")
    wait.until(EC.presence_of_element_located((By.ID, "loginGnbForm")))

    inputID = driver.find_element(By.ID, "midAginGnb")
    inputPW = driver.find_element(By.ID, "mpasswordGnb")

    actions = ActionChains(driver).send_keys_to_element(inputID, USERNAME).send_keys_to_element(inputPW,
                                                                                                PASSWORD).send_keys(
        Keys.ENTER)
    actions.perform()

    multiFinding(driver, USERNAME, isRecoveryMode)
    end_time = time.time()

    print(f"{USERNAME} 완료. 걸린 시간: {end_time - start_time}")


if __name__ == '__main__':
    argv = sys.argv
    main(argv, args)