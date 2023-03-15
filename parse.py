# import requests

# login: int = int(input('Input login: '))
# password: str = (input('Input password: '))

# url = f'http://ntb.spbgasu.ru/irbis64r/php/login_by_ldap.php?samaccountname={login}&password={password}&block_cache=69397810848857&&_=1678865045689'

# result = requests.get(url=url)

# print(result.text)

from selenium import webdriver

# Указываем путь к драйверу для Chrome
driver_path = "путь_к_драйверу/chromedriver.exe"

# Создаем объект веб-драйвера
driver = webdriver.Chrome(driver_path)

# Открываем сайт
driver.get("https://example.com")

# Находим элемент ссылки на странице и кликаем по ней
link = driver.find_element_by_link_text("Название ссылки")
link.click()

# Получаем HTML страницы и сохраняем в файл
html = driver.page_source
with open("page.html", "w", encoding="utf-8") as f:
    f.write(html)

# Закрываем браузер
driver.quit()