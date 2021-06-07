import sys
import os
current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_dir)
sys.path.append("..")

from .Util.browser_operator import BrowserOperate
import re
from time import sleep

# category example: https://www.wandoujia.com/category/5026
CATEGORY = "^https:\/\/www\.wandoujia\.com\/category\/50[0-9]{2}$"
#

class Crawler(object):
    def __init__(self, welcome_link, saving_path):
        self.browser_operator = BrowserOperate(welcome_link, False)
        self.saving_path = saving_path
        self.page_counter = 20

    def category_hanlder(self):
        '''
        get all of the category page, switch to it and turn to detailed_page_handler
        :return:
        '''
        category_links, category_texts = self.browser_operator.get_links_by_re(CATEGORY, True)
        download_links = set()
        for i in range(len(category_links)):
            print("we are prcessing: " + category_links[i] + " " + category_texts[i])
            for j in range(self.page_counter):
                self.browser_operator

            self.detail_page_handler()
            self.saving_path(category_texts[i], download_links)
            download_links.clear()

    def detail_page_handler(self) -> set:
        pass

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
crawler = Crawler(welcome_link, "hell")
crawler.category_hanlder()