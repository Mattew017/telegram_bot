from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
import requests
from bs4 import BeautifulSoup
import time
import re
import urllib.request
from selenium import webdriver

api_id = 5691675
api_hash = 'e45f7197100f1099c06ffd130ea028b4'

client = TelegramClient('anon', api_id, api_hash)

client.start()


def get_name_from_link(link):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
    req = requests.get(link, headers=headers)
    soup = BeautifulSoup(req.content, "html.parser")
    tag = soup.find('div', class_="tgme_page_extra")
    # print("tag", tag)
    return str(tag.text).split()[0][1:]


class RunChromeTests():
    def __init__(self, waitin, url_rec):
        self.waitin = waitin
        self.url_rec = url_rec

    def testMethod(self):
        caps = {'browserName': 'chrome'}
        driver = webdriver.Remote(command_executor=f'http://localhost:4444/wd/hub', desired_capabilities=caps)
        driver.maximize_window()
        driver.get(self.url_rec)
        time.sleep(self.waitin + 10)
        driver.close()
        driver.quit()



main_bot = "Dogecoin_click_bot"

def adv_loop(main_bot):
    n = 0
    sorry_count_ads = 0
    client.send_message(main_bot, "/visit")
    time.sleep(3)
    while True:
        msgs = client.get_messages(main_bot, limit=1)

        for mes in msgs:
            if re.search(r'\bseconds to get your reward\b', mes.message):
                print("Найдено reward")
                str_a = str(mes.message)
                zz = str_a.replace('You must stay on the site for', '')
                qq = zz.replace('seconds to get your reward.', '')
                waitin = int(qq)
                print("Ждать придется: ", waitin)
                client.send_message(main_bot, "/visit")
                time.sleep(3)
                msgs2 = client.get_messages(main_bot, limit=1)
                for mes2 in msgs2:
                    button_data = mes2.reply_markup.rows[1].buttons[1].data
                    message_id = mes2.id

                    print("Перехожу по ссылке")
                    time.sleep(2)
                    url_rec = messages[0].reply_markup.rows[0].buttons[0].url
                    ch = RunChromeTests(waitin,url_rec)
                    ch.testMethod()
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
                        # os.system("pkill chromium")
                    else:
                        time.sleep(waitin)
                        # os.system("pkill chromium")
                        time.sleep(2)

            elif re.search(r'\bSorry\b', mes.message):
                print("Найдено Sorry")
                sorry_count_ads += 1
                if sorry_count_ads > 2:
                    return
                client.send_message(main_bot, "/visit")
                time.sleep(6)


            else:
                messages = client.get_messages(main_bot)
                url_rec = messages[0].reply_markup.rows[0].buttons[0].url
                f = open("per10.txt")
                fd = f.read()
                if fd == url_rec:
                    pass
                else:
                    url = 'https://www.virustotal.com/vtapi/v2/url/scan'
                    params = {
                        'apikey': 'faf8a5bd4de74887ab146d24368cbe1b337b6048f7f9934deebfdee97b104dd6', 'url': url_rec}
                    response = requests.post(url, data=params)
                    my_file = open('per10.txt', 'w')
                    my_file.write(url_rec)
                    print("Новая запись в файле сдерана")
                    time.sleep(120)
                    n = n + 1
                    print("Пройдено циклов: ", n)


def adv(main_bot):
    pass


def bot_loop(main_bot):
    sorry_bot_count = 0
    while True:
        client.send_message(main_bot, "/bots")
        time.sleep(2)
        messages = next(client.iter_messages(main_bot, limit=1))
        if re.search(r'\bSorry\b', messages.message):
            sorry_bot_count += 1
            if sorry_bot_count > 3:
                print("No bot available")
                return
        try:
            url = messages.reply_markup.rows[0].buttons[0].url
            print(url)
            bot_name = get_name_from_link(url)
            time.sleep(5)
            print(bot_name)
            client.send_message(bot_name, "/start")
            time.sleep(5)
            messages = next(client.iter_messages(bot_name, limit=1))
            if messages.message == "/start": # скипаем бота, если он не отвечает
                messages = next(client.iter_messages(main_bot, limit=1))
                client(GetBotCallbackAnswerRequest(
                    main_bot,
                    messages.id,
                    data=messages.reply_markup.rows[1].buttons[1].data
                ))
                time.sleep(3)

            peer_id = messages.peer_id
            client.forward_messages(main_bot, messages)
            for dialog in client.iter_dialogs():
                if dialog.message.peer_id == peer_id:
                    dialog.delete()
                    print("dialog was deleted")
        except Exception as e:
            print(e)


while True:
    #adv_loop(main_bot)
    time.sleep(5)
    bot_loop(main_bot)
    print("Спим 10 минут")
    time.sleep(60*10)