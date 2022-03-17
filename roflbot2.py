import datetime
import logging

import requests
import bs4
from bs4 import BeautifulSoup
from aiogram import *

url = 'https://goo.su/EseK/'
bot = Bot(token='5249454736:AAGR3O6RcXnH3Xcy1zBh8sraQUmFeCtfXYQ')
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def start_command(msg: types.Message):
    await msg.reply('Привет!'
                    '\nЦена на товар может периодически меняться'
                    '\nОбо всех изменениях мы будем сообщать тебе:)')
    date: datetime.datetime = datetime.datetime.now()

    resp: requests.Response = requests.get(url)
    soup: bs4.BeautifulSoup = BeautifulSoup(resp.content, 'html.parser')

    old_price: int = get_price(soup)
    date_format: str = date.strftime("%d/%m/%Y  %H:%M:%S")
    while True:
        resp: requests.Response = requests.get(url)
        soup: bs4.BeautifulSoup = BeautifulSoup(resp.content, 'html.parser')
        actual_price: int = get_price(soup)
        if old_price != actual_price:
            difference: int = old_price - actual_price
            await msg.reply(f'Название товара: {get_text_price(soup)}'
                            f'\nНовая цена: {actual_price}₽'
                            f'\nСтарая цена: {old_price}₽'
                            f'\nДата: {date_format}'
                            f'\nРазница в цене: {difference}₽')
            old_price = actual_price


def get_price(soup: bs4.BeautifulSoup) -> int:
    x = soup.find('span', class_='woocommerce-Price-amount').text.split('.')[0]
    x = x.replace('₽', '')
    return int(x)


def get_text_price(soup: bs4.BeautifulSoup) -> str:
    return str(soup.find('h1', class_='product_title entry-title').text.strip())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
