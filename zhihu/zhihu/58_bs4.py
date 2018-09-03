from bs4 import BeautifulSoup
import requests

def get_links_from(who_sells):
    urls = []
    list_view = 'http://fs.58.com/iphonesj/{}/?PGTID=0d301f15-000d-ee37-6f74-731d74983018&ClickID=1'.format(str(who_sells))
    wb_data = requests.get(list_view)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    for link in soup.select('td.t a.t'):
        urls.append(link.get('href').split('?')[0])
    return urls

def get_itme_info(who_sells=1):
    
    urls = get_links_from(who_sells)
    for url in urls:
        
        wb_data = requests.get(url)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        title = soup.title.text
        date = soup.select('li.time')
        price = soup.select('span.price')
        area = soup.select('div.su_con a')
        data = {
            'title': title,
            'date': date[0].text if soup.select('li.time') else None,
            'price': price[0].text.strip() if soup.select('span.price') else None,
            'area': list(area[0].stripped_strings) if soup.select('div.su_con a') else None,
            'cate': '个人' if who_sells == 0 else '商家',
        }
        print(data)

get_itme_info()



       




