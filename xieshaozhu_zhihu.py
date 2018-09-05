import requests
from lxml import etree
import time
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
    'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'}
with open("D:\ zhihu.txt",'w',encoding='utf-8') as f:
    for a in range(0, 10):

        url = "https://www.zhihu.com/node/ExploreAnswerListV2?params={%22offset%22:" + str(a*5) + ",%22type%22:%22day%22}"
        data = requests.get(url, headers=headers).text
        s = etree.HTML(data)
        file = s.xpath('/html/body/div')
        time.sleep(3)

        for div in file:
            title = div.xpath("./h2/a/text()")[0].replace("\n", "")
            number = div.xpath("./div/div[1]/a/text()")[0].replace("\n", "")
            author = div.xpath("./div/div[3]/div[1]/span/span[1]/a/text()")
            motto = div.xpath("./div/div[3]/div[1]/span/span[2]/text()")
            data = div.xpath("./div/div[4]/p/a/text()")[0].replace("\n", "")
            comment = div.xpath("./div /div[5]/div/a[2]/i/text()")
            content = div.xpath(".//div/div[4]/div/text()")[0].replace("\n", "")
            print(title,number,author,motto,data,comment,content)
            f.write("{},{},{},{},{},{},{}\n".format(title, number, author, motto, data, comment, content))



