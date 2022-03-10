from aiogram import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import logging
from time import sleep
bot = Bot(token='5249454736:AAGR3O6RcXnH3Xcy1zBh8sraQUmFeCtfXYQ')
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Привет!\nМы сообщим, как только цена на товар поменяется:)')
    old_price = new_price()[1]
    while True:
        if old_price != new_price()[1]:
            await message.reply(f'Новая цена: {new_price()[1]}\n Старая цена: {old_price}\n Цена изменилась на {old_price - new_price()[1]}')
        else:
            continue
        sleep(3)


async def new_price():
    chrome_options = Options()
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get('http://gendalf.cf/')
    text = driver.find_element(By.TAG_NAME, 'h1').text
    price = int(driver.find_element(By.TAG_NAME, 'h2')).text
    return text, price

bot.polling(none_stop=True, interval=0)

