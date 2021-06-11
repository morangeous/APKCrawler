import re
from selenium import webdriver
from time import sleep

class BrowserOperate(object):
    def __init__(self, welcome_link, headless):
        options = webdriver.ChromeOptions()
        # anti-anti-crawler
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')
        # options.add_argument(
        #     'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
        options.add_argument("proxy-server=socks5://127.0.0.1:10808")
        res_json = self.get_timezone_geolocation("16.162.106.129")
        print(res_json)
        geo = {
            "latitude": res_json["lat"],
            "longitude": res_json["lon"],
            "accuracy": 1
        }
        tz = {
            "timezoneId": res_json["timezone"]
        }
        # anti-anti-crawler end
        if headless:
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument('blink-settings=imagesEnabled=false')
            options.add_argument('--disable-gpu')
            options.add_argument("--headless")
        self.browser = webdriver.Chrome(options=options)
        self.browser.execute_cdp_cmd("Emulation.setGeolocationOverride", geo)
        self.browser.execute_cdp_cmd("Emulation.setTimezoneOverride", tz)
        self.browser.implicitly_wait(10)
        self.browser.get(welcome_link)
        self.last_window = []

    def get_timezone_geolocation(self, ip):
        import requests
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url)
        return response.json()

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

