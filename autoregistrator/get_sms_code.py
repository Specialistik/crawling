import requests
import time

sms_activator = requests.get("https://sms-activate.ru/stubs/handler_api.php?api_key=56bfe0d6bc9000edefc2AA7400ed8820\",\"&action=getNumber&service=vi&operator=any")
if len(sms_activator.text.split(":")) != 3:
    print('your life sucks')
    print(sms_activator.text)

print(sms_activator.text)
nothing, transaction, phone = sms_activator.text.split(":")

print("the phone is " + phone)
print("the transaction is " + transaction)

sms_request_url = "https://sms-activate.ru/stubs/handler_api.php?api_key=56bfe0d6bc9000edefc2AA7400ed8820&action=getStatus&id=" + str(transaction)
sms_code = requests.get(sms_request_url)

print(sms_request_url)
while sms_code.text == 'STATUS_WAIT_CODE':
    print(sms_code.text)
    time.sleep(30)
    sms_code = requests.get(sms_request_url)

print(sms_code.text)
    