import requests

url = "https://old.spbgasu.ru/Abiturientam/Dni_otkrytyh_dverey/Registraciya_na_dni_otkrytyh_dverey/"
data = {"ajax": 1,
        "fullname": "Иванов Иван Иванович",
        'edu-level': '11 б',
        'tel': '89999999999',
        'email': '123456@mail.ru',
        'event-type': 1,
        'event-name': 5,
        'event-date': 149,
        'agreement': True,
        'privacy': True,
        'submit': 'submit'
        }

response = requests.post(url, json=data)
print(response.text)

# ajax=1&fullname=Иванов Иван Иванович&edu-level=11 б&tel=89999999999999&email=123456@mail.ru&event-type=1&event-name=5&event-date=149&agreement=true&privacy=true&submit=submit