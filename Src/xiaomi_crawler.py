import sys
import os
import random
from tqdm import tqdm
current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_dir)
sys.path.append("..")
sys.path.append(".")

from Util.browser_operator import BrowserOperate
from time import sleep
import re

# category example: https://www.wandoujia.com/category/5026
CATEGORY_PREFIX = "https://app.mi.com/category/"
# detail page: https://www.wandoujia.com/apps/6046085
DETAIL_PAGE = "^https:\/\/www\.wandoujia\.com\/apps\/[0-9]+$"
# app link example: https://app.mi.com/details?id=com.starbaba.cheetahcharge
APP_LINK = "^https:\/\/app\.mi\.com\/details\?id\=[a-z\.]+$"

CATEGORY_ITEM = [
    # {
    #     "name": "游戏",
    #     "value": 15
    # },
    # {
    #     "name": "影音视听",
    #     "value": 27
    # },
    {
        "name": "图书阅读",
        "value": 7
    },
    {
        "name": "效率办公",
        "value": 10
    },
    {
        "name": "居家生活",
        "value": 4
    },
    {
        "name": "摄影摄像",
        "value": 6
    },
    {
        "name": "体育运动",
        "value": 8
    },
    {
        "name": "娱乐消遣",
        "value": 13
    },
    {
        "name": "实用工具",
        "value":5
    },
    {
        "name": "聊天社交",
        "value": 2
    },
    {
        "name": "学习教育",
        "value": 12
    },
    {
        "name": "时尚购物",
        "value": 9
    },
    {
        "name": "旅行交通",
        "value": 3
    },
    {
        "name": "医疗健康",
        "value": 14
    },
    {
        "name": "新闻资讯",
        "value": 11
    },
    {
        "name": "金融理财",
        "value": 1
    }
]

class Crawler(object):
    def __init__(self, welcome_link, saving_path):
        self.browser_operator = BrowserOperate(welcome_link, False)
        self.saving_path = saving_path
        self.page_counter = 20
        self.bad_link = []

    def category_hanlder(self):
        '''
        get all of the category page, switch to it and turn to detailed_page_handler
        :return:
        '''
        for item in CATEGORY_ITEM:
            category_link = CATEGORY_PREFIX + str(item["value"])
            category_text = item["name"]
            print("we are handling the " + category_text + ", link: " + category_link)
            self.browser_operator.open_new_window(category_link)
            download_links = set()
            for i in range(self.page_counter):
                url = category_link + "#page=" + str(i)
                print("This is page " + url)
                self.browser_operator.open_new_window(url)
                before_union = len(download_links)
                download_links = download_links.union(self.detail_page_handler())
                add_number = len(download_links) - before_union
                if add_number == 0:
                    break
                self.browser_operator.close_new_window()
            # self.saving_path(category_texts[0], self.detail_page_handler())
            print("before clean: " + str(len(download_links)))
            cleaned = self.get_unique_link(download_links)
            print("after clean: " + str(len(cleaned)))
            self.save_to_file(category_text, cleaned)
            download_links.clear()
            self.browser_operator.close_new_window()

    @staticmethod
    def get_unique_link(download_links: set):
        pkg_filter = list()
        result = set()
        for link in download_links:
            package_name = link[link.find("id")+3: link.find("&")]
            if package_name not in pkg_filter:
                result.add(link)
            pkg_filter.append(package_name)

        return result


    def detail_page_handler(self) -> set:
        items = crawler.browser_operator.browser.find_elements_by_xpath('//*[@id="all-applist"]//*[@href]')
        app_urls = set()
        for item in items:
            href = item.get_attribute("href")
            if bool(re.search(APP_LINK, href)):
                app_urls.add(href)
        download_links = set()
        print("url numbers: " + str(len(app_urls)))
        for url in app_urls:
            if url in self.bad_link:
                print(url + " is a bad link, abort")
                continue
            sleep_time = random.uniform(0.2, 0.8)
            sleep(sleep_time)
            self.browser_operator.open_new_window(url)
            print("we are processing: " + url)
            try:
                download_item = self.browser_operator.browser.find_element_by_xpath('//*[@class="download"]')
            except:
                print("[FAILURE]: fail to load element, we will try another time")
                try:
                    download_item = self.browser_operator.browser.find_element_by_xpath('//*[@class="download"]')
                except:
                    print("[FATAL]: fail to load element in the second time, abort this one")
                    self.browser_operator.close_new_window()
                    self.bad_link.append(url)
                    continue
            download_href = download_item.get_attribute("href")

            download_links.add(download_href + "\n")
            self.browser_operator.close_new_window()
            print("done")

        return download_links

    def save_to_file(self, category_text, links):
        saving_path = self.saving_path + category_text + ".txt"
        links = list(links)
        with open(saving_path, 'w') as f:
            f.writelines(links)

welcome_link = "https://app.mi.com/"
crawler = Crawler(welcome_link, "E:\\PycharmProgram\\APKCrawler\\Data\\xiaomi\\")
crawler.category_hanlder()

# crawler.browser_operator.open_new_window("https://app.mi.com/category/2#page=0")
# links = crawler.browser_operator.get_links_by_re(APP_LINK)
# print("without wating, total number: " + str(len(links)))
# for link in set(links):
#     print(link)
# crawler.browser_operator.close_new_window()
# crawler.browser_operator.open_new_window("https://app.mi.com/category/2#page=0")
# items = crawler.browser_operator.browser.find_elements_by_xpath('//*[@id="all-applist"]//*[@href]')
# links = set()
# for item in items:
#     links.add(item.get_attribute("href"))
# links = set(crawler.browser_operator.get_links_by_re(APP_LINK))
# print("without wating, total number: " + str(len(links)))
# for link in links:
#     print(link)
# crawler.browser_operator.close_new_window()
# crawler.browser_operator.open_new_window("https://app.mi.com/category/2#page=0")
# sleep(10)
# links = set(crawler.browser_operator.get_links_by_re(APP_LINK))
# print("wait 10, total number: " + str(len(links)))
# for link in links:
#     print(link)
# crawler.browser_operator.close_new_window()
# with open("E:\\PycharmProgram\\APKCrawler\\Data\\before_clean.txt", 'r') as f:
#     lines = f.readlines()
#     cleaned = Crawler.get_unique_link(set(lines))
#     print(cleaned)
