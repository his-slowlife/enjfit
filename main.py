import telebot

from telebot import types

# bot = telebot.TeleBot('1216448489:AAGa0aixNFa6R9AvpuYF0wkTTlTOauHKYzg') # Sergei's token
# bot = telebot.TeleBot('1281817942:AAE24DX-h9ZunkdS4ZGJvSfxUY5rdqzwdgI') # Oleh's token
bot = telebot.TeleBot('1216448489:AAGa0aixNFa6R9AvpuYF0wkTTlTOauHKYzg')

KEYBOARDS = {
  'main': [
    types.KeyboardButton("Чек-лист ✅"),
    types.KeyboardButton("Тренировки 🎯")
  ],
  'trainings': [
    types.KeyboardButton("Программа тренировок"),
    types.KeyboardButton("Персональное ведение"),
    types.KeyboardButton("Вернуться в главное меню")
  ]
}

def initialize_keyboard(k):
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  # print(KEYBOARDS['main'])
  markup.add(*KEYBOARDS[k])
  return markup

@bot.message_handler(commands=['help'])
def about(message):
  bot.send_message(message.chat.id, "Я классный, пока это все, что нужно знать;)")

@bot.message_handler(commands=['start'])
def welcome(message):
  sti = open('hello.webp', 'rb')
  bot.send_sticker(message.chat.id, sti)
  # main keyboard
  markup = initialize_keyboard('main')
  bot.send_message(message.chat.id, "Привет, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот-помощник Даши".format(message.from_user, bot.get_me()),
        parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text', 'document'])
def ask_bot(message):
  if message.chat.type == 'private':
    if message.text == 'Чек-лист ✅':
      doc = open('check.pdf', 'rb')
      bot.send_document(message.chat.id, doc)
    elif message.text == 'Тренировки 🎯':
      # trainings
      markup = initialize_keyboard('trainings')
      bot.send_message(message.chat.id, "Выбери опцию", parse_mode='html', reply_markup=markup)
    elif message.text == 'Программа тренировок':
      bot.send_message(message.chat.id, "Составление программы тренировок + визуальная диагностика от Даши стоит 1200р")
    elif message.text == 'Персональное ведение':
      bot.send_message(message.chat.id, "Полноценное ведение с разбором твоих тренировок будет стоить 3000р. А еще напиши боту - питание, чтобы узнать о специальном предложении 😉")
    elif message.text == 'Вернуться в главное меню':
       markup = initialize_keyboard('main')
       bot.send_message(
         message.chat.id, 
         "Главное меню",
         parse_mode='html', 
         reply_markup=markup
        )
    elif message.text.lower() == 'питание':   
       markup = types.InlineKeyboardMarkup(row_width=2)
       item1 = types.InlineKeyboardButton("Да, я за пп", callback_data='yes')
       item2 = types.InlineKeyboardButton("Нет", callback_data='no')
       markup.add(item1, item2)
       bot.send_message(message.chat.id, "Добавим питание?",reply_markup=markup)
    else:
      bot.send_message(message.chat.id, "Я умею отвечать только на запросы под кнопками:)")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'yes':
                bot.send_message(call.message.chat.id, "Тогда напиши Кристине, она нутрициолог и с радостью составит для тебя план питания")
            elif call.data == 'no':
                bot.send_message(call.message.chat.id, "Хорошо, надеюсь, ты уже кушаешь правильно:)")

                # remove inline buttons
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Питание",
                                      reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                          text="У тебя все получится!")

    except Exception as e:
        print(repr(e))
#RUN
bot.polling(none_stop=True)