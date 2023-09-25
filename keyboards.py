from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

btn1 = InlineKeyboardButton("Зашифровать файл", callback_data='enc')
btn2 = InlineKeyboardButton("Расшифровать файл", callback_data='dec')

kb_start = InlineKeyboardMarkup().add(btn1, btn2)

