import asyncio
import logging
import random
import wikipedia, re
import aiohttp                                                             #________________________________________ это для сервера!!! можно не комментить
#________________________________________________________
from aiogram.client.session.aiohttp import AiohttpSession                  #________________________________________ это для сервера!!! можно не комментить
#from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector  #________________________________________ это для сервера!!! 

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import (Message, PhotoSize)
from aiogram.types import (CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove)  # кнопки

from aiogram.filters import Text, Command, StateFilter, CommandStart
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage

# 06/07/2024 ___________________ФОТО_______________________________________________________________________________________________  
from aiogram.types import Message, FSInputFile, InputFile  # для сохранения фото 07/07/2024
import os
all_media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_media')
# 06/07/2024 ___________________ФОТО_______________________________________________________________________________________________  

#from handlers import other_handlers, user_handlers   # их пока нет
from config_reader import config
#from config_data.config import load_config  # загрузка файла конфиг чтоб считать АПИ бота, это из курса

#config = load_config(r'C:\Users\hp\botW.env') # для дома
#config = load_config(r'C:\Users\user\botW.env') # для работы

from keyboards.keyboards import (yes_no_kb, choice1_kb, choice2_kb, choice3_kb, fillform_kb)    # импортируем файл с клавиатурами
from keyboards.keyboards import (markup1, markup2, markup3)
# импорт списков из файла list
from lists.list import (answer_yes_list, answer_YES_list1, answer_YES_list2, answer_NO_list1, answer_NO_list2,
                        answer_magic_ball, Hello_list, Goodbye_list, answer_GoGame_list, answer_OutGame_list,
                        answer_pnh_list, answer_pes_list, stop_list, Good_list, answer_krys_list, anketa_list, help_list)

#session = AiohttpSession(proxy="http://proxy.server:3128")                                     #________________________________________ это для сервера!!!

# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage: MemoryStorage = MemoryStorage()
bot = Bot(token=config.bot_token.get_secret_value())                                           #_____________________________ это для комнадной строки!!!
# bot: Bot= Bot(token=config.bot_token.get_secret_value(), session=session, parse_mode='HTML') #________________________________________ это для сервера!!!
dp: Dispatcher = Dispatcher(storage=storage) # с этим не работает
#dp = Dispatcher(storage=storage)  # а в чем разница с верхней строкой???

# Создаем "базу данных" пользователей
user_dict: dict[int, dict[str, str | int | bool]] = {}

# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодейтсвия с пользователем
    fill_name = State()        # Состояние ожидания ввода имени
    fill_age = State()         # Состояние ожидания ввода возраста
    fill_gender = State()      # Состояние ожидания выбора пола
    upload_photo = State()     # Состояние ожидания загрузки фото
    fill_education = State()   # Состояние ожидания выбора образования
    fill_wish_news = State()   # Состояние ожидания выбора получать ли новости
    fill_start_game = State()  # Состояние начала игры
    fill_continue_game = State() # Состояние продолжение игры
    fill_make_a_choice = State() # Состояние выбора действия после игры
    #first_question = State()    # Состояние ожидания ответа для заполнения анкеты 20.07

#_________________________________HELP____________________________________________________________________________________________________
@dp.message(Command(commands=["help"]), StateFilter(default_state))
@dp.message(Text(text=help_list, ignore_case=True), StateFilter(default_state))
async def process_help_command_state(message: Message, state: FSMContext):
    await message.answer(text="Ниже представлен список доступных команд\n"
                              'Чтобы перейти к заполнению анкеты, '
                              'жми команду /fillform\n'
                              "Чтобы посмотреть данные,\n"
                              'жми команду /showdata\n'
                              'Чтобы поиграть в магический шар,\n'
                              'жми команду /play\n'
                              'Чтобы глянуть прогноз погоды,\n'
                              'жми команду /weather\n'
                              'Чтобы глянуть мировое время,\n'
                              'жми команду /time', reply_markup=choice2_kb)
#_________________________________HELP____________________________________________________________________________________________________

#_________________________________WEATHER_________________________________________________________________________________________________
# Этот хэндлер будет срабатывать на команду "/weather"
@dp.message(Command(commands=["weather"]), StateFilter(default_state))                              #сработает на команду
@dp.message(Text(text='погода', ignore_case=True), StateFilter(default_state))                      #сработает на "погода"
async def process_weather_command(message: Message):
    # Создаем объекты инлайн-кнопок
    url_button_1: InlineKeyboardButton = InlineKeyboardButton(
        text='Яндекс прогноз',
        url='https://yandex.ru/pogoda/samara?lat=53.195876&lon=50.100199')
    url_button_2: InlineKeyboardButton = InlineKeyboardButton(
        text='Gismeteo',
        url='https://www.gismeteo.ru/weather-samara-4618/')
    # Создаем объект инлайн-клавиатуры
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[[url_button_1],[url_button_2]])
    await message.answer(text="Нажми на кнопку,\nчтоб глянуть погоду на сайте", reply_markup=keyboard)
#_________________________________WEATHER_________________________________________________________________________________________________

#_________________________________TIME____________________________________________________________________________________________________
# Этот хэндлер будет срабатывать на команду "/time"
@dp.message(Command(commands=["time"]), StateFilter(default_state))                           #сработает на команду
@dp.message(Text(text='время', ignore_case=True), StateFilter(default_state))                 #сработает на "время"
async def process_time_command(message: Message):
    # Создаем объекты инлайн-кнопок
    url_button_1: InlineKeyboardButton = InlineKeyboardButton(
        text='Время по Гринвичу',
        url='https://time100.ru/GMT')
    # Создаем объект инлайн-клавиатуры
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[url_button_1]])
    await message.answer(text="Нажми на кнопку,\nчтоб увидеть время", reply_markup=keyboard)
#_________________________________TIME____________________________________________________________________________________________________

#________________________________CANCEL___________________________________________________________________________________________________
# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях, кроме состояния по умолчанию, и отключать машину состояний   
@dp.message(Command(commands='cancel'), ~StateFilter(default_state))                            #сработает на команду
@dp.message(Text(text=Goodbye_list, ignore_case=True), ~StateFilter(default_state))             #сработает на прощание
@dp.message(Text(text=stop_list, ignore_case=True), ~StateFilter(default_state))
#@dp.message(Text(text=answer_OutGame_list, ignore_case=True), ~StateFilter(default_state))      #сработает на просьбу выйти из игры
#@dp.message(Text(text=answer_NO_list1, ignore_case=True), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    answer = message.text.lower();
    if answer in Goodbye_list:
        await message.answer(text='До свидания, всего доброго тебе, {0.first_name}!'.format(message.from_user))
        await state.clear()
    else:
        await message.answer(text='[~(default_state)]\nМы вышли из машины состояний\n\n'
                              'Чтобы перейти к заполнению анкеты, '
                              'жми команду /fillform\n'
                              "Чтобы посмотреть данные,\n"
                              'жми команду /showdata\n'
                              'Чтобы поиграть в магический шар,\n'
                              'жми команду /play\n'
                              'Чтобы глянуть прогноз погоды,\n'
                              'жми команду /weather', reply_markup=choice2_kb)
        await state.clear()                                                                     # Сбрасываем состояние

@dp.message(Command(commands='cancel'), StateFilter(default_state)) # 12/06/2024 Добавил cancel, чтоб всегда можно было выйти всегда. не пойму почему раньше так не сделал
@dp.message(Text(text=Goodbye_list, ignore_case=True), StateFilter(default_state))             #сработает на прощание
@dp.message(Text(text=stop_list, ignore_case=True), StateFilter(default_state))
#@dp.message(Text(text=answer_OutGame_list, ignore_case=True), StateFilter(default_state))      #сработает на просьбу выйти из игры
#@dp.message(Text(text=answer_NO_list1, ignore_case=True), StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    answer = message.text.lower();
    if answer in Goodbye_list:
        await message.answer(text='До свидания, всего доброго тебе, {0.first_name}!'.format(message.from_user))
        await state.clear()
    else:
        await message.answer(text='[~(default_state)]\nМы вышли из машины состояний\n\n'
                              'Чтобы перейти к заполнению анкеты, '
                              'жми команду /fillform\n'
                              "Чтобы посмотреть данные,\n"
                              'жми команду /showdata\n'
                              'Чтобы поиграть в магический шар,\n'
                              'жми команду /play\n'
                              'Чтобы глянуть прогноз погоды,\n'
                              'жми команду /weather', reply_markup=choice2_kb)
        await state.clear()
#________________________________CANCEL___________________________________________________________________________________________________

# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]), StateFilter(default_state))                            #сработает на команду
@dp.message(Text(text=Hello_list, ignore_case=True), StateFilter(default_state))                #сработает на приветствие
async def process_start_command(message: Message):
    answer = message.text.lower();
    if answer in ["ты тут?", "ты тут", "тут?", "тут", "здесь?", "здесь", "ты здесь?", "ты здесь"]:
        await message.answer(text="Конечно! Рад тебя видеть, {0.first_name}!\n\n"
                         'Заполнишь анкету? [да/нет][/fillform]?\n'
                         'Или:\n'
                         'Жми /play, чтобы начать игру.\n'
                         'Жми /weather, чтобы посмотреть прогноз погоды.\n'
                         'Жми /time, чтобы узнать время.\n'
                         #'Жми /wiki, чтоб получать\n'
                         #"значения слов из википедии."
                         .format(message.from_user), reply_markup=choice1_kb)
        #await state.set_state(FSMFillForm.first_question                               #20/07/2024г
    else:
        await message.answer(text="Привет, {0.first_name}! я тестовый бот!\n\n"
                         'Давай знакомиться! [да/нет][/fillform]?\n'
                         'Или:\n'
                         'Жми /play, чтобы начать игру.\n'
                         'Жми /weather, чтобы посмотреть прогноз погоды.\n'
                         'Жми /time, чтобы узнать время.\n'
                         #'Жми /wiki, чтоб получать\n'
                         #"значения слов из википедии."
                         .format(message.from_user), reply_markup=choice1_kb)
        #await state.set_state(FSMFillForm.first_question)                              #20/07/2024г

# Этот хэндлер будет срабатывать на текст из положительного списка
# и переводить бота в состояние ожидания ввода имени
@dp.message(Command(commands=['fillform']), StateFilter(default_state))                           #сработает на команду
@dp.message(Text(text=answer_yes_list, ignore_case=True), StateFilter(default_state))
@dp.message(Text(text=anketa_list, ignore_case=True), StateFilter(default_state))
async def process_fillform_command(message: Message, state: FSMContext):
    await message.answer(text='Меня ты уже знаешь, я весёлый бот:)\n'
                                'А кто ты? Напиши своё имя.', reply_markup=ReplyKeyboardRemove())          # Удаление клавиатуры!!!!
    await state.set_state(FSMFillForm.fill_name)                                                           # Устанавливаем состояние ожидания ввода имени

# Этот хэндлер будет срабатывать, если введено корректное имя
# и переводить в состояние ожидания ввода возраста
@dp.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    await state.update_data(name=message.text)                                                  # Cохраняем введенное имя в хранилище по ключу "name"
    await message.answer(text='Спасибо!\nА теперь напиши свой возраст')                         # Устанавливаем состояние ожидания ввода возраста
    await state.set_state(FSMFillForm.fill_age)

# Этот хэндлер будет срабатывать, если во время ввода имени
# будет введено что-то некорректное
@dp.message(StateFilter(FSMFillForm.fill_name))
async def warning_not_name(message: Message):
    await message.answer(text='То, что вы отправили не похоже на имя.\n'
                              'Пожалуйста, введите ваше имя.\n\n'
                              'Если хотите прервать заполнение анкеты - отправьте команду /cancel')

# Этот хэндлер будет срабатывать, если введен корректный возраст и переводить в состояние выбора образования
@dp.message(StateFilter(FSMFillForm.fill_age), lambda x: x.text.isdigit() and 1 <= int(x.text) <= 120)
async def process_age_sent(message: Message, state: FSMContext):
    await state.update_data(age=message.text)                                                    # Cохраняем возраст в хранилище по ключу "age"\
    await message.answer(text='Спасибо!\nУкажи свой пол', reply_markup=markup3)
    await state.set_state(FSMFillForm.fill_gender)  # Устанавливаем состояние ожидания выбора пола 
 
# Этот хэндлер будет срабатывать, если во время ввода возраста будет введено что-то некорректное
@dp.message(StateFilter(FSMFillForm.fill_age))
async def warning_not_age(message: Message):
    await message.answer(
        text='Возраст должен быть целым числом от 1 до 120\n\n'
             'Попробуй еще раз\n\n'
             'Если хочешь прервать заполнение анкеты - отправь команду /cancel')
             
# 20/07/2024 ___________________SEX_______________________________________________________________________________________________
# Этот хэндлер будет срабатывать на нажатие кнопки при
# выборе пола и переводить в состояние отправки фото
#@dp.callback_query(StateFilter(FSMFillForm.fill_gender), F.data.in_(['male', 'female', 'undefined_gender']))
#@dp.callback_query(StateFilter(FSMFillForm.fill_gender), F.data.in_(['male', 'female']))
@dp.callback_query(StateFilter(FSMFillForm.fill_gender), Text(text=['male', 'female']))
async def process_gender_press(callback: CallbackQuery, state: FSMContext):
    await state.update_data(gender=callback.data)                                               # Cохраняем пол (callback.data нажатой кнопки) в хранилище, по ключу "gender"
    await callback.message.edit_text(text='Кнопка уже нажата,\nне тыкай на неё', reply_markup=callback.message.reply_markup)
    await callback.message.answer(text='Спасибо! А теперь загрузи, пожалуйста, своё фото')
    await state.set_state(FSMFillForm.upload_photo)  # Устанавливаем состояние ожидания загрузки фото

# Этот хэндлер будет срабатывать, если во время выбора пола
# будет введено/отправлено что-то некорректное
@dp.message(StateFilter(FSMFillForm.fill_gender))
async def warning_not_gender(message: Message):
    await message.answer(
        text='Пожалуйста, пользуйся кнопками при выборе пола\n\n'
             'Если хочешь прервать заполнение анкеты - отправь команду /cancel')
# 20/07/2024 ___________________SEX_______________________________________________________________________________________________
 
# 06/07/2024 ___________________ФОТО_______________________________________________________________________________________________
# Этот хэндлер будет срабатывать, если отправлено фото и переводить в состояние выбора образования 
@dp.message(StateFilter(FSMFillForm.upload_photo),
            F.photo[-1].as_('largest_photo'))
async def process_photo_sent(message: Message, state: FSMContext, largest_photo: PhotoSize):
    # Cохраняем данные фото (file_unique_id и file_id) в хранилище по ключам "photo_unique_id" и "photo_id"
    await state.update_data(
        photo_unique_id=largest_photo.file_unique_id,
        photo_id=largest_photo.file_id
    ) 
    await message.answer(text='Спасибо! Классная фотка!\n\nУкажи своё образование', reply_markup=markup1)      # Отправляем пользователю сообщение с клавиатурой
    await state.set_state(FSMFillForm.fill_education)                                            # Устанавливаем состояние ожидания выбора образования
 
# Этот хэндлер будет срабатывать, если во время отправки фото будет введено/отправлено что-то некорректное
@dp.message(StateFilter(FSMFillForm.upload_photo))
async def warning_not_photo(message: Message, state: FSMContext):
#async def warning_not_photo(message: Message, state: FSMContext):
    answer = message.text.lower();
    if answer in ["в другой раз", "без фото", "не хочу отправлять", "не хочу отправлять фото", "не отправлю", "давай без фото", "не хочу", "не буду", "да ну", "не загружу", "хм"]:
        # Отправляем стандартное фото и получаем file_id
        #__1_______________
        #photo_message = await bot.send_photo(message.chat.id, photo=open('avatar1.png', 'rb')) # не работает, может URL вставить
        #__2_______________
        photo_file = FSInputFile(path=os.path.join(all_media_dir, 'avatar1.png'))
        photo_message =await bot.send_photo(message.chat.id, photo=photo_file)
        # файлом или URL
        #photo_url  = 'https://avatars.mds.yandex.net/i?id=f7db9440cebfe2991388e177c8c1b485b0168eea6904916f-4055877-images-thumbs&n=13' #19/07
        #photo_message =await bot.send_photo(message.chat.id, photo=photo_url)
        # или так
        #photo_message= await message.answer_photo(message.chat.id, photo=photo_url)
        #await message.answer(text='тогда вот твоя аватарка по умолчанию')
        
        #__3_______________
        #with open('avatar1.png', 'rb') as photo:                                          # не работает, не знаю почему
        #photo_message = await bot.send_photo(message.chat.id, photo=photo)
                
        await state.update_data(
            #photo_unique_id=photo_message.file_unique_id,
            photo_id=photo_message.photo[-1].file_id  # Получаем file_id последнего фото в массиве
        )
        await message.answer(
            text='Выше твоя аватарка, раз тебе фотку лень скинуть.'
            '\nЕсли хочешь прервать заполнение анкеты - отправь команду /cancel'
            '\nДля продолжения, введи образование', reply_markup=markup1) 
        await state.set_state(FSMFillForm.fill_education)                                            # Устанавливаем состояние ожидания выбора образования
    else:
        await message.answer(text='Пожалуйста, на этом шаге отправь своё фото для анкеты\n')
# 06/07/2024 ___________________ФОТО_______________________________________________________________________________________________       
     
# Этот хэндлер будет срабатывать, если выбрано образование
@dp.callback_query(StateFilter(FSMFillForm.fill_education), Text(text=['secondary', 'higher', 'no_edu']))
async def process_education_press(callback: CallbackQuery, state: FSMContext):
    #await state.update_data(education=callback.data)                                            # Cохраняем данные об образовании по ключу "education"
    await callback.message.edit_text(text='Кнопка уже нажата,\nне тыкай на неё', reply_markup=callback.message.reply_markup)
    await state.update_data(education=callback.data)                                            # Cохраняем данные об образовании по ключу "education"
    user_dict[callback.from_user.id] = await state.get_data()                                   # Добавляем в "базу данных" анкету пользователя по ключу id пользователя
    await state.clear()                                                                         # Завершаем машину состояний
    await callback.message.answer(text='Отлично! Данные сохранены!\nВыходим из машины состояний', reply_markup=choice2_kb) # Отправляем в чат сообщение о выходе из машины состояний

# Этот хэндлер будет срабатывать, если во время выбора образования
# будет введено/отправлено что-то некорректное
@dp.message(StateFilter(FSMFillForm.fill_education))
async def warning_not_education(message: Message):
    await message.answer(text='Пожалуйста, пользуйся кнопками при выборе образования\n\n'
                              '\nЕсли хочешь прервать заполнение анкеты - отправь команду /cancel')

# Этот хэндлер будет срабатывать на отправку команды /showdata
# и отправлять в чат данные анкеты, либо сообщение об отсутствии данных
@dp.message(Command(commands=['showdata']), StateFilter(default_state))
async def process_showdata_command(message: Message):
    # Отправляем пользователю анкету, если она есть в "базе данных"
    if message.from_user.id in user_dict:
        #await message.answer( # 06/07 заккоментил
        await message.answer_photo(
            photo=user_dict[message.from_user.id]['photo_id'],
            #text= 
            caption=f'Имя: {user_dict[message.from_user.id]["name"]}\n'
                    f'Возраст: {user_dict[message.from_user.id]["age"]}\n'
                    f'Пол: {user_dict[message.from_user.id]["gender"]}\n'
                    f'Образование: {user_dict[message.from_user.id]["education"]}\n', reply_markup=choice2_kb)
                    #f'Получать новости: {user_dict[message.from_user.id]["wish_news"]}')
        await state.set_state(FSMFillForm.fill_make_a_choice)
    else:
        await message.answer(text='Вы еще не заполняли анкету. '                                # Если анкеты пользователя в базе нет - предлагаем заполнить
                                  'Чтобы приступить - отправьте '
                                  'команду /fillform', reply_markup=fillform_kb)
        await state.set_state(FSMFillForm.fill_make_a_choice)

# Этот хэндлер будет срабатывать на команду "/play"
@dp.message(Command(commands=['play']), StateFilter(default_state))                             #сработает на команду
@dp.message(Text(text=answer_GoGame_list, ignore_case=True), StateFilter(default_state))        #сработает на желание сыграть
async def process_play_command(message: Message, state: FSMContext):
    await message.answer('Хороший выбор!\nБудем играть в магический шар.\n'
                         'я буду магическим шаром:\nзадавай любой вопрос, а я дам ответ.', reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMFillForm.fill_start_game) # cостояние начала игры

# Этот хэндлер будет срабатывать на текст
@dp.message(F.text, StateFilter(FSMFillForm.fill_start_game))
async def get_game(message: Message, state: FSMContext):
    await message.reply(text=random.choice(answer_magic_ball))                                  # эхо сообщение
    await message.answer("\nБудут ещё вопросы?", reply_markup=markup2)
    #await message.answer(text="\nБудут ещё вопросы?", reply_markup=yes_no_kb)
    await state.set_state(FSMFillForm.fill_continue_game)

#____________________________________________________________________________________________________________________________________________________________________________
@dp.callback_query(StateFilter(FSMFillForm.fill_continue_game), Text(text= ['да', 'нет']))     # ответ инлайн клавиатурой
async def process_play_press(callback: CallbackQuery, state: FSMContext):
    answer = callback.data

    if answer == "да":
        await callback.message.answer('Хорошо :)\nПиши свой вопрос.')
        await state.set_state(FSMFillForm.fill_start_game)
        await callback.message.edit_text(text='на вопрос: "Будут ещё вопросы?"\nты ответил - да\nбольше не жми на клавиши', reply_markup=callback.message.reply_markup)

    elif answer == "нет":
        await callback.message.answer('Тогда топай в начало.', reply_markup=choice2_kb)
        #await state.set_state(FSMFillForm.fill_make_a_choice)
        await state.clear()
        await callback.message.edit_text(text='на вопрос: "Будут ещё вопросы?"\nты ответил - нет\nбольше не жми на клавиши', reply_markup=callback.message.reply_markup)

@dp.message(FSMFillForm.fill_continue_game)                                                     # отвечать только кнопками, он не сработает пока хэндлер на слова работает
async def warning_not_play_press(message: Message):
    await message.answer(text="Пожалуйста, пользуйтесь кнопками\n"
                              'Если вы хотите прервать игру - отправьте команду /cancel')
    await message.answer("\nБудут ещё вопросы?", reply_markup=markup2)
    await state.set_state(FSMFillForm.fill_continue_game)
#_______________________________________________________________________________________________________________________________________________________________________________
# Этот хэндлер будет срабатывать на любые сообщения,
# кроме тех для которых есть отдельные хэндлеры, вне состояний
@dp.message(StateFilter(default_state))
async def send_echo(message: Message, state: FSMContext):
    answer = message.text.lower();

    if answer in answer_NO_list1 or answer in answer_NO_list2 or answer in answer_OutGame_list:
        await message.answer('Тогда сам выбери что хочешь:\n'
                            "заполнить анкету /fillform\n"
                            "посмотреть анкету /showdata\n"
                            "играть /play\n", reply_markup=choice2_kb);
    elif answer in answer_pnh_list:
        await message.reply(text='[(default_state)]\nОхренел? пшел вон отсюда!!!\n', reply_markup=choice2_kb);  
    elif answer in Good_list:
        await message.reply(text='[(default_state)]\nТы меня таким сделал!\nВсё это благодаря Тебе!\nТы потрясающий!\n', reply_markup=choice2_kb);
    elif answer in answer_pes_list or answer in answer_krys_list:
        await message.reply(text='[(default_state)]\nАхахах! Сам такой!\n'
                                'заполни анкетку! [да/нет][/fillform]?\n'
                                'Или:\n'
                                'Жми /play, чтобы начать игру.\n'
                                'Жми /weather, чтобы посмотреть прогноз погоды.\n'
                                'Жми /time, чтобы узнать время.\n', reply_markup=choice1_kb); 
    else:
        await message.reply(text='[(default_state)]\nИзвини, моя твоя не понимать\n'
                        "Выбери на клавиатуре что-нибудь\n", reply_markup=choice2_kb);                            
#_________________________16/06/2024   

# Этот хэндлер будет срабатывать на любые сообщения, которые отправляются из состояния просмотра данных
# по факту он не работает никогда! в это состояние программа не заходит, не пойму только почему.
@dp.message(StateFilter(FSMFillForm.fill_make_a_choice))
#@dp.message(StateFilter(FSMFillForm.fill_make_a_choice), F.text.isalpha()) 
async def send_echo(message: Message, state: FSMContext):
    answer = message.text.lower();

    if answer in answer_NO_list1 or answer in answer_NO_list2 or answer in answer_OutGame_list:
        await message.answer('[(fill_make_a_choice)]\nТогда сам выбери что хочешь:\n'
                            "заполнить анкету /fillform\n"
                            "посмотреть анкету /showdata\n"
                            "играть /play\n", reply_markup=choice2_kb);
    elif answer in answer_pnh_list:
        await message.reply(text='[(fill_make_a_choice]\nОхренел? пшел вон отсюда!!!\n', reply_markup=choice2_kb);     
    elif answer in Good_list:
        await message.reply(text='[(fill_make_a_choice)]\nТы меня таким сделал!\nВсё это благодаря Тебе!\nТы потрясающий!\n', reply_markup=choice2_kb);
    elif answer in answer_pes_list or answer in answer_krys_list:
        await message.reply(text='[(fill_make_a_choice)]\nАхахах! Сам такой!\n'
                                'заполни анкетку! [да/нет][/fillform]?\n'
                                'Или:\n'
                                'Жми /play, чтобы начать игру.\n'
                                'Жми /weather, чтобы посмотреть прогноз погоды.\n'
                                'Жми /time, чтобы узнать время.\n', reply_markup=choice1_kb); 
    else:
        await message.reply(text='[(fill_make_a_choice)]\nИзвини, моя твоя не понимать\n'
                        "Выбери на клавиатуре что-нибудь\n", reply_markup=choice2_kb); 
                        
    await state.clear()  

#_______________________________________________________________________________
#место под вики
#_______________________________________________________________________________

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":  # эти две строки пока не понимаю
    asyncio.run(main())