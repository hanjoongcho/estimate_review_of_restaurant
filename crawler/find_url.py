#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from reviewdao import ReviewDAO
from selenium import webdriver

class Find_URL(object):
    def __init__(self):
        chromedriver = './chromedriver'
        self.driver = webdriver.Chrome(chromedriver)

    def move_to_next_url(self, url):
        self.driver.get(url)

    def crawl_restaurant_link(self):
        pass_list =[u'카페 / 디저트',u'베이커리']
        link_list = []
        try:
            div = self.driver.find_elements_by_css_selector('div.info')
            d = iter(div)
            for i in range(10):
                try:
                    section = d.next()
                    review_count = int(section.find_element_by_css_selector("span.review_count").text)
                    info = section.find_element_by_css_selector("p.etc")
                    menu = info.find_element_by_tag_name('span').text

                    if (menu not in pass_list) and (review_count> 50) :
                        a = section.find_element_by_tag_name('a')
                        link_list.append(a.get_attribute('href'))

                except Exception as err:
                    break
        finally:
            return link_list


f = Find_URL()
reviewdao = ReviewDAO()
urls = reviewdao.get_urls('find_urls')
url = iter(urls)
link_list = []
temp_link_list = []

while url:
    try:
       f.move_to_next_url(url.next())
       temp_link_list = f.crawl_restaurant_link()
       link_list.extend(temp_link_list)
       print len(link_list)

    except Exception as err:
        break

print 'done'
l = iter(link_list)
while l:
    try:
        reviewdao.save_urls(l.next())
    except Exception as err:
        break








