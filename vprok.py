from bs4 import BeautifulSoup
import requests

# функция для получения href тега
def hreff(listy):
	url = "https://www.vprok.ru"
	return [url+i['href'] for i in listy]

# создание Базы Данных
def DataBaseVprok():
	url_catalogs = "https://www.vprok.ru/catalog"

	cafile = 'C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python37-32\\lib\\site-packages\\certifi\\cacert.pem'

	url = "https://www.vprok.ru"

	# user-agent 
	head = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; rv:88.0) Gecko/20100101 Firefox/88.0"}
	
	main_page = requests.get(url_catalogs, headers=head).text

	soup = BeautifulSoup(main_page, "lxml")
	categorys = hreff(soup.find_all("a", class_="xf-catalog-categories__link", href=True))
	
	sub_hrefs = []
	for i in categorys: # проходимся по категориям
		sub_page = requests.get(i, headers=head).text

		sub_soup = BeautifulSoup(sub_page, "lxml")
		
		# под категории
		sub_categorys = hreff(sub_soup.find_all("a", class_="xf-filter__item-label xf-ripple js-xf-ripple xf-ripple_gray", href=True))

		# соединяем 2 списка
		sub_hrefs.extend(sub_categorys)

	
	all_hrefs = []
	
	#--------------------------------------------------
	
	for hr in sub_hrefs: # проходимся по каталагом
		
		all_hrefs.extend([hr+f"?attr[rate][]=0&page={i}&sort=rate_desc" for i in range(2, 7)])
		

	all_hrefs.extend(sub_hrefs)
	
	for k in all_hrefs:
		with open("urls.txt", "a") as f:
			f.write(k)

data = DataBaseVprok() 
print(len(data))