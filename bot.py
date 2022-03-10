from aiogram import *
import requests
from bs4 import BeautifulSoup
import logging
import datetime

url = 'http://gendalf.cf/'
bot = Bot(token='5249454736:AAGR3O6RcXnH3Xcy1zBh8sraQUmFeCtfXYQ')
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start'])
async def start_command(msg: types.Message):
    await msg.reply('Привет!\nМы сообщим, как только цена на товар поменяется:)')
    date = datetime.datetime.now()
    old_price = new_price()
    while True:
        if old_price != new_price():
            await msg.reply(f'Название товара: {text_price()}\nНовая цена: {new_price()}\nСтарая цена: {old_price}\nДата: {date.strftime("%d/%m/%Y  %H:%M:%S")}')
        else:
            continue


async def new_price():
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')
    price = soup.find('h2').text.strip()
    return int(price)

async def text_price():
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')
    name = soup.find('h1').text.strip()
    return str(name)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)