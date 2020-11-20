from bot import bot
from telebot import types


homework_new = 'Добавить новое дз'
homework_edit = 'Редактировать дз'

@bot.callback_query_handler(func=lambda call: call.data == "add homework")
def add_homework(message):
	chat_id = message.chat.id
	markup = types.ReplyKeyboardMarkup()
	itembtna = types.KeyboardButton(homework_new, callback_data="new homework")
	itembtnv = types.KeyboardButton(homework_edit, callback_data="edit homework")
	markup.row(itembtna)
	markup.row(itembtnv)
	msg = bot.send_message(chat_id, 'Редактировать/Добавить', reply_markup=markup) 