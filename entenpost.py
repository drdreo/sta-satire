"""
@author: Andreas Hahn
"""
import env

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

import sqlite3

# conn = sqlite3.connect(env.DB_URL)
# cur = conn.cursor()
# print("Starting link crawling")
# for i in range(1, 20):
#     url = "https://www.entenpost.com/page/" + str(i) + "/"
#     html = urllib.request.urlopen(url, context=ctx).read()
#     soup = BeautifulSoup(html, 'html.parser')
#     teasers = soup.find_all("article", class_="post")
#     for art in teasers:
#         link = art.find("a")
#         link = link.get('href')
#         print(link)
#         cur.execute('''INSERT OR IGNORE INTO Links (url) VALUES ( ? )''', (link,))
# conn.commit()
# cur.close()
#
# print("Done link crawling")


def loadArticles(url):
    print("fetching article: " + url)
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    info = soup.find("div", class_="post-info")

    if info is not None:
        cat = info.find("span", class_="thecategory").get_text()
        date = info.find("span", class_="thetime").get_text()
    else:
        return None

    title = soup.find("h1", class_="title")
    if title is not None:
        title = title.get_text()
    else:
        return None

    body = soup.find_all("div", class_="post-single-content")
    if body != []:
        body = body[0].find_all("p")
    else:
        return None

    content = ""
    for p in body:
        content += p.get_text() + " "

    print("loading article: " + title)
    cur.execute('''INSERT OR REPLACE INTO Links (url,Kategorie,Titel, Body, Datum, crawled) VALUES (?,?,?,?,?,?)''',
                (url, cat, title, content, date, "1"))
    return None


conn = sqlite3.connect(env.DB_URL)
cur = conn.cursor()

cur.execute('SELECT url,crawled FROM Links')
sel = cur.fetchmany(400)
for row in sel:
    if row[1] != "1":
        loadArticles(row[0])
conn.commit()
cur.close()
