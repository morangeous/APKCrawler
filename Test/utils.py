import re
import sys

PATTERN = "^http:\/\/zhushou\.360\.cn\/list\/index\/cid\/[0-9]+\/$"

def filter(links: list):
    for link in links:
        if bool(re.search(PATTERN, link)):
            print("we find it")
            print(link)
        else:
            pass

def url_transformer(url: str) -> str:
    pass




with open("../Data/links.txt", 'r') as f:
    links = f.readlines()
    filter(links)
