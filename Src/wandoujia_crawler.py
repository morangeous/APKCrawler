import sys
import os
import random
from tqdm import tqdm
current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_dir)
sys.path.append("..")
sys.path.append(".")

from Util.browser_operator import BrowserOperate
import re
from time import sleep

# category example: https://www.wandoujia.com/category/5026
CATEGORY = "^https:\/\/www\.wandoujia\.com\/category\/50[0-9]{2}$"
# detail page: https://www.wandoujia.com/apps/6046085
DETAIL_PAGE = "^https:\/\/www\.wandoujia\.com\/apps\/[0-9]+$"

class Crawler(object):
    def __init__(self, welcome_link, saving_path):
        self.browser_operator = BrowserOperate(welcome_link, False)
        self.saving_path = saving_path
        self.page_counter = 2

    def category_hanlder(self):
        '''
        get all of the category page, switch to it and turn to detailed_page_handler
        :return:
        '''
        category_links, category_texts = self.browser_operator.get_links_by_re(CATEGORY, True)
        for i in range(len(category_links)):
            print("we are prcessing: " + category_links[i] + " " + category_texts[i])
            self.browser_operator.open_new_window(category_links[i])
            get_more = self.browser_operator.browser.find_element_by_xpath('//*[@id="j-refresh-btn"]')
            for j in range(self.page_counter):
                try:
                    get_more.click()
                except:
                    break

            self.saving_path(category_texts[i], self.detail_page_handler())

            self.browser_operator.close_new_window()

    def detail_page_handler(self) -> set:
        detail_links = self.browser_operator.get_links_by_re(DETAIL_PAGE)
        download_links = set()

        pbar = tqdm(total=len(detail_links))
        for link in detail_links:
            self.browser_operator.open_new_window(link)
            normal_dl_button = self.browser_operator.browser.find_element_by_xpath('//*[@class="normal-dl-btn "]')
            download_links.add(normal_dl_button.get_attribute("href"))
            self.browser_operator.close_new_window()
            sleep_time = random.uniform(1,2)
            sleep(sleep_time)
            pbar.update(1)
        pbar.close()
        sleep(10000)

        return download_links

    def save_to_file(self, category_text, links):
        saving_path = self.saving_path + category_text + ".txt"
        links = list(links)
        with open(saving_path, 'w') as f:
            f.writelines(links)

        # for i in range(len(category_links)):
        #
        #     for j in range(1, self.page_counter + 1):
        #         length_before_append = len(download_links)
        #         new_url = category_links[i] + "list_" + str(j) + ".html"
        #         print("current_url: " + new_url)
        #         self.browser_operator.open_new_window(new_url)
        #         download_link = self.detail_page_handler()
        #         download_links = download_links.union(download_link)
        #         print("close in category handler")
        #         self.browser_operator.close_new_window()
        #         length_after_append = len(download_links)
        #         if length_after_append == length_before_append:
        #             break
        #
        #     # for link in download_links:
        #     #     print(link)
        #
        #     # save as category
        #     self.save_to_file(category_texts[i], download_links)
        #     download_links.clear()


welcome_link = "https://www.wandoujia.com/category/app"
crawler = Crawler(welcome_link, "E:\\PycharmProgram\\APKCrawler\\Data\\wandoujia\\")
crawler.category_hanlder()

# We failed for the anti-crawler can detect me, even though I have changed the ip and geolocation infomation.