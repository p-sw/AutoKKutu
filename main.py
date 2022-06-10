import json
import sys

from lib.logger import Logger
log = Logger()

for _ in range(3):
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        break
    except ImportError:
        log.warning('Required modules not found.')
        log.info('Installing..')
        import pip
        pip.main(['install', '--disable-pip-version-check', 'wheel'])
        pip.main(['install', '--disable-pip-version-check', '-r', 'requirements.txt'])
        log.success('Successfully installed all modules.')
        log.info('Retrying imports..')
log.success('Successfully imported all modules.')


initial = "https://kkutu.co.kr/o/login/"
current_account = None

with open("account.cfg", "r", encoding="utf-8") as f:
    accountConfig = json.load(f)
    log.success('Successfully loaded account config.')

with open("global.cfg", "r", encoding="utf-8") as f:
    globalConfig = json.load(f)
    log.success('Successfully loaded global config.')

for account in accountConfig:
    if not account["use"]:
        continue
    current_account = account
    initial += account["method"]

if not current_account:
    log.error("No account is available. If you want to use account, please set use to true.")
    sys.exit(1)

log.info(f"Using account:\nLOGIN_METHOD:{current_account['method']}\nACCOUNT_ID:{current_account['account_info']['id']}\nACCOUNT_PW:{current_account['account_info']['password']}")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get(initial)

match current_account['method']:
    case "facebook":
        log.info('Using facebook login method.')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        driver.find_element(By.ID, "email").send_keys(current_account['account_info']['id'])
        driver.find_element(By.ID, "pass").send_keys(current_account['account_info']['password'])
        driver.find_element(By.ID, "loginbutton").click()
    case "naver":
        log.info('Using naver login method.')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "id"))
        )
        driver.find_element(By.ID, "id").send_keys(current_account['account_info']['id'])
        driver.find_element(By.ID, "pw").send_keys(current_account['account_info']['password'])
        driver.find_element(By.ID, "log.login").click()
    case "google":
        # log.info('Using google login method.')
        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.ID, "identifierId"))
        # )
        # driver.find_element(By.ID, "identifierId").send_keys(current_account['account_info']['id'])
        # driver.find_element(By.ID, "identifierNext").click()
        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.NAME, "password"))
        # )
        # driver.find_element_by_name("password").send_keys(current_account['account_info']['password'])
        # driver.find_element(By.ID, "passwordNext").click()
        log.error('Google login method is not supported.')
        sys.exit(1)
    case "kakao":
        log.info('Using kakao login method.')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "id_email_2"))
        )
        driver.find_element(By.ID, "id_email_2").send_keys(current_account['account_info']['id'])
        driver.find_element(By.ID, "id_password_3").send_keys(current_account['account_info']['password'])
        driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[8]/button[1]').click()
    case "twitter":
        log.info('Using twitter login method.')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username_or_email"))
        )
        driver.find_element(By.ID, "username_or_email").send_keys(current_account['account_info']['id'])
        driver.find_element(By.ID, "password").send_keys(current_account['account_info']['password'])
        driver.find_element(By.ID, "allow").click()
log.info('Successfully logged in.')
    
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "kkuko"))
)
driver.get(f"https://kkutu.co.kr/o/game?server={globalConfig['game']['server']}")
