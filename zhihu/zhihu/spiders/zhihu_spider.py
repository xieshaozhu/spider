# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from bs4 import BeautifulSoup
import json
from zhihu.items import UserItem


class ZhihuSpiderSpider(Spider):
    name = 'zhihu_spider'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    start_user = 'excited-vczh'

    url_user = 'https://www.zhihu.com/people/{user}/following'
    url_follows = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follws_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    url_button = 'https://zhihu-web-analytics.zhihu.com/api/v1/logs/batch'

    def start_requests(self):
        yield Request(self.url_user.format(user=self.start_user), callback=self.parse_user)
        yield Request(self.url_follows.format(user=self.start_user, include=self.follws_query, offset=0, limit=20), callback=self.parse_follows)

    def parse_user(self, response):
        print(response.text)
        soup = BeautifulSoup(response.text, 'lxml')
        url_tokens = soup.select('div ul li a[class="Tabs-link"]')
        url_token = url_tokens[0].get('href').split('/')[2]
        name = soup.select('div h1 span[class="ProfileHeader-name"]')
        personality_signature = soup.select('div h1 span[class="RichText ztext ProfileHeader-headline"]')
        place = soup.select('div[class="ProfileHeader-detailValue"] span')
        personal_profile = soup.select('div[class="RichText ztext ProfileHeader-detailValue"]')
        career_experiences = soup.select('div[class="ProfileHeader-field"] ')
        for career_experience in career_experiences:
            career_experience = '' + str(career_experience) + ','
        yield {
            'url_token': url_tokens[0].get('href').split('/')[2],
            'name': name[0].text,
            'personality_signature': personality_signature[0].text if soup.select('div h1 span[class="RichText ztext ProfileHeader-headline"]') else None,
            'place': place[0].text if soup.select('div[class="ProfileHeader-detailValue"] span') else None,
            'personal_profile': personal_profile[0].text if soup.select('div[class="RichText ztext ProfileHeader-detailValue"]') else None,
            'career_experience': career_experience if soup.select('div[class="ProfileHeader-field"] ') else None
        }
        yield Request(self.url_follows.format(user=url_token, include=self.follws_query, offset=0, limit=20), self.parse_follows)

    def parse_follows(self, response):
        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.url_user.format(user=result.get('url_token')), callback=self.parse_user)

        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield Request(next_page, callback=self.parse_follows)

