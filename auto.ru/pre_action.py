from threading import Thread
from bs4 import BeautifulSoup
from time import sleep
import requests, os, threading


lock = threading.Lock()
second_script = True


def read_links():
	with open('input/randtext&findlink.txt', encoding='utf-8-sig') as f:
		links = tuple(map(lambda x: x[x.find(':')+1:].strip('\n'), f.readlines()))
	return links


def check_manager(num, link):
	try:
		os.mkdir(f'products/link_{num}')
	except Exception:
		pass

	response_end = requests.get(link).text
	soup_end = BeautifulSoup(response_end, "html.parser")
	e_url = soup_end.find_all("a", class_="ListingPagination-module__page")[-1]['href']
	e = int(e_url[e_url.find('page=')+5:])
	
	for page in range(1, e+1):
	# for page in range(1, 2):
		check(num, link, page)

	print('\nСсылки на все товыры получены')


def check(num, link, page):
	print(f'Ссылка {num} - обработка страницы {page} из 99')
	good_products = []
	html_page = requests.get(f'{link}&page={page}').text
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
						print(product, file=black)
	with lock:
		with open(f'products/link_{num}/good_products.txt', 'a') as f:
			print(*good_products, sep='\n', file=f)



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
	global second_script
	second_script = False



# main_pre_action()
