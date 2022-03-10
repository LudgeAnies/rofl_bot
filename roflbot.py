import datetime
import logging

import bs4
import requests
from aiogram import *
from bs4 import BeautifulSoup

url = 'http://gendalf.cf/'
bot = Bot(token='5249454736:AAGR3O6RcXnH3Xcy1zBh8sraQUmFeCtfXYQ')
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def start_command(msg: types.Message):
    await msg.reply('Привет!\nМы сообщим, как только цена на товар поменяется:)')
    date: datetime.datetime = datetime.datetime.now()

    resp: requests.Response = requests.get(url)
    soup: bs4.BeautifulSoup = BeautifulSoup(resp.content, 'html.parser')

    old_price: int = get_price(soup)
    date_format: str = date.strftime("%d/%m/%Y  %H:%M:%S")
    while True:
        resp: requests.Response = requests.get(url)
        soup: bs4.BeautifulSoup = BeautifulSoup(resp.content, 'html5lib')
        actual_price: int = get_price(soup)
        if old_price != actual_price:
            await msg.reply(f'Название товара: {get_text_price(soup)}'
                            f'\nНовая цена: {actual_price}'
                            f'\nСтарая цена: {old_price}'
                            f'\nДата: {date_format}')
            old_price = actual_price


def get_price(soup: bs4.BeautifulSoup) -> int:
    return int(soup.find('h2').text.strip())


def get_text_price(soup: bs4.BeautifulSoup) -> str:
    return str(soup.find('h1').text.strip())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
