import telebot
import random # для магического шара
from telebot import types
import wikipedia, re # для вики и для очистки строки

token='5890018206:AAHzVz2TCPqbC-k3yMXzril6wPeSy-5P1DQ'
bot=telebot.TeleBot(token)

name = '';
surname = '';
age = 0;
answer=''

#__________________________________________________списки_____________________________________________________________________________________________________________________________________________________________________
answer_magic_ball=["Бесспорно", "Мне кажется - да", "Однозначно - да", "Пока не ясно, попробуй снова", "Даже не думай",
           "Предрешено, так и будет", "Вероятнее всего", "Спроси позже", "Мой ответ - нет",
           "Никаких сомнений", "Хорошие перспективы", "Лучше не рассказывать", "По моим данным - нет",
           "Можешь быть уверен в этом", "Да", "Сконцентрируйся и спроси опять", "Весьма сомнительно", "Даже не знаю", "Предрешено, ответ узнаешь потом"]

Hello_list=["привет", "здорова", "ку", "хай", "helloy", "hello", "приветули", "приветик", "добрый день", "доброе утро", "добрый вечер", "здоров"]
Goodbye_list=["пока", "до свидания", "всего доброго", "goodbuy", "покедосики", "пакедосики", "чау", "досвидули", "досвидания", "пакедова", "покедова", "до скорого", "всего хорошего", "доброй ночи"]

answer_YES_list1=["хорошо", "давай", "yes", "ok", "да давай", "ну ок", "ок", "да", "конечно", "да конечно", "само собой", 'да правильно', "правильно", 'естественно', "ну давай", "да ок", "согласен", "ага", "угу"]
answer_NO_list1=["no", "нет", "не хочу", "хз", "нахрен надо", "нее", "неа", "не", "не буду", "ничего не хочу"]

answer_YES_list2=["будут", "конечно будут", "да будут"]
answer_NO_list2=["не будет", 'нет не будет', "пока нет", "пока что нет", "пока что нету"  "пока не будет", "пока что не будет", "нету"]

answer_GoGame_list=['хочу играть', 'давай играть', 'играть', "пошли играть", "play", "плай", "шар", "магический шар", "magic"]
answer_OutGame_list=["я передумал", "не хочу", "давай заново", "давай в начало", "я передумал, давай в начало", "не надо"]

answer_pnh_list=["иди на", "фак ю", "тварь", "питор", "ты питор", "ты петушара", "петушара", "петух", "ты что псина", "ты что пес", "ты что пёс", "чмо", "лох", "пес", "ты пес", "псина", "шакал", "ты псина", "пёс", "ты пёс", "иди ты", "пошёл ты", "пошел ты", "да иди ты", "да пошёл ты", "да пошел ты", "иди нафиг", "иди нахрен", "иди нахер", "да иди нафиг", "да иди нахрен", " да иди нахер", "да иди ты нафиг", "да иди ты нахрен", " да иди ты нахер", "да пошел ты нафиг", "да пошел ты нахрен", "да пошел ты нахер"]
answer_pes_list=['привет пес', 'привет пёс', 'здорова пёс', 'здорова пес', 'привет псина', 'здорова псина', 'хай псина', 'хай пес', 'привет шакал', 'хай шакал', 'здорова шакал']

stop_list=['stop', 'hare', "out"]
#__________________________________________________списки_____________________________________________________________________________________________________________________________________________________________________

@bot.message_handler(content_types=['text'])
def start(message):
    answer = message.text.lower();

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("start")
    btn2 = types.KeyboardButton("regy")
    btn3 = types.KeyboardButton("play")
    btn4 = types.KeyboardButton("wiki")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4) # специально поставил, чтоб не было прошлых кнопок

    if answer == '/start' or answer == 'start' or answer == 'старт' or answer in Hello_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("play")
        btn2 = types.KeyboardButton("wiki")
        btn3 = types.KeyboardButton("да")
        btn4 = types.KeyboardButton("нет")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4)

        bot.send_message(message.from_user.id, text="Привет, {0.first_name}! я весёлый, тестовый бот!\nДавай знакомиться [да/нет]?\nИли:\nЖми /play, чтобы начать игру.\nЖми /wiki, чтоб получать\nзначения слов из википедии.".format(message.from_user), reply_markup=markup);
        bot.register_next_step_handler(message, start_two); #следующий шаг – функция start_two
    elif answer in answer_pes_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("да")
        btn2 = types.KeyboardButton("нет")
        markup.add(btn1, btn2) # специально поставил, чтоб не было прошлых кнопок

        bot.send_message(message.from_user.id, 'Как грубо! я маленький веселый бот!\nБудем знакомиться [да/нет]?\nИли:\nЖми /play, чтобы начать игру.\nЖми /wiki, чтоб получать\nзначения слов из википедии.', reply_markup=markup);
        bot.register_next_step_handler(message, start_two);
    elif answer in Goodbye_list:
        bot.send_message(message.from_user.id, "До свидания, всего доброго тебе!", reply_markup=markup);
        bot.register_next_step_handler(message, start);
    elif answer in answer_pnh_list:
        bot.send_message(message.from_user.id, "Ты что, пёс?!\nТопай отсюда!", reply_markup=markup);
        bot.register_next_step_handler(message, start);
    elif answer == '/play' or answer in answer_GoGame_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("regy")
        btn2 = types.KeyboardButton("play")
        btn3 = types.KeyboardButton("wiki")

        bot.send_message(message.from_user.id, 'Хороший выбор!\nПредлагаю поиграть в магический шар.\nя буду магическим шаром:\nзадай любой вопрос, а я дам ответ.', reply_markup=markup);
        bot.register_next_step_handler(message, get_game); #следующий шаг – функция get_game
#______________________________________________________википедия_____________________________________________________
    elif answer == '/startwiki' or answer == '/wiki' or answer == 'википедия' or answer == 'wiki' or answer == 'вики':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("out wiki")
        markup.add(btn1)

        bot.send_message(message.from_user.id, 'Понял. Перевожу на вики.\nОтправь мне любое слово, и я найду его значение на Wikipedia.\nЧтобы выйти, введи: [/stop, /hare, /out].', reply_markup=markup);
        bot.register_next_step_handler(message, handle2_text);
#______________________________________________________википедия_____________________________________________________
    elif answer =='/regy' or answer == "regy" :
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("да")
        btn2 = types.KeyboardButton("нет")
        markup.add(btn1, btn2)

        bot.send_message(message.from_user.id, 'Давай начнём знакомство! Хорошо?', reply_markup=markup);
        bot.register_next_step_handler(message, start_two);
    else:
        bot.send_message(message.from_user.id, 'Напиши "Привет", чтобы начать знакомство\nили нажми /start или /regy.\nЖми /play, чтобы начать игру.nЖми /wiki, чтоб получать\nзначения слов из википедии.', reply_markup=markup);
        bot.register_next_step_handler(message, start)
#################################################################################################################################################################################################################
def start_two(message):
    answer = message.text.lower();
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("regy")
    btn2 = types.KeyboardButton("play")
    btn3 = types.KeyboardButton("wiki")
    markup.add(btn1, btn2, btn3) # специально поставил, чтоб не было прошлых кнопок

    if answer in answer_YES_list1 or answer == "давай знакомиться" or answer == "знакомиться":
        bot.send_message(message.from_user.id, 'Меня ты уже знаешь, я весёлый бот:)\nА кто ты? Напиши своё имя.', reply_markup=markup);
        bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name
    elif answer in answer_NO_list1 or answer in answer_OutGame_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("start")
        btn2 = types.KeyboardButton("regy")
        btn3 = types.KeyboardButton("play")
        btn4 = types.KeyboardButton("wiki")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4) # специально поставил, чтоб не было прошлых кнопок

        bot.send_message(message.from_user.id, 'Ну и говнюк!\nВозвращайся в начало и пиши, что хочешь.', reply_markup=markup);
        bot.register_next_step_handler(message, start);
    elif answer in answer_pes_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("да")
        btn2 = types.KeyboardButton("нет")
        markup.add(btn1, btn2) # специально поставил, чтоб не было прошлых кнопок

        bot.send_message(message.from_user.id, 'Как грубо! я маленький веселый бот!\nБудем знакомиться [да/нет]?\nИли:\nЖми /play, чтобы начать игру.\nЖми /wiki, чтоб получать\nзначения слов из википедии.', reply_markup=markup);
        bot.register_next_step_handler(message, start_two);
    elif answer in Goodbye_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("start")
        btn2 = types.KeyboardButton("regy")
        btn3 = types.KeyboardButton("play")
        btn4 = types.KeyboardButton("wiki")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4) # специально поставил, чтоб не было прошлых кнопок

        bot.send_message(message.from_user.id, "До свидания, всего доброго тебе!", reply_markup=markup);
        bot.register_next_step_handler(message, start);
    elif answer in answer_pnh_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("start")
        btn2 = types.KeyboardButton("regy")
        btn3 = types.KeyboardButton("play")
        btn4 = types.KeyboardButton("wiki")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4) # специально поставил, чтоб не было прошлых кнопок

        bot.send_message(message.from_user.id, "Ты что, пёс?!\nТопай отсюда!", reply_markup=markup);
        bot.register_next_step_handler(message, start);
    elif answer == '/play' or answer in answer_GoGame_list:
        bot.send_message(message.from_user.id, 'Хороший выбор!\nПредлагаю поиграть в магический шар.\nя буду магическим шаром:\nзадай любой вопрос, а я дам ответ.',reply_markup=markup);
        bot.register_next_step_handler(message, get_game); #следующий шаг – функция get_game
#______________________________________________________википедия_____________________________________________________
    elif answer == '/startwiki' or answer == '/wiki' or answer == 'википедия' or answer == 'wiki' or answer == 'вики':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("out wiki")
        markup.add(btn1)

        bot.send_message(message.from_user.id, 'Понял. Перевожу на вики.\nОтправь мне любое слово, и я найду его значение на Wikipedia.\nЧтобы выйти, введи: [/stop, /hare, /out].', reply_markup=markup);
        bot.register_next_step_handler(message, handle2_text);
#______________________________________________________википедия_____________________________________________________
    elif answer == '/start' or answer == 'start' or answer == 'старт' or answer in Hello_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("play")
        btn2 = types.KeyboardButton("wiki")
        btn3 = types.KeyboardButton("да")
        btn4 = types.KeyboardButton("нет")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4)

        bot.send_message(message.from_user.id, text="Привет, {0.first_name}! я весёлый, тестовый бот!\nДавай знакомиться [да/нет]?\nИли:\nЖми /play, чтобы начать игру.\nЖми /wiki, чтоб получать\nзначения слов из википедии.".format(message.from_user), reply_markup=markup);
        bot.register_next_step_handler(message, start_two); #следующий шаг – функция start_two
    elif answer =='/regy' or answer == "regy":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("да")
        btn2 = types.KeyboardButton("нет")
        markup.add(btn1, btn2)

        bot.send_message(message.from_user.id, 'Давай начнём знакомство! Хорошо?', reply_markup=markup);
        bot.register_next_step_handler(message, start_two);
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("согласен")
        btn2 = types.KeyboardButton("play")
        btn3 = types.KeyboardButton("wiki")
        markup.add(btn1, btn2, btn3)

        bot.send_message(message.from_user.id, 'я ничего не понял...\nНапиши, согласен ли ты знакомиться?\nНапиши "хорошо", "давай" или "ок".\nИли жми:\n/play, чтобы начать игру.\n/wiki, чтоб получать\nзначения слов из википедии.', reply_markup=markup);
        bot.register_next_step_handler(message, start_two)
#################################################################################################################################################################################################################
def get_name(message): #получаем фамилию
    global name;
    answer = message.text.lower()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("regy")
    btn2 = types.KeyboardButton("play")
    btn3 = types.KeyboardButton("wiki")
    markup.add(btn1, btn2, btn3) # специально поставил, чтоб не было прошлых кнопок

    if  answer in answer_NO_list1 or answer in answer_OutGame_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("start")
        btn2 = types.KeyboardButton("regy")
        btn3 = types.KeyboardButton("play")
        btn4 = types.KeyboardButton("wiki")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4) # специально поставил, чтоб не было прошлых кнопок

        bot.send_message(message.from_user.id, 'Тогда топай в начало.', reply_markup=markup);
        bot.register_next_step_handler(message, start);
    elif answer in Goodbye_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("start")
        btn2 = types.KeyboardButton("regy")
        btn3 = types.KeyboardButton("play")
        btn4 = types.KeyboardButton("wiki")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4) # специально поставил, чтоб не было прошлых кнопок

        bot.send_message(message.from_user.id, "До свидания, всего доброго тебе!", reply_markup=markup);
        bot.register_next_step_handler(message, start);
    elif answer in answer_pnh_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("start")
        btn2 = types.KeyboardButton("regy")
        btn3 = types.KeyboardButton("play")
        btn4 = types.KeyboardButton("wiki")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4) # специально поставил, чтоб не было прошлых кнопок

        bot.send_message(message.from_user.id, "Ты что, пёс?!\nТопай отсюда!", reply_markup=markup);
        bot.register_next_step_handler(message, start);
    elif answer == '/play' or answer in answer_GoGame_list:
        bot.send_message(message.from_user.id, 'Хороший выбор!\nПредлагаю поиграть в магический шар.\nя буду магическим шаром:\nзадай любой вопрос, а я дам ответ.', reply_markup=markup);
        bot.register_next_step_handler(message, get_game); #следующий шаг – функция get_game
#______________________________________________________википедия_____________________________________________________
    elif answer == '/startwiki' or answer == '/wiki' or answer == 'википедия' or answer == 'wiki' or answer == 'вики':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("out wiki")
        markup.add(btn1)

        bot.send_message(message.from_user.id, 'Понял. Перевожу на вики.\nОтправь мне любое слово, и я найду его значение на Wikipedia.\nЧтобы выйти, введи: [/stop, /hare, /out].', reply_markup=markup);
        bot.register_next_step_handler(message, handle2_text);
#______________________________________________________википедия_____________________________________________________
    elif answer == '/start' or answer == 'start' or answer == 'старт' or answer in Hello_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("play")
        btn2 = types.KeyboardButton("wiki")
        btn3 = types.KeyboardButton("да")
        btn4 = types.KeyboardButton("нет")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4)

        bot.send_message(message.from_user.id, text="Привет, {0.first_name}! я весёлый, тестовый бот \nДавай знакомиться [да/нет]?\nИли:\nЖми /play, чтобы начать игру\nЖми /wiki, чтоб получать статьи из википедии".format(message.from_user), reply_markup=markup);
        bot.register_next_step_handler(message, start_two); #следующий шаг – функция start_two
    elif answer =='/regy' or answer == "regy":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("да")
        btn2 = types.KeyboardButton("нет")
        markup.add(btn1, btn2)

        bot.send_message(message.from_user.id, 'Мы же и так знакомимся! Ладно, давай заново.', reply_markup=markup);
        bot.register_next_step_handler(message, start_two);
    else:
        name = message.text;
        bot.send_message(message.from_user.id, 'Какая у тебя фамилия?', reply_markup=markup);
        bot.register_next_step_handler(message, get_surname);
#################################################################################################################################################################################################################
def get_surname(message):
    global surname;
    answer = message.text.lower()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("regy")
    btn2 = types.KeyboardButton("play")
    btn3 = types.KeyboardButton("wiki")
    markup.add(btn1, btn2, btn3) # специально поставил, чтоб не было прошлых кнопок

    if  answer in answer_NO_list1 or answer in answer_OutGame_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("start")
        btn2 = types.KeyboardButton("regy")
        btn3 = types.KeyboardButton("play")
        btn4 = types.KeyboardButton("wiki")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4) # специально поставил, чтоб не было прошлых кнопок

        bot.send_message(message.from_user.id, 'Тогда топай в начало.', reply_markup=markup);
        bot.register_next_step_handler(message, start);
    elif answer in Goodbye_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("start")
        btn2 = types.KeyboardButton("regy")
        btn3 = types.KeyboardButton("play")
        btn4 = types.KeyboardButton("wiki")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4) # специально поставил, чтоб не было прошлых кнопок

        bot.send_message(message.from_user.id, "До свидания, всего доброго тебе!", reply_markup=markup);
        bot.register_next_step_handler(message, start);
    elif answer in answer_pnh_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("start")
        btn2 = types.KeyboardButton("regy")
        btn3 = types.KeyboardButton("play")
        btn4 = types.KeyboardButton("wiki")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4) # специально поставил, чтоб не было прошлых кнопок

        bot.send_message(message.from_user.id, "Ты что, пёс?!\nТопай отсюда!", reply_markup=markup);
        bot.register_next_step_handler(message, start);
    elif answer == '/play' or answer in answer_GoGame_list:
        bot.send_message(message.from_user.id, 'Хороший выбор!\nПредлагаю поиграть в магический шар.\nя буду магическим шаром:\nзадай любой вопрос, а я дам ответ.', reply_markup=markup);
        bot.register_next_step_handler(message, get_game); #следующий шаг – функция get_game
#______________________________________________________википедия_____________________________________________________
    elif answer == '/startwiki' or answer == '/wiki' or answer == 'википедия' or answer == 'wiki' or answer == 'вики':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("out wiki")
        markup.add(btn1)

        bot.send_message(message.from_user.id, 'Понял. Перевожу на вики.\nОтправь мне любое слово, и я найду его значение на Wikipedia.\nЧтобы выйти, введи: [/stop, /hare, /out].', reply_markup=markup);
        bot.register_next_step_handler(message, handle2_text);
#______________________________________________________википедия_____________________________________________________
    elif answer == '/start' or answer == 'start' or answer == 'старт' or answer in Hello_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("play")
        btn2 = types.KeyboardButton("wiki")
        btn3 = types.KeyboardButton("да")
        btn4 = types.KeyboardButton("нет")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4)

        bot.send_message(message.from_user.id, text="Привет, {0.first_name}! я весёлый, тестовый бот!\nДавай знакомиться [да/нет]?\nИли:\nЖми /play, чтобы начать игру.\nЖми /wiki, чтоб получать\nзначения слов из википедии.".format(message.from_user), reply_markup=markup);
        bot.register_next_step_handler(message, start_two); #следующий шаг – функция start_two
    elif answer =='/regy' or answer == "regy":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("да")
        btn2 = types.KeyboardButton("нет")
        markup.add(btn1, btn2)

        bot.send_message(message.from_user.id, 'Мы же и так знакомимся! Ладно, давай заново.', reply_markup=markup);
        bot.register_next_step_handler(message, start_two);
    else:
        surname = message.text;
        bot.send_message(message.from_user.id, 'Сколько тебе лет?\nНапиши пожалуйста цифрами, а то я могу зависнуть.', reply_markup=markup);
        bot.register_next_step_handler(message, get_age);
#################################################################################################################################################################################################################
def get_age(message):
    global age;
    answer = message.text.lower()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("regy")
    btn2 = types.KeyboardButton("play")
    btn3 = types.KeyboardButton("wiki")
    markup.add(btn1, btn2, btn3) # специально поставил, чтоб не было прошлых кнопок

    if message.text.isdigit():
        age = int(message.text)

        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes'); #кнопка «Да»
        keyboard.add(key_yes); #добавляем кнопку в клавиатуру
        key_no= types.InlineKeyboardButton(text='Нет', callback_data='no');
        keyboard.add(key_no);
        question = 'Тебе '+str(age)+' лет, тебя зовут '+name+' '+surname+'?';
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

        bot.register_next_step_handler(message, response_processing); #чтоб понять что дальше делать
    ###_______________________________________________________________________________________________________________
    elif  answer in answer_NO_list1 or answer in answer_OutGame_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("start")
        btn2 = types.KeyboardButton("regy")
        btn3 = types.KeyboardButton("play")
        btn4 = types.KeyboardButton("wiki")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4) # специально поставил, чтоб не было прошлых кнопок

        bot.send_message(message.from_user.id, 'Тогда топай в начало.', reply_markup=markup);
        bot.register_next_step_handler(message, start);
    elif answer in Goodbye_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("start")
        btn2 = types.KeyboardButton("regy")
        btn3 = types.KeyboardButton("play")
        btn4 = types.KeyboardButton("wiki")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4) # специально поставил, чтоб не было прошлых кнопок

        bot.send_message(message.from_user.id, "До свидания, всего доброго тебе!", reply_markup=markup);
        bot.register_next_step_handler(message, start);
    elif answer in answer_pnh_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("start")
        btn2 = types.KeyboardButton("regy")
        btn3 = types.KeyboardButton("play")
        btn4 = types.KeyboardButton("wiki")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4) # специально поставил, чтоб не было прошлых кнопок

        bot.send_message(message.from_user.id, "Ты что, пёс?!\nТопай отсюда!", reply_markup=markup);
        bot.register_next_step_handler(message, start);
    elif answer == '/play' or answer in answer_GoGame_list:
        bot.send_message(message.from_user.id, 'Хороший выбор!\nПредлагаю поиграть в магический шар.\nя буду магическим шаром:\nзадай любой вопрос, а я дам ответ.', reply_markup=markup);
        bot.register_next_step_handler(message, get_game); #следующий шаг – функция get_game
#______________________________________________________википедия_____________________________________________________
    elif answer == '/startwiki' or answer == '/wiki' or answer == 'википедия' or answer == 'wiki' or answer == 'вики':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("out wiki")
        markup.add(btn1)

        bot.send_message(message.from_user.id, 'Понял. Перевожу на вики.\nОтправь мне любое слово, и я найду его значение на Wikipedia.\nЧтобы выйти, введи: [/stop, /hare, /out].', reply_markup=markup);
        bot.register_next_step_handler(message, handle2_text);
#______________________________________________________википедия_____________________________________________________
    elif answer == '/start' or answer == 'start' or answer == 'старт' or answer in Hello_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("play")
        btn2 = types.KeyboardButton("wiki")
        btn3 = types.KeyboardButton("да")
        btn4 = types.KeyboardButton("нет")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4)

        bot.send_message(message.from_user.id, text="Привет, {0.first_name}! я весёлый, тестовый бот!\nДавай знакомиться [да/нет]?\nИли:\nЖми /play, чтобы начать игру.\nЖми /wiki, чтоб получать\nзначения слов из википедии.".format(message.from_user), reply_markup=markup);
        bot.register_next_step_handler(message, start_two); #следующий шаг – функция start_two
    elif answer =='/regy' or answer == "regy":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("да")
        btn2 = types.KeyboardButton("нет")
        markup.add(btn1, btn2)

        bot.send_message(message.from_user.id, 'Мы же и так знакомимся! Ладно, давай заново.', reply_markup=markup);
        bot.register_next_step_handler(message, start_two);
    else:
        bot.send_message(message.from_user.id, 'Неверный ввод. Напиши цифрами пожалуйста.', reply_markup=markup)
        bot.register_next_step_handler(message, get_age)
#################################################################################################################################################################################################################
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
        bot.send_message(call.message.chat.id, 'Запомню!\nЧто будешь делать дальше? :)\nХочешь изменить данные, жми /regy.\nХочешь поиграть, жми /play.\nХочешь почитать википедию, жми /wiki.');
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Ты же сам мне всё это написал.\nХочешь изменить данные, жми /regy.\nХочешь поиграть, жми /play.\nХочешь почитать википедию, жми /wiki.');
#################################################################################################################################################################################################################
def response_processing(message):
    answer = message.text.lower();
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("regy")
    btn2 = types.KeyboardButton("play")
    btn3 = types.KeyboardButton("wiki")
    markup.add(btn1, btn2, btn3) # специально поставил, чтоб не было прошлых кнопок

    if message.text=='/regy' or answer == "regy" :
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("да")
        btn2 = types.KeyboardButton("нет")
        markup.add(btn1, btn2)

        bot.send_message(message.from_user.id, 'Начнём знакомство сначала? Да?', reply_markup=markup);
        bot.register_next_step_handler(message, start_two);
    elif answer == '/start' or answer == 'start' or answer == 'старт' or answer in Hello_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("play")
        btn2 = types.KeyboardButton("wiki")
        btn3 = types.KeyboardButton("да")
        btn4 = types.KeyboardButton("нет")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4)

        bot.send_message(message.from_user.id, text="Привет, {0.first_name}! я весёлый, тестовый бот!\nДавай знакомиться [да/нет]?\nИли:\nЖми /play, чтобы начать игру.\nЖми /wiki, чтоб получать\nзначения слов из википедии.".format(message.from_user), reply_markup=markup);
        bot.register_next_step_handler(message, start_two); #следующий шаг – функция start_two
    elif  answer in answer_NO_list1 or answer in answer_OutGame_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("start")
        btn2 = types.KeyboardButton("regy")
        btn3 = types.KeyboardButton("play")
        btn4 = types.KeyboardButton("wiki")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4) # специально поставил, чтоб не было прошлых кнопок

        bot.send_message(message.from_user.id, 'Хорошо, возвращайся в начало.\nНапиши что-нибудь, чтоб запустить бота :)', reply_markup=markup);
        bot.register_next_step_handler(message, start);
    elif answer in Goodbye_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("start")
        btn2 = types.KeyboardButton("regy")
        btn3 = types.KeyboardButton("play")
        btn4 = types.KeyboardButton("wiki")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4) # специально поставил, чтоб не было прошлых кнопок

        bot.send_message(message.from_user.id, "До свидания, всего доброго тебе!", reply_markup=markup);
        bot.register_next_step_handler(message, start);
    elif answer in answer_pnh_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("start")
        btn2 = types.KeyboardButton("regy")
        btn3 = types.KeyboardButton("play")
        btn4 = types.KeyboardButton("wiki")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4) # специально поставил, чтоб не было прошлых кнопок

        bot.send_message(message.from_user.id, "Ты что пёс?!\nТопай отсюда!", reply_markup=markup);
        bot.register_next_step_handler(message, start);
    elif message.text == '/play' or answer in answer_GoGame_list:
        bot.send_message(message.from_user.id, 'Хороший выбор!\nПредлагаю поиграть в магический шар.\nя буду магическим шаром:\nзадай любой вопрос, а я дам ответ.', reply_markup=markup);
        bot.register_next_step_handler(message, get_game); #следующий шаг – функция get_game
#______________________________________________________википедия_____________________________________________________
    elif answer == '/startwiki' or answer == '/wiki' or answer == 'википедия' or answer == 'wiki' or answer == 'вики':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("out wiki")
        markup.add(btn1)

        bot.send_message(message.from_user.id, 'Понял. Перевожу на вики.\nОтправь мне любое слово, и я найду его значение на Wikipedia.\nЧтобы выйти, введи: [/stop, /hare, /out].', reply_markup=markup);
        bot.register_next_step_handler(message, handle2_text);
#______________________________________________________википедия_____________________________________________________
    else:
        bot.send_message(message.from_user.id, 'Ммм, я ничего не понял,\nвыбери, что будешь делать:\nХочешь изменить данные, жми /regy\nХочешь поиграть, жми /play\nХочешь почитать википедию, жми /wiki', reply_markup=markup);
        bot.register_next_step_handler(message, response_processing);
#################################################################################################################################################################################################################
def get_game(message):
    answer = message.text.lower();
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("regy")
    btn2 = types.KeyboardButton("play")
    btn3 = types.KeyboardButton("wiki")
    markup.add(btn1, btn2, btn3) # специально поставил, чтоб не было прошлых кнопок

    if answer in answer_OutGame_list or answer in answer_NO_list1:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("start")
        btn2 = types.KeyboardButton("regy")
        btn3 = types.KeyboardButton("play")
        btn4 = types.KeyboardButton("wiki")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4) # специально поставил, чтоб не было прошлых кнопок

        bot.send_message(message.from_user.id, 'Ну ладно, возвращайся в начало.', reply_markup=markup);
        bot.register_next_step_handler(message, start);
    elif answer in Goodbye_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("start")
        btn2 = types.KeyboardButton("regy")
        btn3 = types.KeyboardButton("play")
        btn4 = types.KeyboardButton("wiki")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4) # специально поставил, чтоб не было прошлых кнопок

        bot.send_message(message.from_user.id, "До свидания, всего доброго тебе!", reply_markup=markup);
        bot.register_next_step_handler(message, start);
    elif answer in answer_pnh_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("start")
        btn2 = types.KeyboardButton("regy")
        btn3 = types.KeyboardButton("play")
        btn4 = types.KeyboardButton("wiki")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4) # специально поставил, чтоб не было прошлых кнопок

        bot.send_message(message.from_user.id, "Ты что пёс?!\nТопай отсюда!", reply_markup=markup);
        bot.register_next_step_handler(message, start);
    elif message.text == '/play' or answer in answer_GoGame_list:
        bot.send_message(message.from_user.id, 'Ты же и так в игре!\nЗадай мне любой вопрос, а я дам ответ.', reply_markup=markup);
        bot.register_next_step_handler(message, get_game); #следующий шаг – функция get_game
#______________________________________________________википедия_____________________________________________________
    elif answer == '/startwiki' or answer == '/wiki' or answer == 'википедия' or answer == 'wiki' or answer == 'вики':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("out wiki")
        markup.add(btn1)

        bot.send_message(message.from_user.id, 'Понял. Перевожу на вики.\nОтправь мне любое слово, и я найду его значение на Wikipedia.\nЧтобы выйти, введи: [/stop, /hare, /out].', reply_markup=markup);
        bot.register_next_step_handler(message, handle2_text);
#______________________________________________________википедия_____________________________________________________
    elif answer == '/start' or answer == 'start' or answer == 'старт' or answer in Hello_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("play")
        btn2 = types.KeyboardButton("wiki")
        btn3 = types.KeyboardButton("да")
        btn4 = types.KeyboardButton("нет")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4)

        bot.send_message(message.from_user.id, text="Привет, {0.first_name}! я весёлый, тестовый бот!\nДавай знакомиться [да/нет]?\nИли:\nЖми /play, чтобы начать игру.\nЖми /wiki, чтоб получать\nзначения слов из википедии.".format(message.from_user), reply_markup=markup);
        bot.register_next_step_handler(message, start_two); #следующий шаг – функция start_two
    elif answer =='/regy' or answer == "regy":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("да")
        btn2 = types.KeyboardButton("нет")
        markup.add(btn1, btn2)

        bot.send_message(message.from_user.id, 'Начнем знакомство сначала? Да?', reply_markup=markup);
        bot.register_next_step_handler(message, start_two);
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("да")
        btn2 = types.KeyboardButton("нет")
        markup.add(btn1, btn2)

        bot.send_message(message.from_user.id, random.choice(answer_magic_ball) + "\nБудут ещё вопросы?", reply_markup=markup);
        bot.register_next_step_handler(message, continue_game);
#################################################################################################################################################################################################################
def continue_game(message):
    answer = message.text.lower();
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("regy")
    btn2 = types.KeyboardButton("play")
    btn3 = types.KeyboardButton("wiki")
    markup.add(btn1, btn2, btn3) # специально поставил, чтоб не было прошлых кнопок

    if answer in answer_YES_list1 or answer in answer_YES_list2:
        bot.send_message(message.from_user.id, 'Хорошо :)\nПиши свой вопрос.', reply_markup=markup);
        bot.register_next_step_handler(message, get_game);
    elif answer in answer_NO_list1 or answer in answer_NO_list2 or answer in answer_OutGame_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("start")
        btn2 = types.KeyboardButton("regy")
        btn3 = types.KeyboardButton("play")
        btn4 = types.KeyboardButton("wiki")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4) # специально поставил, чтоб не было прошлых кнопок

        bot.send_message(message.from_user.id, 'Тогда топай в начало.', reply_markup=markup);
        bot.register_next_step_handler(message, start);
    elif answer in Goodbye_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("start")
        btn2 = types.KeyboardButton("regy")
        btn3 = types.KeyboardButton("play")
        btn4 = types.KeyboardButton("wiki")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4) # специально поставил, чтоб не было прошлых кнопок

        bot.send_message(message.from_user.id, "До свидания, всего доброго тебе!", reply_markup=markup);
        bot.register_next_step_handler(message, start);
    elif answer in answer_pnh_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("start")
        btn2 = types.KeyboardButton("regy")
        btn3 = types.KeyboardButton("play")
        btn4 = types.KeyboardButton("wiki")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4) # специально поставил, чтоб не было прошлых кнопок

        bot.send_message(message.from_user.id, "Ты что пёс?!\nТопай отсюда!", reply_markup=markup);
        bot.register_next_step_handler(message, start);
    elif message.text == '/play' or answer in answer_GoGame_list:
        bot.send_message(message.from_user.id, 'Ты же и так в игре!\nЗадай мне любой вопрос, а я дам ответ.', reply_markup=markup);
        bot.register_next_step_handler(message, get_game); #следующий шаг – функция get_game
#______________________________________________________википедия_____________________________________________________
    elif answer == '/startwiki' or answer == '/wiki' or answer == 'википедия' or answer == 'wiki' or answer == 'вики':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("out wiki")
        markup.add(btn1)

        bot.send_message(message.from_user.id, 'Понял. Перевожу на вики.\nОтправь мне любое слово, и я найду его значение на Wikipedia.\nЧтобы выйти, введи: [/stop, /hare, /out].', reply_markup=markup);
        bot.register_next_step_handler(message, handle2_text);
#______________________________________________________википедия_____________________________________________________
    elif answer == '/start' or answer == 'start' or answer == 'старт' or answer in Hello_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("play")
        btn2 = types.KeyboardButton("wiki")
        btn3 = types.KeyboardButton("да")
        btn4 = types.KeyboardButton("нет")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4)

        bot.send_message(message.from_user.id, text="Привет, {0.first_name}! я весёлый, тестовый бот!\nДавай знакомиться [да/нет]?\nИли:\nЖми /play, чтобы начать игру.\nЖми /wiki, чтоб получать\nзначения слов из википедии.".format(message.from_user), reply_markup=markup);
        bot.register_next_step_handler(message, start_two); #следующий шаг – функция start_two
    elif answer =='/regy' or answer == "regy":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("да")
        btn2 = types.KeyboardButton("нет")
        markup.add(btn1, btn2)

        bot.send_message(message.from_user.id, 'Начнем знакомство сначала? Да?', reply_markup=markup);
        bot.register_next_step_handler(message, start_two);
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("да")
        btn2 = types.KeyboardButton("нет")
        markup.add(btn1, btn2)

        bot.send_message(message.from_user.id, 'Ммм, я ничего не понял, ответь внятно\nБудут ещё вопросы [да/нет]?', reply_markup=markup);
        bot.register_next_step_handler(message, continue_game);

#______________________________________________________википедия_____________________________________________________
wikipedia.set_lang("ru") # Устанавливаем русский язык в Wikipedia

def getwiki(s): # Чистим текст статьи в Wikipedia и ограничиваем его тысячей символов
    try:
        ny = wikipedia.page(s)
        # Получаем первую тысячу символов
        wikitext=ny.content[:1000]
        # Разделяем по точкам
        wikimas=wikitext.split('.')
        # Отбрасываем всЕ после последней точки
        wikimas = wikimas[:-1]
        # Создаем пустую переменную для текста
        wikitext2 = ''
        # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
        for x in wikimas:
            if not('==' in x):
                    # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные при разделении строк точки на место
                if(len((x.strip()))>3):
                    wikitext2=wikitext2+x+'.'
            else:
                break
        # Теперь при помощи регулярных выражений убираем разметку
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
        # Возвращаем текстовую строку
        return wikitext2
    # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
    except Exception as e:
        return 'В энциклопедии нет информации об этом'
#################################################################################################################################################################################################################
def handle2_text(message):
    answer = message.text.lower()
    if answer in stop_list or answer == "out wiki" or answer == "/stop" or answer == "/hare" or answer == "/out" or answer in answer_NO_list1 or answer in answer_OutGame_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("start")
        btn2 = types.KeyboardButton("regy")
        btn3 = types.KeyboardButton("play")
        btn4 = types.KeyboardButton("wiki")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4) # специально поставил, чтоб не было прошлых кнопок

        bot.send_message(message.chat.id, "Это слово для выхода из вики, отправляю в начало.", reply_markup=markup)
        bot.register_next_step_handler(message, start)
    elif answer in answer_pnh_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("start")
        btn2 = types.KeyboardButton("regy")
        btn3 = types.KeyboardButton("play")
        btn4 = types.KeyboardButton("wiki")
        markup.add(btn1, btn2)
        markup.add(btn3, btn4) # специально поставил, чтоб не было прошлых кнопок

        bot.send_message(message.from_user.id, "Ты что пёс?!\nТопай отсюда!", reply_markup=markup);
        bot.register_next_step_handler(message, start);
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("out wiki")
        markup.add(btn1)

        bot.send_message(message.chat.id, getwiki(message.text), reply_markup=markup)
        bot.register_next_step_handler(message, handle2_text);
#______________________________________________________википедия_____________________________________________________

bot.polling(none_stop=True, interval=0)