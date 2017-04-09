#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import math
import time
from reviewdao import ReviewDAO


class RestaurantReviewCrawler(object):
    def __init__(self):
        chromedriver = './chromedriver'
        self.driver = webdriver.Chrome(chromedriver)

    def move_to_next_url(self, url):
        self.driver.get(url)

    def get_review_number(self):
        span = self.driver.find_elements_by_css_selector("span.cnt.review")
        num_review = int(span[0].text)
        return num_review

    def find_review_more_btn(self):
        self.btn = self.driver.find_element_by_css_selector("button.btn-reivews-more")

    def click_review_more_btn(self,num_review):
        click_count = int(math.ceil((num_review-5)/float(5)))
        self.find_review_more_btn()
        try:
            for i in range(click_count):
                self.btn.send_keys("\n")
                if i != click_count - 1:
                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-reivews-more")))
        except Exception as err:
            print err

    def crawl_restaurant_name(self):
        restaurant_name = ""
        try:
            element = self.driver.find_element_by_css_selector("span.title")
            name = element.find_element_by_css_selector("h1.restaurant_name")
            branch = element.find_element_by_css_selector("p.branch")
            if branch.text:
                restaurant_name = name.text +'-'+ branch.text
            else:
                restaurant_name = name.text
        except Exception as err:
            print err
        finally:
            return {'restaurant_name': restaurant_name}


    def crawl_first_five_reviews(self):
        reviews = []
        try:
            element = self.driver.find_elements_by_css_selector("span.short_review.more_review_bind.review_content")
        finally:
            #print len(element)
            for e in element:
                reviews.append({'review': e.text, 'len_review': len(e.text)})
            return reviews

            #for i in range(len(element)):
            #    print i
            #    print element[i].text

    def crawl_other_reviews(self):
        reviews = []
        try:
            element = WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.review_content.ng-binding")))
        finally:
            #print len(element)
            for e in element:
                reviews.append({'review': e.text, 'len_review': len(e.text)})
            return reviews

            #for i in range(len(element)):
            #    print i
            #    print element[i].text
    def crawl_ratings(self):
        ratings = []
        try:
            element = self.driver.find_elements_by_css_selector("span.icon-rating")
        finally:
            #print len(element)
            for e in element:
                ratings.append({'rating': e.text})
            return ratings

reviewdao = ReviewDAO()

urls = reviewdao.get_urls('urls')
url = iter(urls)

crawler = RestaurantReviewCrawler()
reviews = []

while url:
    try:
        crawler.move_to_next_url(url.next())

        num_review = crawler.get_review_number()
        crawler.click_review_more_btn(num_review)

        restaurant_name = crawler.crawl_restaurant_name()
        temp_reviews = crawler.crawl_first_five_reviews()
        time.sleep(5)
        temp_reviews2 = crawler.crawl_other_reviews()
        temp_ratings = crawler.crawl_ratings()
        temp_reviews.extend(temp_reviews2)
        for i in xrange(len(temp_reviews)):
            temp_reviews[i].update(temp_ratings[i])
            temp_reviews[i].update(restaurant_name)
        reviews.extend(temp_reviews)
        print len(reviews)

    except Exception as err:
        print err
        break

print 'done'
try:
    reviewdao.save_reviews(reviews)
except Exception as err:
    print err


