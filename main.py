from telethon.sync import TelegramClient
import requests
from bs4 import BeautifulSoup
import time
import re
import urllib.request


api_id = 5691675
api_hash = 'e45f7197100f1099c06ffd130ea028b4'

client = TelegramClient('anon', api_id, api_hash)

client.start()


def get_name_from_link(link):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    req = requests.get(link, headers=headers)
    soup = BeautifulSoup(req.content, "html.parser")
    tag = soup.find('div', class_="tgme_page_extra")
    # print("tag", tag)
    return str(tag.text).split()[0][1:]


main_bot = "Dogecoin_click_bot"

sorry_count = 0
while True:
    client.send_message(main_bot, "/visit")
    msgs = client.iter_messages(main_bot, limit=1)
    for mes in msgs:
        #print(mes)
        if re.search(r'\bseconds to get your reward\b', mes.message):
            print("Найдено reward")
            str_a = str(mes.message)
            zz = str_a.replace('You must stay on the site for', '')
            qq = zz.replace('seconds to get your reward.', '')
            waitin = int(qq)
            print ("Ждать придется: ", waitin)
            client.send_message(main_bot, "/visit")
            time.sleep(3)
            msgs2 = client.get_messages(main_bot, limit=1)
            for mes2 in msgs2:
                button_data = mes2.reply_markup.rows[1].buttons[1].data
                message_id = mes2.id
                print("Перехожу по ссылке")
                time.sleep(2)
                url_rec = messages[0].reply_markup.rows[0].buttons[0].url


                time.sleep(6)
                fp = urllib.request.urlopen(url_rec)
                mybytes = fp.read()
                mystr = mybytes.decode("utf8")
                fp.close()
                if re.search(r'\bSwitch to reCAPTCHA\b', mystr):
                    from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
                    resp = client(GetBotCallbackAnswerRequest(
                        main_bot,
                        message_id,
                        data=button_data
                    ))
                    time.sleep(2)
                    print("КАПЧА!")

                else:
                    time.sleep(waitin)

                    time.sleep(2)
        elif re.search(r'\bSorry\b', mes.message):
            sorry_count += 1
            if sorry_count >= 3:
                sorry_count = 0
                break
            print("Найдено Sorry")


        else:
            messages = next(client.iter_messages(main_bot, limit=1))
            #print(messages)
            time.sleep(0.5)
            url_rec = messages.reply_markup.rows[0].buttons[0].url
            f = open("per10.txt")
            fd = f.read()
            if fd == url_rec:
                print("Найдено повторение переменной")
                msgs2 = client.get_messages(main_bot, limit=1)
                for mes2 in msgs2:
                    button_data = mes2.reply_markup.rows[1].buttons[1].data
                    message_id = mes2.id
                    from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
                    resp = client(GetBotCallbackAnswerRequest(
                        main_bot,
                        message_id,
                        data=button_data
                    ))
                    time.sleep(2)
            else:
                waitin = 15
                data1 = requests.get(url_rec).json
                print(data1)

                my_file = open('per10.txt', 'w')
                my_file.write(url_rec)
                print("Новая запись в файле сделана")
                time.sleep(16)


while True:
    client.send_message(main_bot, "/bots")
    time.sleep(3)
    messages = next(client.iter_messages(main_bot, limit=1))
    if re.search(r'\bSorry\b', messages.message):
        print("No bot available")
        break
    try:
        url = messages.reply_markup.rows[0].buttons[0].url
        print(url)
        bot_name = get_name_from_link(url)
        print(bot_name)
        client.send_message(bot_name, "/start")
        time.sleep(3)
        messages = next(client.iter_messages(bot_name, limit=1))
        if messages.message == "/start":
            # skipping bot cuz it sucks
            pass
        peer_id = messages.peer_id
        client.forward_messages(main_bot, messages)
        for dialog in client.iter_dialogs():
            if dialog.message.peer_id == peer_id:
                dialog.delete()
                print("dialog was deleted")
    except Exception as e:
        print(e)
