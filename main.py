import telebot
from telebot import types

bot = telebot.TeleBot("6005042268:AAHVSyA5XqyMWOdzITWs8Ppbh3hRmsS6oSw")
storage = {}


class UserInteration:
    def __init__(self, action):
        self.action = action
        self.first_number = None
        self.second_number = None


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    butl1 = types.KeyboardButton("Сложить")
    butl2 = types.KeyboardButton("Вычесть")
    butl3 = types.KeyboardButton("Умножить")
    butl4 = types.KeyboardButton("Разделить")
    butl5 = types.KeyboardButton("Возвести в степень")
    markup.add(butl1)
    markup.add(butl2)
    markup.add(butl3)
    markup.add(butl4)
    markup.add(butl5)
    bot.send_message(message.chat.id, "Выбери ниже", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def controller(message):
    print(message.text)
    if message.text in ["Сложить", "Вычесть", "Умножить", "Разделить", "Возвести в степень"]:
        storage[message.chat.id] = UserInteration(message.text)
        get_inputs_from_user(message)


def get_inputs_from_user(message):
    bot.send_message(message.chat.id, 'Введите первое число', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, input_first_number)


def input_first_number(message):
    chat_id = message.chat.id
    first_number = message.text
    if not first_number.isdigit():
        msg = bot.reply_to(message, 'Должно быть число!')
        bot.register_next_step_handler(msg, input_first_number)
        return

    interaction = storage[chat_id]
    interaction.first_number = int(first_number)

    bot.send_message(message.chat.id, 'Введите второе число')
    bot.register_next_step_handler(message, input_second_number)


def input_second_number(message):
    chat_id = message.chat.id
    second_number = message.text
    interaction = storage[chat_id]

    if not second_number.isdigit():
        msg = bot.reply_to(message, 'Должно быть число!')
        bot.register_next_step_handler(msg, input_second_number)
        return

    if interaction.action == "Разделить":
        msg = bot.reply_to(message, 'Нельзя делить на 0!')
        bot.register_next_step_handler(msg, input_second_number)
        return

    interaction.second_number = int(second_number)

    calc(message.chat.id, interaction)


def calc(chat_id, interaction):
    print(chat_id)
    print(interaction)
    a = interaction.first_number
    b = interaction.second_number
    result = ''
    if interaction.action == "Сложить":
        result = a + b
    elif interaction.action == "Вычесть":
        result = a - b
    elif interaction.action == "Умножить":
        result = a * b
    elif interaction.action == "Разделить":
        result = a / b
    elif interaction.action == "Возвести в степень":
        result = a ** b

    bot.send_message(chat_id, result)


bot.infinity_polling()
