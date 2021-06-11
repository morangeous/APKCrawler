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

# category example: http://www.anzhi.com/sort_45_1_hot.html
CATEGORY_PREFIX = "http://www.anzhi.com/sort_"
# detail page: https://www.wandoujia.com/apps/6046085
DETAIL_PAGE = "^https:\/\/www\.wandoujia\.com\/apps\/[0-9]+$"
# app link example: https://app.mi.com/details?id=com.starbaba.cheetahcharge
APP_LINK = "^https:\/\/app\.mi\.com\/details\?id\=[a-z\.]+$"

CATEGORY_ITEM = [
    {
        "name": "视频播放",
        "value": 45
    },
    {
        "name": "综合服务",
        "value": 50
    },
    {
        "name": "音乐音频",
        "value": 43
    },
    {
        "name": "新闻阅读",
        "value": 53
    },
    {
        "name": "办公学习",
        "value": 54
    },
    {
        "name": "系统工具",
        "value": 39
    },
    {
        "name": "社交网络",
        "value": 52
    },
    {
        "name": "摄影美化",
        "value": 46
    },
    {
        "name": "主题桌面",
        "value": 44
    },
    {
        "name": "气象交通",
        "value": 47
    },
    {
        "name": "手机安全",
        "value": 40
    },
    {
        "name": "输入法",
        "value": 42
    },
    {
        "name": "金融理财",
        "value": 49
    },
    {
        "name": "通信聊天",
        "value": 51
    },
    {
        "name": "阅读器",
        "value": 55
    },
    {
        "name": "浏览器",
        "value": 41
    },
    {
        "name": "购物支付",
        "value": 48
    }
]


class Crawler(object):
    def __init__(self, welcome_link, saving_path):
        self.browser_operator = BrowserOperate(welcome_link, True)
        self.saving_path = saving_path
        self.page_counter = 20

    def category_hanlder(self):
        '''
        get all of the category page, switch to it and turn to detailed_page_handler
        :return:
        '''
        for item in CATEGORY_ITEM:
            # category_example: http://www.anzhi.com/sort_45_1_hot.html
            link_prefix = CATEGORY_PREFIX + str(item["value"]) + "_"
            category_text = item["name"]
            download_links = set()
            print("begin to process " + category_text)
            for i in range(1, self.page_counter + 1):
                url = link_prefix + str(i) + "_hot.html"
                print("we are processing " + url)
                self.browser_operator.open_new_window(url)
                number_before_union = len(download_links)
                download_links = download_links.union(self.detail_page_handler())
                add_number = len(download_links) - number_before_union
                self.browser_operator.close_new_window()
                if add_number == 0:
                    break

            # self.saving_path(category_texts[0], self.detail_page_handler())
            self.save_to_file(category_text, download_links)
            download_links.clear()

# https://app.mi.com/download/94579?id=com.xiaomi.jr&ref=appstore.mobile_download&nonce=-8113586658422584174%3A27049738&appClientId=2882303761517485445&appSignature=CopYI8ZhWQslFjGmKQ7cRPfO-pXHz99a4UAKktscmGA

    # def get_unique_link(self, download_links: set):
    #     pkg_filter = list()
    #     result = set()
    #     for link in download_links:
    #         package_name = link[link.find("id")+3: link.find("&")]
    #         if package_name not in pkg_filter:
    #             result.add(link)
    #         pkg_filter.append(package_name)
    #
    #     return result

    def detail_page_handler(self) -> set:
        app_items = self.browser_operator.browser.find_elements_by_xpath('//*[@href="javascript:void(0)"]')
        download_links = set()
        download_link_prefix = "http://www.anzhi.com/dl_app.php?s="
        for item in app_items:
            app_id = item.get_attribute("onclick")[9:-2]
            dl_link = download_link_prefix + app_id + "&n=5"
            print(dl_link)
            download_links.add(dl_link + "\n")

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


crawler = Crawler("http://www.baidu.com", "E:\\PycharmProgram\\APKCrawler\\Data\\anzhi\\")
crawler.category_hanlder()
