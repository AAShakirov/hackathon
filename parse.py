import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


login = int(input('Введите номер студенческого билета: '))
password = input('Введите пароль от moodle: ')
# Указываем путь к драйверу для Chrome
driver_path = f'webdriver\chromedriver.exe'

# Создаем объект веб-драйвера
service = Service(driver_path)
chrome_options = Options()
chrome_options.headless = False
driver = webdriver.Chrome(service=service, options=chrome_options)

# Открываем сайт
driver.get("http://ntb.spbgasu.ru/index.php?C21COM=F&I21DBN=IBIS_FULLTEXT&P21DBN=IBIS&LNG=&Z21ID=")

login_case = driver.find_element(by=By.NAME, value='Z21ID')
login_case.send_keys(login)
password_case = driver.find_element(by=By.NAME, value='Z21FAMILY')
password_case.send_keys(password)

# Находим элемент ссылки на странице и кликаем по ней
link = driver.find_element(by=By.XPATH, value="/html/body/div[3]/table/tbody/tr[1]/td/div[5]/table/tbody/tr/td[5]/table/tbody/tr[1]/td[3]/input[@type='image' and @onclick='uc_logIn(); return false;']")
link.click()

# Получаем HTML страницы и сохраняем в файл
html = driver.page_source
print(html)
time.sleep(5)
# Закрываем браузер
# driver.quit()