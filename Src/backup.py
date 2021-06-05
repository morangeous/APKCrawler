#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2021-06-02 19:59:06
# Project: FirstCrawler

from pyspider.libs.base_handler import *
import re
import json

CATEGORY_PATTERN = "^http:\/\/zhushou\.360\.cn\/list\/index\/cid\/[0-9]{2,}\/$"
DOWNLOAD_PATTERN = "http://s.shouji.qihucdn.com"


class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.saving_prefix = "/root/workspace/code/apkcrawler/data/links/"
        self.page_to_crawl = 40


    def save_data_to_file(self, file_path, binary_data):
        with open(file_path, 'wb') as f:
            f.write(binary_data)
            f.close()
            print("complete saving file to %s" % file_path)

    def download_callback(self, response):
        bin_data = response.content
        path = "/root/workspace/code/apkcrawler/data/apks"
        self.save_data_to_file(path, bin_data)

    @every(minutes=10 * 24 * 60)
    def on_start(self):
        self.crawl('http://zhushou.360.cn/list/index/cid/', callback=self.category_page)


    def save_links(self, path, link_list: list):
        with open(path, 'a+') as f:
            f.writelines(link_list)

    def save_json(self, path, json_file: object):
        with open(path, 'a+') as f:
            f.write(json_file)

    def category_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if bool(re.search(CATEGORY_PATTERN, each.attr.href)):
                print(each.attr.href)
                category_name = each.text()
                for i in range(1, self.page_to_crawl+1):
                    page = "?page=" + str(i)
                    self.crawl(each.attr.href+page, callback=self.detailed_page, save={'category_name': category_name})

    def parse_name(self, raw_string: str):
        index = raw_string.find("name=")
        raw_string = raw_string[index + 5:]
        index = raw_string.find("&")
        return raw_string[:index]

    def detailed_page(self, response):
        links = []
        apk_info = []
        for each in response.doc('a[href^="zhushou360"]').items():
            link = each.attr.href
            print("raw link is: " + link)
            index = link.find(DOWNLOAD_PATTERN)
            if index != -1:
                links.append(link[index:] + "\n")
                print("download link is: " + link[index:])
                name = self.parse_name(link)
                print("name is: " + name)
                apk_info.append({
                    "name": name,
                    "link": link,
                })
        category_name = response.save['category_name']
        print("begin to save" + category_name)
        self.save_links(self.saving_prefix + category_name + ".txt", links)
        self.save_json(self.saving_prefix + category_name + ".json", json.dumps(apk_info))