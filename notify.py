import re
import datetime
import yaml
import sys

from slack import Slack
from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from collections import OrderedDict

YAML_PATH = './config/slack.yml'
URL = 'https://datatracker.ietf.org/doc/'

def main():

    # load parameter from config file
    yaml = load_yaml(YAML_PATH)
    if yaml['token'] is None or yaml['channel'] is None:
        sys.stderr.write("Please set parameter\n")
        sys.exit(2)

    # scrape draft from web site
    html = fetch('https://datatracker.ietf.org/doc/active/')
    draft_list = scrape_draft_url(html)
    date_list = extract_date_from_url(html)

    # create dictionary list
    dict_list = OrderedDict()
    for (draft, date) in zip(draft_list, date_list):
        dict_list[draft] = date

    # get yesterday date
    date = datetime.date.today() - datetime.timedelta(1)
    search_date = date.strftime("%Y-%m-%d")

    # post to slack
    slack = Slack(yaml['token'])

    for key, value in dict_list.items():
        if value == search_date:
            slack.post(yaml['channel'], key, yaml['username'])

def fetch(url):
    r = urlopen(url)
    encode = r.info().get_content_charset(failobj="utf-8")
    html = r.read().decode(encode)

    return html

def scrape_draft_url(html):
    soup = BeautifulSoup(html, "html.parser")
    draft_list = []

    for link in soup.findAll("a"):
        if "draft" in link.get("href"):
            draft = urljoin(URL, link.get("href"))
            draft_list.append(draft)

    return draft_list

def extract_date_from_url(html):
    pattern = r"<br>\d*-\d*-\d*"
    date_list = []

    matchs = re.findall(pattern, html)
    for match in matchs:
        date = match.replace('<br>', '')
        date_list.append(date)

    return date_list

def load_yaml(path):
    f = open(path, 'r').read()
    ret = yaml.load(f)

    return ret

if __name__ == '__main__':
    main()
