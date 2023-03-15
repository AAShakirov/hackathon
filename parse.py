import requests

login: int = int(input('Input login: '))
password: str = (input('Input password: '))

url = f'http://ntb.spbgasu.ru/irbis64r/php/login_by_ldap.php?samaccountname={login}&password={password}&block_cache=69397810848857&&_=1678865045689'

result = requests.get(url=url)

print(result.text)