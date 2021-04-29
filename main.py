from telethon import TelegramClient
import requests
from bs4 import BeautifulSoup
import time

api_id = 5691675
api_hash = 'e45f7197100f1099c06ffd130ea028b4'

client = TelegramClient('anon', api_id, api_hash)

client.start()




def get_name_from_link(link):
    req = requests.get(link)
    soup = BeautifulSoup(req.content, "html.parser")
    return soup


def get_name_by_url(url):
    pass


def send_msg(name, msg):
    client.send_message(name, msg)


main_bot = "Dogecoin_click_bot"
name = 'claim_free_bitcoin_bot'


while True:
    send_msg(main_bot, "/bots")
    time.sleep(5)
    messages = next(client.iter_messages(main_bot, limit=1))
    url = messages.reply_markup.rows[0].buttons[0].url
    print(url)
    soup = get_name_from_link(url)
    time.sleep(10)



