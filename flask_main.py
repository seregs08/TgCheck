import re
import os
import asyncio
import configparser
# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.sync import TelegramClient

from flask import Flask, request, render_template
app = Flask(__name__)

# Считываем учетные данные
config = configparser.ConfigParser()
config.read(f"{os.path.dirname(os.path.abspath(__file__))}/config.ini") # Временно, переделать под норамльное указание конфига

# Присваиваем значения внутренним переменным
api_id   = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

client = TelegramClient(username, api_id, api_hash)
# client.start()
loop = asyncio.get_event_loop()
alphabet = set([chr(s) for s in range(ord('а'), ord('я') + 1)])

async def dump_all_messages(channel):
    async for message in client.iter_messages(channel, limit=50):
        if (message.message and alphabet.intersection(set(message.message.lower()))):
            return
    return f"@{channel}"

async def main(channel_split):
    problem_channel = set()
    await client.start()
    for input_channel in channel_split:
        #channel = await client.get_entity(f"https://t.me/{input_channel}")
        try:
            check = await dump_all_messages(input_channel)
            if check:
                problem_channel.add(check)
        #return problem_channel
        except Exception as ex:
            problem_channel.add(f"Error in channel @{input_channel}: {ex}")
    return problem_channel

@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        tg_channel = request.form['tg_channel']
        channel_split = set([ch for ch in re.split(",|\n|@|\r| ", tg_channel) if ch])

    if 'channel_split' in locals():
        if channel_split:
            problem_chnl = loop.run_until_complete(main(channel_split))
            return render_template("main.html", problem_channel=problem_chnl)
        else:
            return render_template("main.html", problem_channel=None)
    else:
        return render_template("main.html", problem_channel=None)

if __name__ == '__main__':
    app.run(debug=True)
