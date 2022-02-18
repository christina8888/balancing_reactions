import logging
from aiogram import Dispatcher, Bot, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from bot_code import balance
from aiogram.dispatcher.filters.state import StatesGroup, State
from keyboard import keyboard, keyboard1, keyboard2
from os import getenv
from sys import exit

bot_token = getenv("token")
if not bot_token:
    exit("Error: no token provided")

bot_url = getenv("url_app")

bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot, storage=MemoryStorage())

# async def on_startup(dp):
#     await bot.set_webhook(bot_url)
#
# async def on_shutdown(dp):
#     await bot.delete_webhook()

logging.basicConfig(level=logging.INFO)


class FormulaInput(StatesGroup):
    waiting_for_reac = State()
    waiting_for_prod = State()


async def welcome(message: types.Message):
    await message.answer("<b>Привет!</b> Я помогу вам сбалансировать любое химическое уравнение.",
                         reply_markup=keyboard)


async def template(message: types.Message):
    await message.answer("""
Реактанты и продукты должны быть написаны <u>латиницей, заглавными буквами, строго через пробел</u>, иначе я ничего не пойму :(
    
Например, вы хотите сбалансировать уравнение H2 + O2 -> H2O. 
Когда я попрошу вас написать реактанты, следует сделать это так: <b>H2 O2</b>.
Когда я попрошу вас написать продукты, следует сделать это так: <b>H2O</b>.
    
Обязательно проверяйте, существует ли вообще уравнение, написанное вами, ведь я пока не умею этого делать.   
    """)


async def start_input(message: types.Message):
    await FormulaInput.waiting_for_reac.set()
    await message.answer(f"Укажите реактанты через пробел:", reply_markup=keyboard1)


async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("OK. Начать заново?", reply_markup=keyboard2)


async def no(message: types.Message, state: FSMContext):
    await message.answer("Пока!", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


async def input_reac(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['reac'] = message.text
    await FormulaInput.next()
    await message.answer(f"Укажите продукты через пробел:", reply_markup=keyboard1)


async def input_prod(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['prod'] = message.text
        result = balance(data['reac'], data['prod'])
        if result == "Неверный ввод реактантов или продуктов":
            await message.answer("Не понимаю. Пожалуйста, воспользуйтесь кнопкой 'Помощь'.", reply_markup=keyboard)
        else:
            await message.answer(result, reply_markup=keyboard)
        await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(welcome, commands="start")
    dp.register_message_handler(template, Text(equals="Помощь"))
    dp.register_message_handler(start_input, Text(equals=["Уравнять формулу", "Да"]), state=None)
    dp.register_message_handler(cancel, Text(equals="Отмена"), state="*")
    dp.register_message_handler(no, Text(equals="Нет"), state="*")
    dp.register_message_handler(input_reac, state=FormulaInput.waiting_for_reac)
    dp.register_message_handler(input_prod, state=FormulaInput.waiting_for_prod)


register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



    # executor.start_webhook(
    #     dispatcher=dp,
    #     webhook_path='',
    #     on_startup=on_startup,
    #     on_shutdown=on_shutdown,
    #     skip_updates=True,
    #     host="0.0.0.0",
    #     port=int(os.environ.get("PORT", 5000))
    # )
