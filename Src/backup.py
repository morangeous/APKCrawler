#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2021-06-02 19:59:06
# Project: FirstCrawler

from pyspider.libs.base_handler import *
import re

CATEGORY_PATTERN = "^http:\/\/zhushou\.360\.cn\/list\/index\/cid\/[0-9]+\/$"
DOWNLOAD_PATTERN = "http://s.shouji.qihucdn.com"

class Handler(BaseHandler):
    crawl_config = {
    }

    def save_data_to_file(self, file_path, binary_data):
        with open(file_path, 'wb') as f:
            f.write(binary_data)
            f.close()
            print("complete saving file to %s" % file_path)

    def download_callback(self, response):
        bin_data = response.content
        path = "/home/zhaoxin/workspace/code/apkcrawler/data/apks"
        self.save_data_to_file(path, bin_data)

    @every(minutes=10 * 24 * 60)
    def on_start(self):
        self.crawl('http://zhushou.360.cn/list/index/cid/', callback=self.category_page)

    def download_page(self):
        download_link = "zhushou360://type=apk&marketid=10000001&refer=thirdlink&name=西瓜视频&icon=https://p0.qhimg.com/t01f87f7a74c4486081.png&appmd5=68d669b0d0005ebe33c16d674f750f90&softid=3293291&appadb=&url=http://s.shouji.qihucdn.com/210602/68d669b0d0005ebe33c16d674f750f90/com.ss.android.article.video_572.apk?en=curpage%3D%26exp%3D1623243006%26from%3DAppList_json%26m2%3D%26ts%3D1622638206%26tok%3D11ab2fc69d253e5e72f100984a2632de%26v%3D%26f%3Dz.apk"
        self.crawl(download_link, callback=self.download_callback)

    def category_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if bool(re.search(CATEGORY_PATTERN, each.attr.href)):
                print(each.attr.href)
                self.crawl(each.attr.href, callback=self.detailed_page)

    def detailed_page(self, response):
        for each in response.doc('a[href^="zhushou360"]').items():
            if each.attr.href.find()
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
