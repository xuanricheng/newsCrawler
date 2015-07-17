import scrapy
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from pyvirtualdisplay import Display
import re

class yahooSpider(scrapy.Spider):
    name = 'yahooNews'
    allowed_domains = ['yahoo.com']
    start_urls = ["http://news.yahoo.com/"]
    
    def __init__(self):
        # Virtual Display for Running Selenium
        self.display = Display(visible=0, size=(1280, 1024))
        self.display.start()
        profile = webdriver.FirefoxProfile()
        profile.native_events_enabled = True
        self.driver = webdriver.Firefox(profile)
        #self.driver = webdriver.Firefox()
    
    def addNews(self):
        #add news
        actions = ActionChains(self.driver)
        next = self.driver.find_element_by_xpath('//div[@id="Main"]//ul/li[@class = "next-batch notice loading"]')
        actions.click(next)
        actions.perform()
        
    def parse(self, response):
        self.driver.get("http://news.yahoo.com/")
        try:
            
            newsList = self.driver.find_elements_by_xpath('//div[@id="Main"]//ul/li/div[@class = "wrapper cf"]')
            print len(newsList)
            self.addNews()
            newsList = self.driver.find_elements_by_xpath('//div[@id="Main"]//ul/li/div[@class = "wrapper cf"]')
            print len(newsList)
            self.addNews()
            for news_item in  newsList:
                news_title = news_item.find_element_by_xpath('.//div[@class = "body-wrap"]/h3/a').text
                #print news_title
        except:
            raise
        finally:
            if self.driver != None:
                self.driver.close()
                self.driver.quit()
            if self.display != None:
                self.display.stop()
        '''for i in range(100):
            next = self.driver.find_element_by_xpath('//div[@id="Main"]//ul/li[@class = "next-batch"]/button')
            next.click()
        for item in  self.driver.find_element_by_xpath('//div[@id="Main"]//ul/li/div[@class = "wrapper cf"]'):
            title = item.xpath('.//div[@class = "body-wrap"]/h3/a/text()').extract()
            print title
        '''

	'''for item in  response.xpath('//div[@id="Main"]//ul/li/div[@class = "wrapper cf"]'):
	    #title = item.xpath('//h3/a/text()').extract()
	    #link = item.xpath('//h3/a/@href').extract()
	    #print len(title)
            #print item.extract()
            title = item.xpath('.//div[@class = "body-wrap"]/h3/a/text()').extract()
            print title
            #yield scrapy.Request( callback = self.parse_news)
	    '''
    def parse_news(self, response):
        yield scrapy.Request(news_link.extract(), callback = self.parse_news)
