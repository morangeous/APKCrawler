from time import sleep
import re
from selenium import webdriver

# category example: https://shouji.baidu.com/software/503/
CATEGORY = "^https:\/\/shouji\.baidu\.com\/software\/5[0-9]{2}\/$"
# detailed page example: https://shouji.baidu.com/software/28488159.html
DETAILED_PAGE = "^https:\/\/shouji\.baidu\.com\/software\/[0-9]+\.html"
# download_link example: http://p.gdown.baidu.com/2119cac02ff19133e78ec4d79a7d5695ec69d7728e0b40a907a5ed0f4ac433f73142bbbf8741b8cd54907f19d11b27fec1250aa4f4faf97104bfd7a923fcda3e03bfe38b8993c7ef2dd0c8de7ca67e6cf3b6222944a0dff9b95a67ce74b0272569fb2701df049e2ecf635800e284d55d16b138ef9a3d5575e92c04b8884690a9b4fdc97816f92da2202a286da2f7e1dbb8420f96f1a4d67c
DOWNLOAD_LINK = "^http:\/\/p\.gdown\.baidu\.com\/[0-9a-z]+$"

class BrowserOperate(object):
    def __init__(self, welcome_link):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument('blink-settings=imagesEnabled=false')
        options.add_argument('--disable-gpu')
        options.add_argument("--headless")
        self.browser = webdriver.Chrome(options=options)
        self.browser.get(welcome_link)
        self.last_window = []

    def open_new_window(self, link):
        '''
        Attention, before you open a new tab, you should call this function, after you close tab
        remember to call the function close_current_tab
        :param link:
        :return: None
        '''
        # First reset the current_window
        if self.browser.current_window_handle == None or self.browser.current_window_handle == "":
            assert False, "[BrowserOperate]: FATAL, current_window_handle is None"
        self.last_window.append(self.browser.current_window_handle)

        # Second change to the target link
        current_page_num = len(self.browser.window_handles)
        script = 'window.open("' + link + '")'
        self.browser.execute_script(script)
        self.browser.switch_to.window(self.browser.window_handles[current_page_num])

    def close_new_window(self):
        self.browser.close()
        self.browser.switch_to.window(self.last_window[len(self.last_window) - 1])
        self.last_window.pop()

    def get_links_by_re(self, pattern, with_text=False):
        link_elements = self.browser.find_elements_by_xpath("//*[@href]")
        pattern = re.compile(pattern)
        links = []
        texts = []
        for element in link_elements:
            link = element.get_attribute("href")
            if bool(pattern.search(link)):
                links.append(link)
                texts.append(element.text)
        if with_text:
            return links, texts
        return links

    # def get_link_text_by_re(self, pattern):
    #     '''
    #     Attention, this function is used to get the text of an link element which matches the pattern provided
    #     by caller, return value is a string representing the text of element
    #     :param pattern: str
    #     :return: text: str
    #     '''
    #     elements = self.browser.find_elements_by_xpath("//*[@href]")
    #     pattern = re.compile(pattern)
    #     for element in


class Crawler(object):
    def __init__(self, welcome_link, saving_path):
        self.browser_operator = BrowserOperate(welcome_link)
        self.page_counter = 20
        self.saving_path = saving_path

    def category_hanlder(self):
        '''
        get all of the category page, switch to it and turn to detailed_page_handler
        :return:
        '''
        category_links, category_texts = self.browser_operator.get_links_by_re(CATEGORY, True)
        download_links = set()
        for i in range(len(category_links)):

            for j in range(1, self.page_counter + 1):
                length_before_append = len(download_links)
                new_url = category_links[i] + "list_" + str(j) + ".html"
                print("current_url: " + new_url)
                self.browser_operator.open_new_window(new_url)
                download_link = self.detail_page_handler()
                download_links = download_links.union(download_link)
                print("close in category handler")
                self.browser_operator.close_new_window()
                length_after_append = len(download_links)
                if length_after_append == length_before_append:
                    break

            # for link in download_links:
            #     print(link)

            # save as category
            self.save_to_file(category_texts[i], download_links)
            download_links.clear()

    def detail_page_handler(self) -> set:
        '''
        switch to detailed pages, get the app link and info, save all of these eventually
        :return:
        '''
        links = self.browser_operator.get_links_by_re(DETAILED_PAGE)
        download_links = set()
        for link in links:
            self.browser_operator.open_new_window(link)
            download_link = self.browser_operator.get_links_by_re(DOWNLOAD_LINK)
            print(download_link)
            for temp in download_link:
                temp = temp + "\n"
                download_links.add(temp)
            print("close in detailed_page_handler")
            self.browser_operator.close_new_window()
        sleep(1)
        return download_links

    def save_to_file(self, category_text, links):
        saving_path = self.saving_path + category_text + ".txt"
        links = list(links)
        with open(saving_path, 'w') as f:
            f.writelines(links)

# browser = webdriver.Chrome()
# browser.get("https://shouji.baidu.com/software")
# link_elements = browser.find_elements_by_xpath("//*[@href]")
# category_pattern = re.compile(CATEGORY)
# for element in link_elements:
#     link = element.get_attribute("href")
#     if bool(category_pattern.search(link)):
#         print(link)


crawler = Crawler("http://shouji.baidu.com/software", "E:\\PycharmProgram\\APKCrawler\\Data\\")
crawler.category_hanlder()