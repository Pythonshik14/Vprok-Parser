import pandas as pd
from bs4 import BeautifulSoup
import requests
from vprok import data
from string import punctuation
from lxml import etree
import lxml.html

def delete(r):
	res = []
	for i in r:
		if i != '':
			res.append(i)
	return res

def textt(soup):
	return [i.replace("\n", "").strip() for i in soup if i.replace("\n", "").strip() != '']

def ParserVprok():

	global data
	

	AllData = {
	"Category":[],
	"Name":[],
	"OldPrice":[],
	"NewPrice":[],
	"Measure":[]
	}

	head = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; rv:88.0) Gecko/20100101 Firefox/88.0"}

	print(len(data))
	
	START = 0
	COUNT = 200

	while COUNT < 3348:

		for url in data[START:COUNT]:
			
			try:
				response = requests.get(url, headers=head)

				if response.status_code == 200:

					tree = lxml.html.document_fromstring(response.text)

					soup = BeautifulSoup(response.text, "lxml")

					result_not = []
					result_notFalse = []

					DIV_INFORMATION = tree.xpath('//div[@data-owox-product-name and @data-owox-is-available=1]')

					allNames = tree.xpath('//div[@data-owox-is-available=1]/@data-owox-product-name')

					for na in range(len(DIV_INFORMATION)):

						try:
							sssOup = BeautifulSoup(etree.tostring(DIV_INFORMATION[na], method='html', with_tail=False), "lxml")
							
							if sssOup.find("div", class_="xf-price xf-product-cost__current js-product__cost") == None or sssOup.find("p", class_="xf-product-discount js-calculated-discount") != None:
								result_not.append(allNames[na])
		
							else:
								result_notFalse.append(allNames[na])

						except:
							continue

					categorySS = [soup.find("h1", class_="xf-products-section__title").text] * (len(result_notFalse) + len(result_not)) 


					just = tree.xpath('//div[@class="xf-product__cost xf-product-cost "]/div[@class="xf-price xf-product-cost__current js-product__cost "]/@data-cost')
					just_meas = tree.xpath('//div[@class="xf-product__cost xf-product-cost "]/div[@class="xf-price xf-product-cost__current js-product__cost "]/@data-type')

					old = tree.xpath('//div[@class="xf-price xf-product-cost__prev js-product__old-cost"]/@data-cost')

					new = tree.xpath('//div[@class="xf-price xf-product-cost__current js-product__cost  _highlight" or @class="xf-price xf-product-cost__current js-product__cost _highlight _with_old_price"]/@data-cost')
					new_meas = tree.xpath('//div[@class="xf-price xf-product-cost__current js-product__cost  _highlight" or @class="xf-price xf-product-cost__prev js-product__old-cost" or @class="xf-price xf-product-cost__current js-product__cost _highlight _with_old_price"]/@data-type')


					AllData['Category'].extend(categorySS)
					AllData['Name'].extend(result_not)
					AllData['Name'].extend(result_notFalse)


					AllData['OldPrice'].extend(old)
					AllData['OldPrice'].extend(just)
					

					AllData['NewPrice'].extend(new)
					AllData['NewPrice'].extend(['not/app'] * len(just))


					AllData['Measure'].extend(new_meas)
					AllData['Measure'].extend(just_meas)


			except:
				continue

		COUNT += 200
		START += 200

		print(START)

		AllData['OldPrice'] = delete(AllData['OldPrice'])

		df_read = pd.read_csv("VprokData.csv")

		df = pd.DataFrame(AllData)


		together = pd.concat([df_read, df], ignore_index=True)

		together.to_csv("VprokData.csv", index=None)
	

ParserVprok()