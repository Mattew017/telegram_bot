from telethon import TelegramClient
from telethon import sync, events
import  time

api_id = 5691675
api_hash = 'e45f7197100f1099c06ffd130ea028b4'

client = TelegramClient('anon', api_id, api_hash)

client.start()

dlgs = client.iter_dialogs()

for dlg in dlgs:
    if dlg.title == 'DOGE Click Bot':
        tegmo = dlg

msgs = client.iter_messages(tegmo, limit=1)


def send_msg(bot_name, msg):
    client.send_message(bot_name, msg)


def get_last_msg(bot_name):
    last_msg = next(client.iter_messages(bot_name, limit=1))
    return last_msg


def forward_msg(bot_name, msg):
    client.forward_messages(bot_name, msg)


name = 'claim_free_bitcoin_bot'
while True:
    send_msg(name, "/start")
    time.sleep(0.5)
    last_bot_msg = get_last_msg(name)
    print(last_bot_msg)
    forward_msg('Dogecoin_click_bot', last_bot_msg)
    time.sleep(15)
