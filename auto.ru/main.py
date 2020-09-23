# -*- coding: utf-8 -*-
import datetime
import imaplib
import os
import pickle
import sys
import threading
import warnings
import zipfile
from random import choice, randint
from threading import Thread
from time import sleep, time
from traceback import format_exc
from typing import TextIO

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from twocaptcha import TwoCaptcha


debug = False
Use_Proxy = True
warnings.filterwarnings("ignore")

CAPTCHA_API_KEY = 'f0ef70eefed3b21ecae72c7f0c12961b'


lock = threading.Lock() 
global second_script 
second_script = True


def read_links():
    with open('input/randtext&findlink.txt') as f:
        links = tuple(map(lambda x: x[x.find(':')+1:].strip('\n'), f.readlines()))
    return links


def check_manager(num, link):
    try:
        os.mkdir('products/link_' + str(num))
    except Exception:
        pass

    response_end = requests.get(link).text
    soup_end = BeautifulSoup(response_end, "html.parser")
    e_url = soup_end.find_all("a", class_="ListingPagination-module__page")[-1]['href']
    e = int(e_url[e_url.find('page=')+5:])

    for page in range(1, e+1):
        check(num, link, page)

    print('\nСсылки на все товыры получены')


def check(num, link, page):
    print('Ссылка ' + str(num) + ' - обработка страницы ' + str(page) + ' из 99')
    good_products = []
    html_page = requests.get(link + '&page' + '=' + + 'page}').text
    soup = BeautifulSoup(html_page, "html.parser")
    products = map(lambda x: x['href'].strip(' \n'), soup.find_all("a", class_="ListingItemTitle-module__link"))
    # print(*goods, sep='\n')
    with open('blacklist.txt') as black:
        blacklist = black.read()
    for product in products:
        if not(product in blacklist):
            product_page = requests.get(product).text
            pr_soup = BeautifulSoup(product_page, "html.parser")
            btn = pr_soup.find_all("button", class_="PersonalMessage_type_button")
            sold = pr_soup.find_all('div', class_='CardSold')
            if len(btn) != 0 and len(sold) == 0:
                good_products.append(product)
            else:
                with lock:
                    with open('blacklist.txt', 'a') as black:
                        black.write(product)
                        #print(product, file=black)
    with lock:
        with open('products/link_' + str(num) + '/good_products.txt', 'a') as f:
            f.write(good_products)


def main_pre_action():
    links = read_links()
    th = []
    for num, link in enumerate(links):
        th.append(Thread(target=check_manager, args=(num, link)))
        th[-1].start()
        while len(th) > 5:
            i = 0
            while i < len(th):
                if not th[i].is_alive():
                    th[i].join()
                    del th[i]
                    continue
                i += 1
            sleep(1)
        else:
            for thread in th:
                thread.join()
            break


def end():
    global second_script
    second_script = False


def log_error(error_text=""):
    if error_text != "":
        input(error_text)
    with open('error.txt', 'a') as err_file:
        for s in format_exc().splitlines():
            err_file.write(s)


def read_links():
        with open('input/randtext&findlink.txt') as f:
            return f.write(str(tuple(map(lambda x: x[x.find(':')+1:].strip('\n'), f.readlines()))))


def check_manager(num, link):
    if not os.path.isdir('products/link_' + str(num)):
        os.mkdir('products/link_' + str(num))
    response_end = requests.get(link).text
    soup_end = BeautifulSoup(response_end, 'products/link_' + str(num) + "html.parser")
    e_url = soup_end.find_all("a", class_="ListingPagination-module__page")[-1]['href']
    e = int(e_url[e_url.find('page=')+5:])
    for page in range(1, e+1):
        check(num, link, page)
    print('\nСсылки на все товыры получены')


def check(num, link, page):
    print('Ссылка ' + str(num) + ' - обработка страницы ' + str(page) + ' из 99')
    good_products = []
    html_page = requests.get(link + '&page=' + str(page)).text
	soup = BeautifulSoup(html_page, "html.parser")
	products = map(lambda x: x['href'].strip(' \n'), soup.find_all("a", class_="ListingItemTitle-module__link"))
	with open('blacklist.txt') as black:
		blacklist = black.read()
	with open('products/link_' + str(num) + '/good_products.txt', 'a') as f:
		for product in products:
			if not(product in blacklist):
				product_page = requests.get(product).text
                pr_soup = BeautifulSoup(product_page, "html.parser")
                btn = pr_soup.find_all("button", class_="PersonalMessage_type_button")
                sold = pr_soup.find_all('div', class_='CardSold')
                if len(btn) != 0 and len(sold) == 0:
                    good_products.append(product)
                else:
                    with open('blacklist.txt', 'a') as black:
                        black.write(product)


def main_pre_action():
	links = read_links()
	th = []
	for num, link in enumerate(links):
		if second_script:
			th.append(Thread(target=check_manager, args=(num, link)))
			th[-1].start()
			while len(th) > 5:
				i = 0
				while i < len(th):
					if not th[i].is_alive():
						th[i].join()
						del th[i]
						continue
					i += 1
				sleep(1)
		else:
			for thread in th:
				thread.join()
			break

def end():
	second_script = False

def get_browser():
    chrome_options = webdriver.ChromeOptions()
    plugin_file = get_proxy(*read_proxy())
    chrome_options.add_extension(plugin_file)
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("-start-maximized")
    path = os.path.dirname(os.path.abspath(__file__))
    browser = webdriver.Chrome(os.path.join(path, 'chromedriver'), chrome_options=chrome_options)
    assert isinstance(browser, object)


def get_browser(use_proxy=Use_Proxy, headless=False): # ----------------------------------------------------------------------------------------------PROXY!!!!!!
    chrome_options = webdriver.ChromeOptions()
    if Use_Proxy:
        pluginfile = get_proxy(*read_proxy())
        chrome_options.add_extension(pluginfile)
    chrome_options.add_argument('--log-level=3')

    chrome_options.add_argument("--disable-notifications")
    if not headless:
        chrome_options.add_argument("-start-maximized")
    else:
        chrome_options.add_argument('window-size=640,480')

    path = os.path.dirname(os.path.abspath(__file__))
    browser = webdriver.Chrome(os.path.join(path, 'chromedriver'), chrome_options=chrome_options)
    return browser


def get_credentials(filename):
    with open(filename) as f:
        return f.readlines()
    try:
        credents = []
        with open(filename) as f:
            for line in f.readlines():
                credents.append({'email': line.split()[0], 'pw': line.split()[1]})
        return credents
    except Exception:
        log_error('email и пароль введены некорректно!')
        #print('email и пароль введены некорректно!')
        #input('Для завершения работы введите любой символ... ')
        exit()


def auth(browser, num, login, pw):
    b = time()
    while time()-b < 30:
        while time()-b < 10:
            browser.find_element_by_link_text('Зарегистрироваться')
            try:
                browser.find_element_by_link_text('Зарегистрироваться')
                break
            except Exception:
                log_error('Не найдена элемент "зарегистрироваться"')
                sleep(1)
                pass
        else:
            cur_url = browser.current_url
            browser.get(cur_url)
            continue
    else:
        raise Exception('Время ожидания кнопки "Зарегистрироваться" истекло')

    browser.find_element_by_link_text('Зарегистрироваться').click()
    sleep(3)
    with open('input/i.txt') as f:
        firstname = choice(f.read().split('\n'))
    browser.find_element_by_name('firstname').send_keys(firstname)
    with open('input/f.txt') as f:
        lastname = choice(f.read().split('\n'))
    browser.find_element_by_name('lastname').send_keys(lastname)
    browser.find_element_by_name('login').send_keys(login)
    browser.find_element_by_name('password').send_keys(pw)
    browser.find_element_by_name('password_confirm').send_keys(pw)
    browser.find_element_by_name('phone').send_keys(num[1:])
    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/main/div/div/div/form/div[4]/span/button').click()
    sleep(4)
    try:
        browser.find_element_by_name('phoneCode')
    except Exception:
        log_error('Не найден элемент для ввода кода подтверждения')
        sleep(32)
        browser.find_element_by_link_text('Отправить код sms').click()
        try:
            browser.find_element_by_link_text('Отправить код sms').click()
        except Exception:
            log_error('Не найден элемент "отправить код sms"')
    return login, pw


def get_number():
    url = 'https://sms-activate.ru/stubs/handler_api.php?api_key=e1bfd58294A07360305082d40A929d1d&action=getNumber&service=ya&forward=0&operator=any&country=0'
    r = requests.get(url)
    print('sms activate response is ' + r.text)
    spl = r.text.split(':')
    id_act, num = spl[1], spl[2]
    return id_act, num


def sms_activate(id_act):
    url0 = 'https://sms-activate.ru/stubs/handler_api.php?api_key=e1bfd58294A07360305082d40A929d1d&action=getStatus&id=' + str(id_act)
    begin = time()
    response = requests.get(url0).text
    print('Ожидание кода из sms...')
    while not 'STATUS_OK' in response and time()-begin < 120:
        response = requests.get(url0).text
        print('sms activate response status' + response)
        sleep(2)
    if 'STATUS_OK' in response:
        code = response.split(':')[1]
        print('Получен код:', code)
        return code
    else:
        raise Exception('Сервис sms активации не отвечает')

def complete_activation(browser, code):
    browser.find_element_by_name('phoneCode').send_keys(code)
    sleep(3)
    try:
        browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/main/div/div/div/form/div[3]/div/div[2]/div/div[2]/div[2]/button').click()
        sleep(3)
    except Exception:
        log_error('Не найдена кнопка подтверждения кода активации')

    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/main/div/div/div/form/div[4]/span/button').click()
    sleep(3)
    try:
        browser.find_element_by_xpath('//*[@id="root"]/div/div[1]/div[2]/main/div/div/div[3]/span/a').click()
        sleep(3)
    except:
        log_error('Не найдена ссылка')


def first_browser_action(browser, email=None):
    browser.get('https://auth.auto.ru/login/?r=https%3A%2F%2Fauto.ru%2F')
    sleep(2)
    if email:
        browser.find_element_by_name('login').send_keys(email)
        browser.find_element_by_xpath('//*[@id="app"]/div/div/div/form/div/div[2]/span/button').click()
        return
    browser.find_element_by_class_name('SocialIcon_yandex').click()
    sleep(3)
    windows = browser.window_handles
    browser.switch_to_window(windows[1])
    tryes = 1
    while tryes <= 1:
        try:
            id_act, num = get_number()
            alphavit = 'qwertyuiopasdfghjklzxcvbnm'
            login = choice(alphavit)
            login += num
            for i in range(10):
                login += choice(alphavit)
            pw = 'ivanzubov321654987'
            auth(browser, num, login, pw)
            try:
                sleep(4)
                browser.find_element_by_class_name('error-message')
            except:
                log_error('Не найден элемент текста с ошибкой')
            else:
                try:
                    url = 'https://sms-activate.ru/stubs/handler_api.php?api_key=e1bfd58294A07360305082d40A929d1d&action=setStatus&status=8&id=' + id_act
                    print('sms activate url is ' + url)
                    r = requests.post(url)
                except:
                    log_error('Ошибка при попытке получения номера телефона с sms-activate')
            code = sms_activate(id_act)
            sleep(1)
            complete_activation(browser, code)
            break
        except Exception:
            log_error()

            url = 'https://sms-activate.ru/stubs/handler_api.php?api_key=e1bfd58294A07360305082d40A929d1d&action=setStatus&status=8&id=' + id_act
            print('Проставляем статус ' + url)
            r = requests.post(url)
            print(r.text)
            if 'BAD_STATUS' in r.text:
                code = sms_activate(id_act)
                sleep(1)
                complete_activation(browser, code)
                break
            browser.back()
            assert 'ACCESS_CANCEL' in r.text, 'Отменить активацию номера не удалось'
            tryes += 1
            continue

    login += '@yandex.ru'
    with open('input/emails&passes.txt', 'a') as f:
        f.write(login + pw)
    login = '@yandex.ru'
    try:
        with open('input/emails&passes.txt', 'a') as f:
            f.write(login + pw)
    except:
        log_error('Ошибка при сохранении логина и пароля')

    windows = browser.window_handles
    browser.switch_to_window(windows[0])
    return login, pw

def second_browser_action(browser, code, link):
    browser.find_element_by_xpath('//*[@id="app"]/div/div/div/form/div/div[3]/div[2]/label/div/span/input').send_keys(code)
    sleep(1)
    browser.get(link)


def check_email(email, pw, again=False):
    print(email, pw)
    try:
        mail = imaplib.IMAP4_SSL('imap.' + email.split('@')[1])
        mail.login(email, pw)
        mail.list()
        mail.select('inbox')
        result, data = mail.search(None, "ALL")

        ids = data[0]
        id_list = ids.split()

        latest_email_id = id_list[-1]

        result, data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = data[0][1]
        raw_email_string = raw_email.decode('utf-8')

        ind = raw_email_string.find('code=', raw_email_string.find('https://auth.auto.ru/confirm/?email')) + 7
        code = raw_email_string[ind:ind+6]
    except IndexError:
        code = ''
    except Exception as err:
        try:
            print(err)
            verify_email(email, pw)
            if not again:
                print('Верификация прошла успешно')
                return check_email(email, pw, again=True)
            else:
                raise Exception
        except Exception:
            log_error('Ошибка авторизации email или верифицировать email не удалось')
            with open('badmail.txt', 'a') as f:
                f.writelines(email + pw)
            raise Exception
    return code


def verify_email(email, pw):
    print('Email не верифицирован. Попытка верификации...')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--log-level=3')
    path = os.path.dirname(os.path.abspath(__file__))
    mini_browser = webdriver.Chrome(os.path.join(path, 'chromedriver'), chrome_options=chrome_options)
    mini_browser.get('https://e.mail.ru/login?email=' + email)
    mini_browser.switch_to.frame(mini_browser.find_element_by_class_name('ag-popup__frame__layout__iframe'))
    do = True
    while do:
        try:
            mini_browser.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div/div/form/div[2]/div[2]/div[3]/div/div[1]/button')
            do = False
        except Exception:
            log_error('Не найдена кнопка ')
            sleep(0.1)
            continue
    mini_browser.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div/div/form/div[2]/div[2]/div[3]/div/div[1]/button').click()
    do = True
    while do:
        try:
            mini_browser.find_element_by_name('password')
            do = False
        except Exception:
            log_error('Не найден элемент для ввода пароля')
            sleep(0.1)
            continue
    sleep(1)
    mini_browser.find_element_by_name('password').send_keys(pw)
    sleep(1)
    mini_browser.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div/div/form/div[2]/div/div[3]/div/div[1]/div/button').click()
    try:
        sleep(1)
        mini_browser.find_element_by_xpath('//*[@id="app"]/div/div/form/div[1]/div/img').screenshot('captcha.png')
        try:
            print('Прохождение капчи...')
            code = get_captcha()
        except Exception as err:
            print('Ошибка получения кода капчи.')
            print(err)
            raise Exception
        print('Капча успешно пройдена')
        mini_browser.find_element_by_xpath('//*[@id="app"]/div/div/form/div[1]/div/div/input').send_keys(code)
        mini_browser.find_element_by_xpath('//*[@id="app"]/div/div/form/div[2]/div/div[1]/button').click()

    except Exception as err:
        log_error(err)

    mini_browser.quit()


def get_captcha():
    solver = TwoCaptcha(CAPTCHA_API_KEY)
    params_captcha = {'lang': 'en'}
    result = solver.normal('captcha.png', **params_captcha)
    code = result['code']
    return code


def get_code(email, pw, not_code):
    begin = time()
    while True:
        code = not_code
        while code == not_code:
            if time() - begin > 60:
                return None
            sleep(10)
            try:
                code = check_email(email, pw)
            except:
                raise Exception
        try:
            int(code)
            break
        except Exception:
            log_error("Ошибка интерпретации кода подтверждения")
    return code


def check_logined(browser):
    try:
        sleep(4)
        browser.find_element_by_link_text('Войти')
    except NoSuchElementException:
        return True
    else:
        return False


def save_cookies(browser, email, black_urls):
    try:
        os.mkdir('cookies/' + email)
    except Exception:
       log_error('Ошибка создания папки с куками')
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, 'cookies', email)
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            if email in file:
                os.remove(os.path.join(dirpath, file))
                break

    now = datetime.datetime.now()
    ses_date = str(now.strftime("%d.%m.%Y"))
    log_datetime = now.strftime("%d.%m.%Y-%H:%M").format('utf-8')
    with open("cookies/" + email + "/" + ses_date + "_" + email + ".pkl", "wb") as c:
        pickle.dump(browser.get_cookies() , c)

    L = len(black_urls)
    if L // 10 % 10 == 1:
        end1 = 'й'
    elif L % 10 == 1:
        end1 = 'е'
    elif 2 <= L % 10 <= 4:
        end1 = 'я'
    else:
        end1 = 'й'
    if L == 1:
        end2 = ''
    else:
        end2 = 'ы'
    with open('session_log.txt', 'a', encoding='utf8') as log:
        log.write('[' + log_datetime + ']: Сессия для ' + email + ' была сохранена успешно. Было отправлено ' + L + ' сообщени' + end1 + ' на товар ' + end2 + ' :')
        for url in black_urls:
            log.write(url + '\r\n')
            #print('    ', url, sep='', file=log)
    with open('cookies/' + email +'/' + email + '_log.txt', 'a', encoding='utf8') as log:
        log.write('[' + log_datetime + ']: Сессия для ' + email + ' была сохранена успешно. Было отправлено ' + L + ' сообщени' + end1 + ' на товар' + end2 + ':')
        for url in black_urls:
            log.write(url + '\r\n')
            #print('    ', url, sep='', file=log)
    with open('cookies/' + email + '/datetime.txt', 'w') as d:
        d.write(log_datetime)

def load_cookies(browser, email=None, direct=None):
    try:
        if direct:
            direct = direct.replace('\\\\', '\\')
            with open(direct, "rb") as c:
                cookies = pickle.load(c)
        else:
            path = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(path, 'cookies', email)
            for dirpath, dirnames, filenames in os.walk(path):
                for file in filenames:
                    if email in file:
                        target = file
                        break
            with open("cookies/" + email + "/" + target, "rb") as c:
                cookies = pickle.load(c)

        for cookie in cookies:
            browser.add_cookie(cookie)
    except Exception as err:
        log_error(err)

        try:
            with open("cookies/cookies_" + email + ".pkl", "rb") as c:
                cookies = pickle.load(c)
            for cookie in cookies:
                browser.add_cookie(cookie)
        except Exception as err:
            log_error(str(err) + 'Сессий для ' + email + ' не обнаружено или файл с сессией повреждён')
            browser.close()


def main_action(browser, iterations, text, rand_inserts, dot, text_no, link=None):
    dot = 1
    windows = browser.window_handles
    browser.switch_to.window(windows[0])
    try:
        sleep(3)
        browser.find_element_by_class_name('ChatIndicator_unread')
    except NoSuchElementException:
        log_error(u"Индикатор чата - есть непрочитанные сообщения")
    else:
        try:
            browser.find_element_by_class_name('TopNavigationChatIndicator__icon').click()
            sleep(4)
            with open('input/answer.txt', encoding='utf-8') as ans:
                answers = ans.readlines()
            unreads = browser.find_elements_by_class_name('ChatListItem__unread')
            for i in range(0, len(unreads)):
                try:
                    unread = unreads[i]
                    unread.click()
                    sleep(3)
                    last_msg = browser.find_elements_by_class_name('ChatMessageBubble_sent')[-1].find_element_by_tag_name('div').find_element_by_tag_name('span').find_element_by_tag_name('span').text # -------------------------------
                    prev = '.'
                    ans_dots = 0
                    for i in range(len(last_msg)-1, -1, -1):
                        if last_msg[i] == '.' and prev == '.':
                            ans_dots += 1
                        else:
                            break
                        prev = last_msg[i]
                    answer = answers[ans_dots]
                    browser.find_element_by_class_name('ChatInput__textarea').send_keys(answer)
                    if not debug:
                        browser.find_element_by_class_name('ChatInput__send-button').click()                    #      !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        sleep(2)
                except Exception as err:
                    log_error(str(err))
                sleep(1)
        except Exception as err:
            log_error(err)
        finally:
            browser.find_element_by_class_name('ChatApp__close').click()
            try:
                browser.find_element_by_class_name('ChatApp__close').click()
            except:
                log_error('Не найдена кнопка закрытия чата')

    black_urls = []
    if link:
        goods = browser.find_elements_by_class_name('ListingItemTitle-module__link')

    i = 3
    iterations = randint(*iterations) + 2

    while i <= iterations:
        try:
            write_to_blacklist = True
            rand_text = text
            for j in range(len(rand_inserts)):
                rand_text = rand_text.replace('$$' + str(j) + '$$', choice(rand_inserts[j]))
            rand_text += '.' * dot
            if link:
                goods[i].click()
                windows = browser.window_handles
                browser.switch_to.window(windows[1])
                product = browser.current_url
                with open('blacklist.txt') as black:
                    if product in black.read():
                        iterations += 1
                        write_to_blacklist = False
                        continue

            else:
                try:
                    with open('products/link_' + str(text_no) + '/good_products.txt') as l:
                        products = l.readlines()
                    product = products[0]
                    browser.get(product)
                except Exception:
                    log_error('Ошибка получения списка для рассылки')
            try:
                browser.find_element_by_class_name('ListingCarsFilters-module__container')
            except:
                log_error('Ошибка получения фильтров')
            else:
                continue
            begin = time()
            while time()-begin < 10:
                try:
                    browser.find_element_by_class_name('PersonalMessage_type_button')
                    break
                except NoSuchElementException:
                    sleep(0.5)
            try:
                browser.find_element_by_class_name('CardSold')
                iterations += 1
                continue
            except Exception:
                log_error('Ошибка получения элемента "Машина продана"')
            browser.find_element_by_class_name('PersonalMessage_type_button').click()
            sleep(3)
            begin = time()
            while time()-begin < 7:
                try:
                    browser.find_element_by_class_name('ChatInput__textarea')
                    break
                except NoSuchElementException:
                    browser.find_element_by_class_name('PersonalMessage_type_button').click()
                    sleep(3)
            else:
                raise(NoSuchElementException)
            sleep(1)
            if not debug:
                browser.find_element_by_class_name('ChatInput__textarea').send_keys(rand_text)
                browser.find_element_by_class_name('ChatInput__send-button').click()
                sleep(2)
                begin = time()
                while time()-begin < 4:
                    try:
                        browser.find_element_by_class_name('ChatMessageBubble_sent')
                        break
                    except Exception:
                        log_error('Ошибка получения элемента отправки сообщения в чат')
                else:
                    print('Сообщение не отправлено!')
                    write_to_blacklist = False
                    return black_urls

            black_urls.append(product)

        except NoSuchElementException:
            print('Похоже, для данного аккаунта ограничена отправка сообщений. Переход к следующему...')
            write_to_blacklist = False
            return black_urls
        except IndexError:
            break
        except Exception:
            print('Произошла непредвиденная ошибка. Досрочное сохранение сесии...')
            write_to_blacklist = False
            log_error()
            return black_urls

        finally:
            if write_to_blacklist:
                with lock:
                    if not link:
                        with open('products/link_' + str(text_no) + '/good_products.txt', 'w') as products_file:
                            try:
                                l.write(*products[1:])
                                products_file.write(product)
                            except:
                                log_error('Ошибка записи сущности в список сущностей good_products.txt')
                    with open('blacklist.txt', 'a') as black:
                        black.write(product.strip(' \n'))

            try:
                windows = browser.window_handles
                if len(windows) > 1:
                    browser.close()
                browser.switch_to.window(windows[0])
            except Exception:
                log_error('Ошибка при переключении между окнами')

            i += 1
    sleep(3)
    return black_urls

def get_randtexts(mode):
    try:
        texts, rand_inserts, dots = [], [], []
        if mode == 2:
            link = line[two_dots+1:]

        assert text.count('{') == text.count('}')
        rand_count = text.count('{')
        rand_insert = [() for i in range(rand_count)]
        for i in range(rand_count):
            b = text.find('{')
            e = text.find('}')
            rand_insert[i] = text[b+1:e].split('|')
            try:
                text = text[:b] + '$$' + str(i) + '$$' + text[e+1:]
            except Exception:
                text = text[:b] + '$$' + str(i) + '$$'

        texts.append(text)
        rand_inserts.append(rand_insert)
        return texts, rand_inserts, [] #dots

    except Exception as err:
        log_error(str(err) + 'Файл "input/randtext&findlink.txt" содержит некорректную ссылку или формат рандомного текста, или файл с данными отсутствует!')
        exit()
    if mode == 2:
        return texts, rand_inserts, dots, links
    return texts, rand_inserts, dots


def check_randtext(texts, rand_inserts):
    for text, rand_insert in zip(texts, rand_inserts):
        rand_text = text
        for j in range(len(rand_insert)):
            rand_text = rand_text.replace('$$' + str(j) + '$$', choice(rand_insert[j]))
        print('Один из возможных вариантов рандомного текста:')
        #print(rand_text)


def get_iterations_and_acc():
    with open('input/count.txt') as f:
        acc, iterations = f.read().split(':')
        acc = int(acc)
        iterations = list(map(int, iterations.split('-')))
        return iterations, acc

def get_cookies_emails():
    emails_with_time = []
    emails_without_time = []
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, 'cookies')
    for dirpath, dirnames, filenames in os.walk(path):
        for email in dirnames:
            for dirpath2, dirnames2, filenames2 in os.walk(os.path.join(dirpath, email)):
                if 'datetime.txt' in filenames2:
                    with open(os.path.join(dirpath2, 'datetime.txt')) as d:
                        file_date = datetime.datetime.strptime(d.read(), "%d.%m.%Y-%H:%M")
                    has_time = True
                else:
                    try:
                        file_date = datetime.datetime.strptime(filenames2[0].split('_')[0], "%d.%m.%Y")
                    except:
                        file_date = datetime.datetime.strptime(filenames2[1].split('_')[0], "%d.%m.%Y")
                    has_time = False
                break
            if has_time:
                emails_with_time.append((file_date, email))
            else:
                emails_without_time.append((file_date, email))
    emails_with_time.sort(key=lambda x: x[0])
    emails_without_time.sort(key=lambda x: x[0])
    emails = emails_without_time + emails_with_time
    emails = list(map(lambda x: x[1], emails))
    return emails


def main():
    mode = 1
    headless = False

    if mode == 1:
        texts, rand_inserts, dots = get_random_texts(mode)
        iterations, acc = get_iterations_and_acc()
        check_randtext(texts, rand_inserts)
        th = Thread(target=main_pre_action)
        th.start()
        sleep(5)

        text_no = 0
        sent_messages_by_link = 0
        i = 0
        while i < acc:
            text, rand_insert = texts[text_no], rand_inserts[text_no]
            print(str(i + 1) + ' Создание нового аккаунта Яндекс...')
            browser = get_browser()
            login, pw = first_browser_action(browser)
            print(str(i + 1) + 'Выполнение основного действия...')
            if not check_logined(browser):
                print('Авторизация не удалась. Сессия для ' + login + ' не создана')
            browser.quit()
            black_urls = main_action(browser, iterations, text, rand_insert, 1, text_no)
            sent_messages_by_link += len(black_urls)
            save_cookies(browser, login, black_urls)
            print(str(i + 1) + ' Готово! Сессия для ' + login + ' успешно сохранена')

            text_no += 1
            i += 1
            browser.quit()
       
        mode = 1
        headless = False
        Use_Proxy = True

        if mode == 1:
            texts, rand_inserts, dots = get_randtexts(mode)
            iterations, acc = get_iterations_and_acc()

            check_randtext(texts, rand_inserts)


            th = Thread(target=main_pre_action)
            th.start()
            sleep(5)

            text_no = 0
            sent_messages_by_link = 0
            i = 0
            while i < acc:
                try:
                    text, rand_insert, dot = texts[text_no], rand_inserts[text_no], dots[text_no]
                    print(str(i + 1) + ' Создание нового аккаунта Яндекс...')
                    browser = get_browser(headless=headless)
                    try:
                        login, pw = first_browser_action(browser)
                    except Exception:
                        continue
                    print(str(i + 1) + 'Выполнение основного действия...')
                    if not check_logined(browser):
                        print('Авторизация не удалась. Сессия для ' + login + ' не создана')
                        browser.quit()
                        continue
                    try:
                        black_urls = main_action(browser, iterations, text, rand_insert, dot, text_no)
                        sent_messages_by_link += len(black_urls)
                        save_cookies(browser, login, black_urls)
                        print(str(i + 1) + ' Готово! Сессия для ' + login + ' успешно сохранена')
                    except Exception:
                        pass
            if text_no >= len(texts):
                text_no = 0
                print('Рассылка сообщений по текущей ссылке завершена. Было отправлено ' + str(sent_messages_by_link) + ' сообщений(я)')
                sent_messages_by_link = 0
    else:
        emails = get_cookies_emails()
        text_no = 0
        sent_messages_by_link = 0
        texts, rand_inserts, dots = get_random_texts(1)
        iterations, acc = get_iterations_and_acc()

        check_randtext(texts, rand_inserts)

        th = Thread(target=main_pre_action)
        th.start()
        sleep(5)

        for email in emails:
            try:
                print('Открытие сессии для ' + email)
                text, rand_insert, dot = texts[text_no], rand_inserts[text_no], 3 #dots[text_no]
                browser = get_browser()
                browser.get('https://auto.ru')
                try:
                    load_cookies(browser, email)
                except Exception:
                    continue
                browser.get('https://auto.ru')
                if not check_logined(browser):
                    print('Сессия для ' + email + ' устарела. Вход не выполнен')
                    browser.quit()
                    text_no += 1
                    continue
                try:
                    black_urls = main_action(browser, iterations, text, rand_insert, dot, text_no)
                    sent_messages_by_link += len(black_urls)
                    save_cookies(browser, email, black_urls)
                    print('Готово! Сессия для ' + email + ' успешно перезаписана')
                except Exception:
                    pass

                text_no += 1
                browser.quit()

            finally:
                if text_no >= len(texts):
                    text_no = 0
                    print('Рассылка сообщений по текущей ссылке завершена. Было отправлено ' + str(sent_messages_by_link) + ' сообщений(я)')
                    sent_messages_by_link = 0

                try:
                    browser.quit()
                    if text_no >= len(texts):
                        text_no = 0
                        print('Рассылка сообщений по текущей ссылке завершена. Было отправлено ' + str(sent_messages_by_link) + ' сообщений(я)')
                        sent_messages_by_link = 0
                except Exception as err:
                    log_error(str(err))
                finally:
                    end()
                    input('Для завершения работы введите любой символ...\n')
                    exit()


def open_for_user(email=None, direct=None):
    try:
        if email:
            print('Открытие сессии для ' + email)
        else:
            print('Открытие сессии для ' + direct)
        browser = get_browser()
        browser.get('https://auto.ru')
        if email:
            load_cookies(browser, email)
        elif direct:
            load_cookies(browser, direct=direct)
        browser.get('https://auto.ru')
        if not check_logined(browser):
            print('Сессия устарела. Вход не выполнен')
            browser.quit()

        input('Для перехода к следующей сессии или выхода, если эта последняя, введите любой символ... ')
        browser.quit()
    except Exception as err:
        print(err)


def read_proxy():
    with open('input/proxy.txt') as f:
        proxy_str = choice(f.readlines())
    proxy_and_port, login, pw = proxy_str.split()
    proxy, port = proxy_and_port.split(':')
    print('Используется прокси:', proxy)
    return proxy, port, login, pw


def get_proxy(host, port, user, password):
    PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS = host, int(port), user, password

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
              },
              bypassList: ["localhost"]
            }
          };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

    pluginfile = 'proxy_auth_plugin.zip'
    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return pluginfile


if __name__ == '__main__':
    args = sys.argv
    welcome_msg = '''
Автоматизатор работы в auto.ru. © Максим Белов
Proxy для сессий должны быть записаны в "input/proxy.txt" в формате "proxy:port login password", каждый адрес с новой строки
Поисковая ссылка и сообщения, которые будут отправлены продавцам, должны быть записаны в "randtext&findlink.txt" в формате: "3.Текст {должен быть|нужен} с {несколькими|некоторым количеством} рандом {вставками|кусками}:findlink", где 3 - количество точек в конце сообщения
Количество создаваемых аккаунтов и диапазон количества объявлений, которые будут обработаны, используя один аккаунт, должен быть записан в "input/count.txt" в формате "количество_аккаунтов:от-до" (например "3:4-6")
Если используется вход по email, то email'ы и пароли должны быть записаны в "input/emails&passes.txt" в формате "email password", каждая пара с новой строки
'''
    if len(args) == 1:
        main()
    elif len(args) == 2:
        new_cwd = args[0].replace('\\\\', '\\')
        new_cwd = new_cwd[:new_cwd.rfind('\\')]
        os.chdir(new_cwd)
        print(welcome_msg)
        try:
            open_for_user(direct=args[1])
        except Exception as err:
            print(err)
        input('Введите любой символ для выхода... ')
