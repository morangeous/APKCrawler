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


broswer_operator = BrowserOperate("http://shouji.baidu.com/software")
result = broswer_operator.get_links_by_re(CATEGORY)
print(result)