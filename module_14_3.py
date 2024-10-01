from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api = "7114780577:AAHxOHecAlYkeEFZ3L1BZXr74pGDVkIxuMI"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
kb.add(button)
kb.add(button2)
kb.add(button3)

catalog_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Product1', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product2', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product3', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product4', callback_data='product_buying')]
    ]
)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Выберите опцию', reply_markup=kb)


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    for i in range(1, 5):
        product_text = f'Название: Product{i} | Описание: описание {i} | Цена: {i * 100}'
        await message.answer(product_text)
        await message.answer_photo(photo=open(f'{i}.jpeg', 'rb'))
    await message.answer('Выберите продукт для покупки:', reply_markup=catalog_kb)


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.answer('Вы выбрали продукт для покупки. Подтвердите покупку?', show_alert=True)
    confirm_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Подтвердить', callback_data='confirm_buying')],
            [InlineKeyboardButton(text='Отмена', callback_data='cancel_buying')]
        ]
    )
    await call.message.answer('Подтвердите покупку:', reply_markup=confirm_kb)


@dp.callback_query_handler(text="confirm_buying")
async def confirm_buying(call):
    await call.answer('Вы успешно приобрели продукт!')


@dp.callback_query_handler(text="cancel_buying")
async def cancel_buying(call):
    await call.answer('Покупка отменена.')





if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)


