import json
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from lib.logger import Logger

initial = "https://kkutu.co.kr/o/login/"
current_account = None

logger = Logger()

with open("account.config", "r", encoding="utf-8") as f:
    accountConfig = json.load(f)

with open("global.config", "r", encoding="utf-8") as f:
    globalConfig = json.load(f)

for account in accountConfig:
    if not account["use"]:
        continue
    current_account = account
    initial += account["method"]

if not current_account:
    logger.error("No account is available. If you want to use account, please set use to true.")
    sys.exit(1)


driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(initial)

match current_account['method']:
    case "facebook":
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        driver.find_element_by_id("email").send_keys(current_account['account_info']['id'])
        driver.find_element_by_id("pass").send_keys(current_account['account_info']['password'])
        driver.find_element_by_id("loginbutton").click()
    case "naver":
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "id"))
        )
        driver.find_element_by_id("id").send_keys(current_account['account_info']['id'])
        driver.find_element_by_id("pw").send_keys(current_account['account_info']['password'])
        driver.find_element_by_id("log.login").click()
    case "google":
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        driver.find_element_by_id("identifierId").send_keys(current_account['account_info']['id'])
        driver.find_element_by_id("identifierNext").click()
        driver.find_element_by_name("password").send_keys(current_account['account_info']['password'])
        driver.find_element_by_id("passwordNext").click()
    case "kakao":
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "id_email_2"))
        )
        driver.find_element_by_id("id_email_2").send_keys(current_account['account_info']['id'])
        driver.find_element_by_id("id_password_3").send_keys(current_account['account_info']['password'])
        driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[8]/button[1]').click()
    case "twitter":
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username_or_email"))
        )
        driver.find_element_by_id("username_or_email").send_keys(current_account['account_info']['id'])
        driver.find_element_by_id("password").send_keys(current_account['account_info']['password'])
        driver.find_element_by_id("allow").click()
    
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "kkuko"))
)
driver.get(f"https://kkutu.co.kr/o/game?server={globalConfig['game']['server']}")
