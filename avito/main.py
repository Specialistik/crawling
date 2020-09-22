
import requests, os, zipfile, pickle, json, warnings, datetime, sys
from time import sleep, time
from random import choice
from requests.auth import HTTPProxyAuth
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

warnings.filterwarnings("ignore")


def read_proxy():
    with open('input/proxy.txt') as f:
        proxy_str = choice(f.readlines())
    proxy_and_port, login, pw = proxy_str.split()
    proxy, port = proxy_and_port.split(':')
    return proxy, port, login, pw


def get_proxy(host, port, user, password):

    PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS = host, int(port), user, password
##    PROXY_HOST = '185.126.86.108'  # rotating proxy or host
##    PROXY_PORT = 8761 # port
##    PROXY_USER = '100x10z005' # username
##    PROXY_PASS = 'BJXScE' # password


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


def get_proxies():
    global proxy_list
    proxy_list = []
    proxy_str = input()
    while proxy_str:
        login, password = proxy_str.split('@')[0].split(':')
        host, port = proxy_str.split('@')[1].split(':')
        proxy_list.append((host, int(port), login, password))
        proxy_str = input()


def get_browser(use_proxy=True):
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = get_proxy(*read_proxy())
        chrome_options.add_extension(pluginfile)
    chrome_options.add_argument('--log-level=3')

    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("-start-maximized")
##        chrome_options.add_argument("headless") # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    path = os.path.dirname(os.path.abspath(__file__))
    browser = webdriver.Chrome(os.path.join(path, 'chromedriver'), chrome_options=chrome_options)
##    browser = webdriver.Chrome(r'D:\Python_projects\Avito\chromedriver.exe', chrome_options=chrome_options)
    return browser


def get_credentials():
    try:
        credents = []
        with open('input/vk_logins&passes.txt') as f:
            for line in f.readlines():
                credents.append({'vk_login': line.split(':')[0], 'pw': line.split(':')[1]})
        return credents
    except Exception:
        print('логин и пароль введены некорректно!')
        input('Для завершения работы введите любой символ... ')
        exit()


def vk_login(browser, login, pw):
    browser.get('https://www.avito.ru#login?authsrc=h')
    sleep(2)
    do = True
    while do:
        try:
            browser.find_element_by_xpath('/html/body/div[6]/div/div/div/div/span/div/div[1]/div/span[1]')
            do = False
        except NoSuchElementException:
            sleep(0.1)
    browser.find_element_by_xpath('/html/body/div[6]/div/div/div/div/span/div/div[1]/div/span[1]').click()
    windows = browser.window_handles
    browser.switch_to_window(windows[1])
    do = True
    while do:
        try:
            browser.find_element_by_xpath('//*[@id="login_submit"]/div/div/input[6]')
            do = False
        except NoSuchElementException:
            sleep(0.1)
    browser.find_element_by_xpath('//*[@id="login_submit"]/div/div/input[6]').send_keys(login)
    browser.find_element_by_xpath('/html/body/div/div/div/div[2]/form/div/div/input[7]').send_keys(pw)
    try:
        browser.find_element_by_xpath('/html/body/div/div/div/div[2]/form/div/div/button').click()
    except Exception:
        pass
    sleep(2)
    try:
        browser.find_element_by_xpath('//*[@id="oauth_wrap_content"]/div[3]/div/div[1]/button[1]').click()
    except: pass
    print('vk_login completed')


def main_action(browser, link, iterations=None, text=None, rand_inserts=None):
    print('begin main_action')
    black_urls = []

    windows = browser.window_handles
    browser.switch_to.window(windows[0])

    browser.get(link)
    goods = browser.find_elements_by_class_name('item-photo')
    i = 1
    while i <= iterations:
        try:
            rand_text = text
            for j in range(len(rand_inserts)):
                rand_text = rand_text.replace(f'$${j}$$', choice(rand_inserts[j]))

            goods[i-1].find_element_by_class_name('js-item-slider').click()
            windows = browser.window_handles
            browser.switch_to.window(windows[1])

            url = browser.current_url
            with open('blacklist.txt') as blacklist:
                if url in blacklist.readlines():
                    browser.close()
                    windows = browser.window_handles
                    browser.switch_to.window(windows[0])
                else:
                    black_urls.append(url)

            do = True
            b = time()
            while do and time()-b < 5:
                try:
                    browser.find_element_by_xpath('/html/body/div[3]/div[1]/div[3]/div[3]/div[2]/div[1]/div/div[2]/div/div[3]/span/div/button')
                    do = False
                except NoSuchElementException:
                    sleep(0.1)
            browser.find_element_by_xpath('/html/body/div[3]/div[1]/div[3]/div[3]/div[2]/div[1]/div/div[2]/div/div[3]/span/div/button').click()
            sleep(2)
            try:
                browser.find_element_by_class_name('input-input-25uCh')
            except Exception as ex:
                print(ex)
            else:
                id_act, num = get_number()
                auth(browser, num)
                code = sms_activate(id_act)
                print(code)
                sleep(1)
                complete_activation(browser, code)
            b = time()
            do = True
            while do and time()-b < 3:
                try:
                    browser.find_element_by_xpath('/html/body/div[5]/div/div/msgr-reset/div/div[4]/form/div[2]/textarea')
                    do = False
                except NoSuchElementException:
                    sleep(0.1)
            browser.find_element_by_xpath('/html/body/div[5]/div/div/msgr-reset/div/div[4]/form/div[2]/textarea').send_keys(rand_text)
            browser.find_element_by_class_name('channel-bottom-base-sendButton-11joRV').click() # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        except NoSuchElementException:
            iterations += 1
            continue

        finally:
            with open('blacklist.txt', 'a') as blacklist:
                blacklist.write(browser.current_url + '\n')

            browser.close()
            windows = browser.window_handles
            browser.switch_to.window(windows[0])

            i += 1

    return black_urls


def auth(browser, num='  '):
    browser.find_element_by_class_name('input-input-25uCh').send_keys(num[1:])
    sleep(1)
    browser.find_element_by_xpath('/html/body/div[5]/div/div/msgr-reset/div/div[3]/div/div/span/div/div[2]/button').click()


def get_number():
    URL = 'https://sms-activate.ru/stubs/handler_api.php?api_key=e1bfd58294A07360305082d40A929d1d&action=getNumber&service=av&forward=0&operator=megafon&country=0'
    r = requests.get(URL)
##    print(r.text)
    spl = r.text.split(':')
    id_act, num, ps = spl[1], spl[2], spl[3]
    return id_act, num


def sms_activate(id_act):
    URL0 = f'https://sms-activate.ru/stubs/handler_api.php?api_key=e1bfd58294A07360305082d40A929d1d&action=getStatus&id={id_act}'

    begin = time()
    response = requests.get(URL0).text
    print('Ожидание кода из sms...')
    while not 'STATUS_OK' in response and time()-begin < 120.0:
        response = requests.get(URL0).text
    if 'STATUS_OK' in response:
        code = response.split(':')[1]
        print('Получен код:', code)
        return code
    else:
        raise Exception('Сервис sms активации не отвечает')


def complete_activation(browser, code):
    print(code)
    browser.find_element_by_class_name('input-input-25uCh').send_keys(code)
    sleep(1)
    browser.find_element_by_xpath('/html/body/div[5]/div/div/msgr-reset/div/div[3]/div/div/span/div/div[2]/div/button').click()


def save_cookies(browser, login, black_urls):
    try:
        os.mkdir(f'cookies/{login}')
    except Exception:
        pass
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, 'cookies', login)
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            if login in file:
                os.remove(os.path.join(dirpath, file))
                break

    now = datetime.datetime.now()
    ses_date = str(now.strftime("%d.%m.%Y"))
    log_datetime = str(now.strftime("%d.%m.%Y-%H:%M"))
    with open(f"cookies/{login}/{ses_date}_{login}.pkl", "wb") as c:
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
        print((f'[{log_datetime}]: Сессия для {login} была сохранена успешно. Было отправлено {L} сообщени{end1} на товар{end2}:'), file=log)
        for url in black_urls:
            print('    ', url, sep='', file=log)
    with open(f'cookies/{login}/{login}_log.txt', 'a', encoding='utf8') as log:
        print((f'[{log_datetime}]: Сессия для {login} была сохранена успешно. Было отправлено {L} сообщени{end1} на товар{end2}:'), file=log)
        for url in black_urls:
            print('    ', url, sep='', file=log)
    with open(f'cookies/{login}/datetime.txt', 'w') as d:
        d.write(log_datetime)


def load_cookies(browser, login=None, direct=None):
    try:
        if direct:
            direct = direct.replace('\\\\', '\\')
            print('new direct: ', direct)
            with open(direct, "rb") as c:
                cookies = pickle.load(c)
        else:
            path = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(path, 'cookies', login)
            for dirpath, dirnames, filenames in os.walk(path):
                for file in filenames:
                    if login in file:
                        target = file
                        break
            with open(f"cookies/{login}/{target}", "rb") as c:
                cookies = pickle.load(c)

        for cookie in cookies:
            browser.add_cookie(cookie)
    except Exception:
        try:
            with open(f"cookies/cookies_{login}.pkl", "rb") as c:
                cookies = pickle.load(c)
            for cookie in cookies:
                browser.add_cookie(cookie)
        except Exception:
            print(f'Сессий для {login} не обнаружено')
            browser.close()


def get_links_and_randtexts():
    try:
        links, texts, rand_inserts = [], [], []
        with open('input/randtext&findlink.txt', encoding='utf8') as f:
            for line in f.readlines():
                two_dots = line.find(':')
                text = line[:two_dots]
                link = line[two_dots+1:]

                assert text.count('{') == text.count('}')
                assert int(requests.get(link).status_code) == 200

                rand_count = text.count('{')
                rand_insert = [() for i in range(rand_count)]
                for i in range(rand_count):
                    b = text.find('{')
                    e = text.find('}')
                    rand_insert[i] = text[b+1:e].split('|')
                    try:
                        text = text[:b] + f'$${i}$$' + text[e+1:]
                    except Exception:
                        text = text[:b] + f'$${i}$$'

                texts.append(text)
                links.append(link)
                rand_inserts.append(rand_insert)

    except Exception as err:
        print('Файл "input/randtext&findlink.txt" содержит некорректную ссылку или формат рандомного текста, или файл с данными отсутствует!')
        print(err)
        input('Для завершения работы введите любой символ... ')
        exit()

    return links, texts, rand_inserts


def check_randtext(text, rand_inserts):
    rand_text = text
    for j in range(len(rand_inserts)):
        rand_text = rand_text.replace(f'$${j}$$', choice(rand_inserts[j]))
    print('Один из возможных вариантов рандомного текста:')
    print(rand_text)
    input('Если представленный текст отличается от ожидаемого, значит формат его ввода некорректен, и чтобы его исправить следует закрыть программу и внести изменения в "random_text.txt". Для продолжения введите любой символ... ')


def get_iterations():
    try:
        with open('input/count.txt') as f:
            iterations = int(f.read())
            assert iterations > 0
    except Exception:
        print('Некорректное число, или файл с ним отсутствует!')
        input('Для завершения работы введите любой символ... ')
        exit()

    return iterations


def get_cookies_logins(use_date):
    with open('input/date.txt') as f:
        date_str = f.read()

    b_and_e = date_str.split('-')
    e = None
    if len(b_and_e) == 2:
        b, e = b_and_e
        b = datetime.datetime.strptime(b, "%d.%m.%Y")
        e = datetime.datetime.strptime(e, "%d.%m.%Y")
    elif len(b_and_e) == 1:
        b = b_and_e[0]
        b = datetime.datetime.strptime(b, "%d.%m.%Y")
    else:
        b = None
    if use_date:
        print(f'Поиск сессий, датированных от {b.strftime("%d.%m.%Y")} до {e.strftime("%d.%m.%Y")}')

    logins = []
    logins_with_time = []
    logins_without_time = []
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, 'cookies')
    for dirpath, dirnames, filenames in os.walk(path):
        for login in dirnames:
            for dirpath2, dirnames2, filenames2 in os.walk(os.path.join(dirpath, login)):
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
            if not use_date or (e and b <= file_date <= e) or (not e and file_date == b):
                if has_time:
                    logins_with_time.append((file_date, login))
                else:
                    logins_without_time.append((file_date, login))
    logins_with_time.sort(key=lambda x: x[0])
    logins_without_time.sort(key=lambda x: x[0])
    logins = logins_without_time + logins_with_time
    logins = list(map(lambda x: x[1], logins))

    return logins



def main():
    print(welcome_msg)
    try:
        read = True
        while read:
            try:
                mode = int(input('Введите режим работы: 1 - запись сессии, 2 - её чтение: '))
                assert mode == 1 or mode == 2
                read = False
            except Exception:
                print('Введён некорректный режим работы!')

        if mode == 1:
            links, texts, rand_inserts = get_links_and_randtexts()
            iterations = get_iterations()

            credents = get_credentials()
            text_no = 0
            for credent_iter, login_and_pw in enumerate(credents):
                if text_no >= len(links):
                    text_no = 0

                link, text, rand_insert = links[text_no], texts[text_no], rand_inserts[text_no]
                if credent_iter == 0:
                    check_randtext(text, rand_insert)

                login = login_and_pw['vk_login']
                pw = login_and_pw['pw']
                print(f'{credent_iter+1} Выполняется вход с {login}...')

                browser = get_browser(use_proxy=False)

                vk_login(browser, login, pw)

                black_urls = main_action(browser, link, iterations, text, rand_insert)
                save_cookies(browser, login, black_urls)
                print(f'{credent_iter+1} Готово! Сессия для {login} успешно сохранена')

                text_no += 1
                try:
                    browser.quit()
                except:
                    pass


            input('Для завершения работы введите любой символ... ')

        else:
            read = True
            while read:
                try:
                    session_mode = int(input('Что сделать с сессией?: 1 - рассылка сообщений, используя авторизацию по сессии, 2 - открыть её в браузере для пользователя: '))
                    assert session_mode == 1 or session_mode == 2
                    read = False
                except Exception:
                    print('Введён некорректный режим работы!')

            read = True
            while read:
                try:

                    use_date = int(input('Какие сессии открыть: 1 - сессии для логинов, которые соответствуют дате или периоду, записанному в "date.txt", 2 - все сохранённые сессии: '))
                    assert use_date == 1 or use_date == 2
                    use_date = True if use_date == 1 else False
                    read = False
                except Exception:
                    print('Введён некорректный режим работы!')

            logins = get_cookies_logins(use_date)

##            if len(logins) > 2: #-----------------------------------------------------------------------------------------------------------------------PRE
##                    print('Тестовая версия программы ограничена 2 email. Сократите их количество, чтобы продолжить тестирование')
##                    input('Для завершения работы введите любой символ... ')
##                    exit()

            if session_mode == 1:
                text_no = 0
                links, texts, rand_inserts = get_links_and_randtexts()
                iterations = get_iterations()

                check_randtext(texts[0], rand_inserts[0])

                for login in logins:
                    print(f'Открытие сессии для {login}')
                    if text_no >= len(links):
                        text_no = 0
                    link, text, rand_insert = links[text_no], texts[text_no], rand_inserts[text_no]
                    browser = get_browser(use_proxy=False)
                    browser.get('https://www.avito.ru')
                    load_cookies(browser, login)
                    browser.get(link)
                    black_urls = main_action(browser, link, iterations, text, rand_insert)
                    save_cookies(browser, login, black_urls)

                    print(f'Готово! Сессия для {login} успешно перезаписана')

                    text_no += 1

                    try:
                        browser.quit()
                    except:
                        pass

                input('Для завершения работы введите любой символ... ')

            else:
                for login in logins:
                    open_for_user(login)
                    sleep(1)

    except Exception as err:
        print(err)
##        raise(err) # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        input('Для завершения работы введите любой символ... ')


def open_for_user(login=None, direct=None):
    try:
        if login:
            print(f'Открытие сессии для {login}')
        else:
            print(f'Открытие сессии для {direct}')
        browser = get_browser(use_proxy=False)
        browser.get('https://www.avito.ru')
        if login:
            load_cookies(browser, login)
        elif direct:
            load_cookies(browser, direct=direct)
        browser.get('https://www.avito.ru')

        input('Для перехода к следующей сессии или выхода, если эта последняя, введите любой символ... ')
        browser.quit()
    except Exception as err:
        print(err)


if __name__ == '__main__':
    args = sys.argv
    welcome_msg = '''
Автоматизатор работы в avito.ru. © Максим Белов
ЭТО ТЕСТОВАЯ ВЕРСИЯ ПРОГРАММЫ. ОНА ОГРАНИЧЕНА ОБРАБОТКОЙ ЛИШЬ ДВУХ ЛОГИНОВ И ПРЕДНАЗНАЧЕНА ИСКЛЮЧИТЕЛЬО ДЛЯ ТЕСТОВ
Proxy для сессий должны быть записаны в "input/proxy.txt" в формате "proxy:port login password", каждый адрес с новой строки
Логины и пароли следует писать в файл "input/vk_logins&passes.txt", каждую пару с новой строчки, email и пароль разделять одним пробелом (пароль нужен для только работы в режиме 1).
Поисковая ссылка и сообщения, которые будут отправлены продавцам, должны быть записаны в "randtext&findlink.txt" в формате: "Текст {должен быть|нужен} с {несколькими|некоторым количеством} рандом {вставками|кусками}:findlink"
Количество объявлений, которые будут обработаны, используя один логин, должно быть записано в "input/count.txt"
Если сессия открывается на чтение/дозапись, и планируется использовать фильтр по дате, то дата/период должны быть записаны в "input/date.txt" в формате "ДД.ММ.ГГГГ" (конкретная дата) или "ДД.ММ.ГГГГ-ДД.ММ.ГГГГ" (период)
(Сообщите разработчику, если такой формат Вам неудобен)
'''
    if len(args) == 1:
        main()
    elif len(args) == 2:
        new_cwd = args[0].replace('\\\\', '\\')
        new_cwd = new_cwd[:new_cwd.rfind('\\')]
        os.chdir(new_cwd)
        print(welcome_msg)
        open_for_user(direct=args[1])

