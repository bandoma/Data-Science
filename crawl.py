from bs4 import BeautifulSoup
from bs4.element import Tag
import requests
import csv
import pandas as pd
import openpyxl
import sys
Title = []
PlantType = []
Hardiness = []
ClimateZones = []
PlantFamily = []
Exposure = []
Season = []
Height = []
Speard = []
WaterNeeds = []
SoilType = []
SoilpH = []
SoilDrainage = []
Characteristics = []
Tolerance = []
GardenUses = []
GardenStyles = []

# sys.stdout.reconfigure(encoding='utf-8')
a = {'Name':Title,'Hardiness': Hardiness,'Climate Zones':ClimateZones,'Plant Type':PlantType,'Plant Family':PlantFamily,
     'Exposure':Exposure, 'Season of Interest': Season, 'Height': Height, 'Spread': Speard, 'Water Needs' : WaterNeeds, 
	 "Soil Type": SoilType, "Soil pH": SoilpH, "Soil Drainage": SoilDrainage, "Characteristics": Characteristics, 
	 "Tolerance": Tolerance, "Garden Uses": GardenUses, "Garden Styles": GardenStyles}
def crawl():
	n = 0
	for i in range(1, 100):
		print(i)
		headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0"} #Đây là một dictionary định nghĩa thông tin về User-Agent. User-Agent là một chuỗi ký tự được gửi cùng với yêu cầu HTTP để định danh trình duyệt hoặc ứng dụng gửi yêu cầu đến máy chủ. 
		#Trong trường hợp này, User-Agent định nghĩa trình duyệt Firefox trên hệ điều hành Ubuntu.
		req = requests.get(f"https://www.gardenia.net/plants/plant-types/shrubs?page={i}", headers=headers)  # lấy nội dung trang web
		content = req.content  # Đoạn này lấy nội dung của yêu cầu HTTP và lưu trữ vào biến content. Nội dung này chứa mã HTML của trang web.
		soup = BeautifulSoup(content, 'html.parser') #Dòng này sử dụng thư viện BeautifulSoup để phân tích cú pháp HTML của nội dung trang web. Biến soup sẽ chứa một đối tượng BeautifulSoup, từ đó chúng ta có thể dễ dàng truy xuất và trích xuất thông tin từ trang web đó.
		links = soup.select(".grid-img > a")	
		for link in links :
			n+=1
			productPage = requests.get("{}".format(link.attrs["href"]) , headers = headers) #Đoạn này gửi một yêu cầu HTTP GET đến URL của sản phẩm, được lấy từ thuộc tính "href" của thẻ <a> trong trang web. Đối tượng link đại diện cho một liên kết đến trang chi tiết của sản phẩm. Yêu cầu được gửi với thông tin User-Agent đã được định nghĩa trước đó.
			productsoup = BeautifulSoup(productPage.content, 'html.parser') #Dòng này tạo một đối tượng BeautifulSoup từ nội dung của trang sản phẩm, lấy từ thuộc tính content của đối tượng productPage. Đối tượng productsoup sẽ chứa mã HTML của trang sản phẩm.
			a['Name'].append(productsoup.select("body > div.container > div.main-body > div.body-heading > h1")[0].contents[0].text.strip()) # tìm tên sản phẩm
			
			print(a['Name'][-1])
			infoRows = productsoup.select("div.d-lg-block > table > tbody > tr")
			img_url = productsoup.select("#carouselExampleControls > div > div > img")[0].attrs["data-src"]
			#carouselExampleControls > div > div > img
			crawl_image(img_url,n)
			for row in infoRows:
				th = row.find_all("th")[0].contents[0].text.strip()
				td = row.find_all("td")[0].contents[0].text.strip()
				if (th == "Garden Uses"):
					content = ""
					aTags = row.find_all("td")[0].find_all('a')
					for aTag in aTags:
						content += aTag.contents[0].text.strip() + ","
					content = content[0:-1]
					a[th].append(content)
					continue
				elif (th == "Garden Styles"):
					content = ""
					aTags = row.find_all("td")[0].find_all('a')
					for aTag in aTags:
						content += aTag.contents[0].text.strip() + ","
					content = content[0:-1]
					a[th].append(content)
					continue
				elif th in a.keys():
					a[th].append(td)
			append_null()
	save()
def crawl_image(img_url, i):
	response = requests.get(img_url)
	if response.status_code != 404:
		fp = open(f'Images/hoa{i}.jpg', 'wb')
		fp.write(response.content)
		fp.close()


def append_null():
	maxx = len(a["Name"])
	for key in a.keys():
		if len(a[key]) < maxx:
			a[key].append(None)

def save():
	
	df = pd.DataFrame.from_dict(a, orient='index')
	df = df.transpose()
	dataset = pd.DataFrame(data=df)
	dataset.to_csv('Shrubs.csv', encoding='utf-8-sig', )

if __name__ == '__main__':
	crawl()
	