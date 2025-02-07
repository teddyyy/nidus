# -*- coding: utf-8 -*-

import re
import datetime
import sys
import argparse

import collections
collections.Callable = collections.abc.Callables

from slack import Slack
from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.error import URLError
from bs4 import BeautifulSoup

BASEURL = 'https://datatracker.ietf.org/doc/'

def main():

    # load parameter of slack
    params = load()

    # scrape draft from web site
    html = fetch('https://datatracker.ietf.org/doc/active/')
    if not html:
        sys.stderr.write("An error occurred. Can not html data")
        sys.exit(2)

    draft_list = extract_draft_from_html(html)
    date_list = extract_date_from_html(html)

    # create dictionary list
    dict_list = collections.OrderedDict()
    for (draft, date) in zip(draft_list, date_list):
        dict_list[draft] = date

    search_date = ''
    if not params['search_date']:
        # get yesterday date
        date = datetime.date.today() - datetime.timedelta(1)
        search_date = date.strftime("%Y-%m-%d")
    else:
        search_date = params['search_date']

    # post to slack
    slack = Slack(params['token'])
    for key, value in dict_list.items():
        if value == search_date:
            print(f'draft: {key}')
            slack.post(params['channel'], key)

def fetch(url):
    html = ''
    try:
        r = urlopen(url)
        encode = r.info().get_content_charset(failobj="utf-8")
        html = r.read().decode(encode)
    except URLError as e:
        print("error occurred" + e.reason)

    return html

def extract_draft_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    draft_list = []
    url_list = []
    title_list = []

    # scrape link of draft
    for link in soup.findAll("a"):
        if "draft" in link.get("href"):
            draft = urljoin(BASEURL, link.get("href"))
            url_list.append(draft)

    # scrape title of draft
    for link in soup.findAll("b"):
        if link.string != 'Javascript disabled?':
            title_list.append(link.string)

    # join title and link
    for (title, url) in zip(title_list, url_list):
        draft_list.append(title + "\n" + url)
    
    return draft_list

def extract_date_from_html(html):
    pattern = r"<br>\s*\d*-\d*-\d*"
    date_list = []

    matchs = re.findall(pattern, html)
    for match in matchs:
        date_list.append(re.sub('<br>\s*', '', match))
        
    return date_list

def load():
    parser = argparse.ArgumentParser(description='Notification of Internet Draft Update using Slack')
    parser.add_argument('token', help='Slack Bot User OAuth Token')
    parser.add_argument('--channel', default='ietf-draft')
    parser.add_argument('--search_date', default='', help='YYYY-MM-DD')
    args = parser.parse_args()

    params = {}

    params['token'] = args.token
    params['channel'] = args.channel
    params['search_date'] = args.search_date

    return params


if __name__ == '__main__':
    main()
