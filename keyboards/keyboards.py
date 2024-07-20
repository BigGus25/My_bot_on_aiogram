from aiogram.types import (CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove)  # кнопки


# Клавиатура для выбора образования (не рааботает отсюда)
# Создаем объекты инлайн-кнопок 
secondary_button = InlineKeyboardButton(text='Среднее', callback_data='secondary')
higher_button = InlineKeyboardButton(text='Высшее', callback_data='higher')
no_edu_button = InlineKeyboardButton(text='🤷 Нету', callback_data='no_edu')

keyboard: list[list[InlineKeyboardButton]] = [[secondary_button, higher_button],[no_edu_button]] # Добавляем кнопки в клавиатуру (две в одном ряду и одну в другом)
markup1 = InlineKeyboardMarkup(inline_keyboard=keyboard)


yes_button = InlineKeyboardButton(text='Да', callback_data='да')
no_button = InlineKeyboardButton(text='Нет', callback_data='нет')
keyboard: list[list[InlineKeyboardButton]] = [[yes_button, no_button]]                      # Добавляем кнопки в клавиатуру (две в одном ряду и одну в другом)
markup2 = InlineKeyboardMarkup(inline_keyboard=keyboard) 

# Создаем объекты инлайн-кнопок для выбора полп
male_button = InlineKeyboardButton(text='Мужской ♂', callback_data='male')
female_button = InlineKeyboardButton(text='Женский ♀',callback_data='female')
undefined_button = InlineKeyboardButton(text='🤷 Пока не ясно',callback_data='undefined_gender')
# Добавляем кнопки в клавиатуру (две в одном ряду и одну в другом)
#keyboard: list[list[InlineKeyboardButton]] = [[male_button, female_button],[undefined_button]]
keyboard: list[list[InlineKeyboardButton]] = [[male_button, female_button]]
# Создаем объект инлайн-клавиатуры
markup3 = InlineKeyboardMarkup(inline_keyboard=keyboard)


# обычная клавиатура решения продолжать игру или нет
but_1: KeyboardButton = KeyboardButton(text='да')
but_2: KeyboardButton = KeyboardButton(text='нет')
but_3: KeyboardButton = KeyboardButton(text='/play')
but_4: KeyboardButton = KeyboardButton(text='/fillform')
but_5: KeyboardButton = KeyboardButton(text='/showdata')
but_6: KeyboardButton = KeyboardButton(text='/weather')
but_7: KeyboardButton = KeyboardButton(text='/time')


choice1_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[but_2, but_1], [but_3, but_6, but_7]], resize_keyboard=True)        # Создаем объект клавиатуры для выбора действия
choice2_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[but_3, but_6,  but_7], [but_4, but_5]], resize_keyboard=True) 
choice3_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[but_5, but_4], [but_3, but_6, but_7]], resize_keyboard=True)

fillform_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[but_4]], resize_keyboard=True) 

yes_no_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[but_2, but_1]], resize_keyboard=True)                  # Создаем объект клавиатуры для ответа играть/не играть


