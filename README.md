APKCrawler
===
### Introduction
This repo is a framework for crawling APKs from several application market, such as anzhi, xiaomi, 360 and baidu.
In order to escape from being detected by market, I crawl apks from markets using selenium to operate browser 
download apks.

The whole pipeline contains two step. First, crawl the direct links from markets. Second, download apks via the links.

By comparison, the second step is more simple, you can download apks leveraging the following command:

`aria2 --conf-path=/PATH/TO/CONF/FILE -i /PATH/TO/LINKS/FILE -d /PATH/TO/SAVING/DIR`

### Crawler Framework
You can find four cralwers in /APKCrawler/Src/, they are quite similar and include follow steps:
+ Launch Browser
    
    You can get a browser driver by invoking BrowserOperator in /Src/Util/. What's more, if you want to launch browser 
    in headless mode, just change second parameter into False when you call BrowserOperator

+ Crawl Category Page
    
    Get all of the category pages links and open them in a new window.
    
+ Get Direct Link
    
    In a detailed page, you can get all direct link of apks, remember to store them.
    