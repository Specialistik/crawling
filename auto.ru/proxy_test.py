import requests

proxies = {
  'http': '163.172.11.160:3838',
}

r = requests.get('https://auth.auto.ru/login/') #, proxies=proxies)
print(r.content)