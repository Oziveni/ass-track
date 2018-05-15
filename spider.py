import datetime
import logging
import re
import requests
import grequests
from bs4 import BeautifulSoup

import config

def replace_nbsp (string):
    return string.replace(u"\xa0", " ")

def scrap_member (member_page):
    DOMAIN = "http://www.psp.cz/sqw/"
    member_soup = BeautifulSoup(member_page.content, "html.parser", from_encoding="windows-1250")
    member = {
        "id": re.search("id=(.*)", member_page.url).group(1),
        "name": replace_nbsp(member_soup.h1.string),
        "assistants": [],
    }
    if member_soup.address is not None:
        member["address"] = replace_nbsp(member_soup.address.get_text())
    for assistant in member_soup.select("ul.assistants li strong"):
        member["assistants"].append(replace_nbsp(assistant.string))
    logging.debug("Scrapped member " + member["name"] + " from " + member_page.url)
    return member

def scrap_snapshot ():
    DOMAIN = "http://www.psp.cz/sqw/"
    list_page = requests.get(DOMAIN + "hp.sqw?k=192")
    list_soup = BeautifulSoup(list_page.content, "html.parser", from_encoding="windows-1250")
    snapshot = {
        "timestamp": datetime.datetime.now(),
        "members": [],
    }
    links = list_soup.select(".person-list .name a")
    links = links if config.IS_PRODUCTION else links[0:3]
    rs = (grequests.get(DOMAIN + link["href"]) for link in links)
    rs = grequests.map(rs, size=20)
    for r in rs:
        snapshot["members"].append(scrap_member(r))
    logging.info("Scrapped " + str(len(snapshot["members"])) + " members.")
    return snapshot
