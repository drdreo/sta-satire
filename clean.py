# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 18:09:08 2018

@author: Andreas Stöckl
"""
import env
import sqlite3
import re
import pandas as pd

conn = sqlite3.connect(env.DB_CLEAN_URL)
cur = conn.cursor()


def replaceGermanMonths(month):
    month = re.sub("Dezember", "12", month)
    month = re.sub("November", "11", month)
    month = re.sub("Oktober", "10", month)
    month = re.sub("September", "9", month)
    month = re.sub("August", "8", month)
    month = re.sub("Juli", "7", month)
    month = re.sub("Juni", "6", month)
    month = re.sub("Mai", "5", month)
    month = re.sub("April", "4", month)
    month = re.sub("März", "3", month)
    month = re.sub("Februar", "2", month)
    month = re.sub("Jänner", "1", month)
    return month


def dateEntenpost(txt):
    if txt is not None:
        txt = replaceGermanMonths(txt)
        txt = pd.to_datetime(txt, format='%d. %m %Y')
    return str(txt)


conn2 = sqlite3.connect(env.DB_URL)
cur2 = conn2.cursor()

for row in cur2.execute('SELECT url,Kategorie,Titel,Body,Datum FROM Links'):
    if row[1] is not None:
        print("inserting: " + row[2])
        cur.execute('''INSERT OR REPLACE INTO Artikel
                (url,Kategorie,Titel,Body,Datum,Quelle,Fake) VALUES ( ?,?,?,?,?,?,? )''',
                    (row[0], row[1], row[2], row[3], dateEntenpost(row[4]), "Entenpost", 1))

conn.commit()
cur.close()
cur2.close()
