from aiogram import types

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ["Помощь", "Уравнять формулу"]
keyboard.add(*buttons)

keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
cancel_button = "Отмена"
keyboard1.add(cancel_button)

keyboard2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
yes_or_no_buttons = ["Да", "Нет"]
keyboard2.add(*yes_or_no_buttons)
