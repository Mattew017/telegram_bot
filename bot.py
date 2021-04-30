import os
import time
import logging
import utils

from bs4 import BeautifulSoup
import requests

from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
from telethon.sync import TelegramClient
import config

requests.adapters.DEFAULT_RETRIES = config.DEFAULT_RETRIES
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

os.makedirs(config.URLS_FOLDER_PATH, exist_ok=True)


def skip_task(client, message):
    client(GetBotCallbackAnswerRequest(
        config.BOT_ADDRESS,
        message.id,
        data=message.reply_markup.rows[1].buttons[1].data
    ))
    time.sleep(5)


accounts = utils.get_all_accounts()

for x, phone, password, api_id, api_hash in accounts:
    path_to_bad_urls = os.path.join(config.URLS_FOLDER_PATH, f"{x}.txt")
    no_tasks_count = 0  # Кол-во раз, когда не получилось найти заданий
    logging.info(f"Очередь аккаунта № {x}")
    logging.info(f"Входим в аккаунт: {phone}")
    client = TelegramClient(f"{config.TELETHON_SESSION_NAME}{x}", api_id, api_hash)
    client.start()

    messages = client.get_messages(config.BOT_ADDRESS)
    if messages.total == 0:
        client.send_message(config.BOT_ADDRESS, "/start")
        time.sleep(1)
    client.send_message(config.BOT_ADDRESS, "/visit")

    if not os.path.exists(path_to_bad_urls):
        with open(path_to_bad_urls, "a+") as f:
            pass

    for loop_count in range(config.TASKS_COUNT):
        logging.info(f"Приступаем к {loop_count + 1} заданию из {config.TASKS_COUNT}")
        time.sleep(3)

        if no_tasks_count == config.TRIES_COUNT:
            logging.info("Заданий больше нет. Переходим к ботам")
            break

        message = client.get_messages(config.BOT_ADDRESS)[0]

        if 'Sorry, there are no new ads available.' in message.message:
            no_tasks_count += 1
            logging.info("Похоже, что задания закончились. Попытка получить его ещё раз...")
            client.send_message(config.BOT_ADDRESS, "/visit")
            time.sleep(10)
            continue

        url = message.reply_markup.rows[0].buttons[0].url
        with open(path_to_bad_urls, "r") as f:
            bad_urls = f.read().split('\n')

        if url in bad_urls:
            skip_task(client, message)
            logging.info('url был в bad_url')
            continue
        try:
            soup = BeautifulSoup(requests.get(url).content, "lxml")
            time.sleep(2)  # Задержка из-за того, что бот не сразу присылает время, которое нужно ждать
        except requests.exceptions.ConnectionError as e:
            # Некоторые сайты, которые запрещены в РФ, почему-то не открываются. Может быть не доступен хост
            logging.error("Сайт недоступен")
            logging.exception(e, exc_info=True)
            client.send_message(config.BOT_ADDRESS, "/visit")
            time.sleep(25)
            continue

        potential_captcha = soup.select_one('.card .card-body .text-center h6')

        if potential_captcha is not None and 'captcha' in potential_captcha.text.lower():
            logging.info('Найдена капча. Пропускаем задание...')
            skip_task(client, message)
            continue

        p = soup.select_one('#headbar.container-fluid')
        if p is not None:
            wait_time = int(p['data-timer'])
            logging.debug('+ request')
            logging.info(f"Ожидаем {wait_time} c.")
            time.sleep(wait_time + 1)
            r = requests.post('https://dogeclick.com/reward', data={'code': p['data-code'], 'token': p['data-token']})
            logging.debug(r.json())
        else:
            message = client.get_messages(config.BOT_ADDRESS)[0]
            elements = list(filter(lambda i: i.isnumeric(), message.message.split(' ')))
            wait_time = int(elements[0]) if len(elements) == 1 else 25
            logging.info(f"Ожидаем {wait_time} c.")
            time.sleep(wait_time)
        message.mark_read()
        logging.info(f"Выполнено: {loop_count + 1} из {config.TASKS_COUNT}")

        with open(path_to_bad_urls, "a") as f:
            f.write(f"{url}\n")

    time.sleep(3)
    no_tasks_count = 0  # Кол-во раз, когда не получилось найти ботов
    client.send_message(config.BOT_ADDRESS, "/bots")
    for loop_count in range(config.BOT_COUNT):
        logging.info(f"Приступаем к {loop_count + 1} боту из {config.BOT_COUNT}")
        time.sleep(3)

        if no_tasks_count == config.TRIES_COUNT:
            logging.info("Ботов больше нет. Переходим на другой аккаунт")
            break

        message = client.get_messages(config.BOT_ADDRESS)[0]  # что ответил основной бот

        if 'Sorry, there are no new ads available.' in message.message:
            no_tasks_count += 1
            logging.info("Похоже, что боты закончились. Попытка получить их ещё раз...")
            client.send_message(config.BOT_ADDRESS, "/bots")
            time.sleep(8)
            continue
        else:
            url = message.reply_markup.rows[0].buttons[0].url  # ссылка на сайт
            try:
                bot_name = utils.get_name_from_link(url)  # имя бота, которому нужно написать
                client.send_message(bot_name, "/start")
                time.sleep(10)  # бот может ответить с задержкой
                msg_to_forward = client.get_messages(bot_name)[0]

                no_answer = False
                if msg_to_forward.message == "/start":  # скипаем бота, если он не отвечает
                    no_answer = True
                    skip_task(client, message)

                if not no_answer:  # пересылаем основному боту, если бот ответил
                    client.forward_messages(config.BOT_ADDRESS, msg_to_forward)
                peer_id = msg_to_forward.peer_id  # Id бота, с которому мы писали
                for dialog in client.iter_dialogs():
                    if dialog.message.peer_id == peer_id:
                        dialog.delete()  # удаляем диалог с ботом
                        #print(f"dialog with {bot_name} was deleted")

            except Exception as e:
                logging.info("Скипаем бота, т.к. есть проверка на ddos или еще что-то")
                skip_task(client, message)
                continue

    time.sleep(60*30)
    logging.info("Спим 30 минут, т.к. ботов всего 2")

