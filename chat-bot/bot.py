import telebot
from telebot import types

bot = telebot.TeleBot('6977588177:AAGVX2mcTagDMAhj-6OEBhRXSBiHZP-bdSw')
shops=[]
with open('fonts/shop_list.txt', 'r') as f:
    shops = f.readlines()

@bot.message_handler(commands=['start'])
def start(message):
    btns = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btns.add(types.KeyboardButton('Конечно!'), types.KeyboardButton('Пожалуй, воздержусь...'))
    bot.send_message(message.from_user.id, "Пссс... Хочешь сладких апельсинов? Хочешь...?", reply_markup=btns)
    
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text == 'Конечно!':
        btns = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btns.add(types.KeyboardButton('Угу.'), types.KeyboardButton('Нет.'))
        bot.send_message(message.from_user.id, "А дома они вообще есть?", reply_markup=btns)
        bot.register_next_step_handler(message, second_question)
        
        
    elif message.text == 'Пожалуй, воздержусь...':
        bot.send_message(message.from_user.id, "А. Ну на 'нет' - и суда нет")
        return
        
    elif message.text != 'Конечно!' 'Пожалуй, воздержусь...':
        bot.send_message(message.from_user.id, "Та-та-та, что я у тебя спрашиваю, и что ты отвечаешь.")
        return
        
def second_question(message):
    if message.text == 'Угу.':
        a = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, "А, ну так чего ждем? Вперед к апельсинам!", reply_markup=a)
        return
    
    elif message.text == 'Нет.': 
        bot.send_message(message.from_user.id, "Черт, грустно.")
        bot.send_message(message.from_user.id, "Ну... Пошли тогда в магазин.")
        bot.send_message(message.from_user.id, "Вот тебе адресса:")
        
        for i in range(len(shops)):
            bot.send_message(message.from_user.id, shops[i])
            
        btns = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btns.add(types.KeyboardButton('В первый'), types.KeyboardButton('Во второй'), types.KeyboardButton('В третий'))
        bot.send_message(message.from_user.id, "В какой пойдем первым?", reply_markup=btns)
        bot.register_next_step_handler(message, shop_list)
        
def shop_list(message):
    if message.text == "В первый" and len(shops) == 3:
        shops.pop(0)
        bot.register_next_step_handler(message, submit)
        
    elif message.text == "В первый" and len(shops) <= 2:
        bot.send_message(message.from_user.id, "Мы тут уже были.")
        
    elif message.text == 'Во второй':
        shops.pop(1)
        bot.register_next_step_handler(message, submit)
        
    elif message.text == 'В третий':
        shops.pop(2)
        bot.register_next_step_handler(message, submit)
        
    elif message.text == 'В магазин А':
        shops.pop(0)
        bot.register_next_step_handler(message, submit)
    elif message.text == 'В магазин Б':
        shops.pop(1)
        bot.register_next_step_handler(message, submit)
    elif len(shops) == 1:
        shops.pop(0)
        bot.register_next_step_handler(message, last_submit)
        
def submit(message):
    btns = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btns.add(types.KeyboardButton('Да.'), types.KeyboardButton('Нет.'))
    bot.send_message(message.from_user.id, "Ну что, здесь есть нужные нам апельсины?", reply_markup=btns)
    bot.register_next_step_handler(message, select_2)

def last_submit(message):
    bot.send_message(message.from_user.id, "Последний шанс.")
    btns = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btns.add(types.KeyboardButton('Да.'), types.KeyboardButton('Нет.'))
    bot.send_message(message.from_user.id, "Ну что, здесь есть нужные нам апельсины?", reply_markup=btns)
    bot.register_next_step_handler(message, last_select)
    
def last_select(message):
    if message.text == "Да.":
        a = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, "Покупаем!", reply_markup=a)
        
    elif message.text == "Нет.":
        a = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, "Ну, сорян, на этом мои полномочия все.", reply_markup=a)

    
def select_2(message):   
    if message.text == "Да.":
        a = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, "Покупаем!", reply_markup=a)
        return
        
    elif message.text == "Нет.":
        bot.register_next_step_handler(message, select_1)


def select_1(message):
    a = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, "Пошли дальше искать.", reply_markup=a)
    bot.send_message(message.from_user.id, "Вот тебе адресса:")
        
    for i in range(len(shops)):
        bot.send_message(message.from_user.id, shops[i])

    if len(shops) == 2:
        btns = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btns.add(types.KeyboardButton('В магазин А'), types.KeyboardButton('В магазин Б'))
        bot.send_message(message.from_user.id, "Куда теперь?", reply_markup=btns)
        bot.register_next_step_handler(message, shop_list)
    elif len(shops) == 1:
        btns = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btns.add(types.KeyboardButton('В последний магазин'))
        bot.send_message(message.from_user.id, "Куда теперь?", reply_markup=btns)
        bot.register_next_step_handler(message, shop_list)
    

bot.enable_save_next_step_handlers(delay=3)
bot.load_next_step_handlers()    
bot.polling()