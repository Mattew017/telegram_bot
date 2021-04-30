import sqlite3
import requests
from bs4 import BeautifulSoup

def get_all_accounts(filename='accounts.db'):
    with sqlite3.connect(filename) as conn:
        cur = conn.cursor()

        cur.execute("SELECT id, phone, password, api_id, api_hash FROM accounts")
        accounts = cur.fetchall()

        cur.close()
    return accounts


def get_name_from_link(link):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
    req = requests.get(link, headers=headers)
    soup = BeautifulSoup(req.content, "html.parser")
    tag = soup.find('div', class_="tgme_page_extra")
    # print("tag", tag)
    return str(tag.text).split()[0][1:]