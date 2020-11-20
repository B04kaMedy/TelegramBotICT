import telebot
from telebot import types

bot = telebot.TeleBot("1422565102:AAERHvM0_GEG4IK7RWn-TdJ1AYmcFwy8Ahg")


# User control
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	chat_id = message.chat.id
	chat = message.chat
	bot.send_message(chat_id, 'Nice to meet you ' + '\n' + str(chat.username))
	bot.send_message(chat_id, 'Current ID of the chat is ' + str(chat_id))


# Teacher options functions
homework_add = 'Добавить домашнее задание'
grades = 'Выставить оценки'
exel_download = 'Скачать exel-таблицу'

@bot.message_handler(commands=['teacher'])
def teacher_options(message):
	chat_id = message.chat.id
	markup = types.ReplyKeyboardMarkup() 
	itembtna = types.KeyboardButton(homework_add)
	itembtnv = types.KeyboardButton(grades)
	itembtnc = types.KeyboardButton(exel_download)

	markup.row(itembtna)
	markup.row(itembtnv)
	markup.row(itembtnc)
	msg = bot.send_message(chat_id, 'Your current options: ' + '\n', reply_markup=markup)
	bot.register_next_step_handler(msg, option_next)
	pass



# Main teacher options
homework_new = 'Добавить новое дз'
homework_edit = 'Редактировать дз'

def option_next(message):
	chat_id = message.chat.id
	option = message.text
	if (option == homework_add):
		markup = types.ReplyKeyboardMarkup()
		itembtna = types.KeyboardButton(homework_new)
		itembtnv = types.KeyboardButton(homework_edit)
		markup.row(itembtna)
		markup.row(itembtnv)
		msg = bot.send_message(chat_id, "Choose next option" + '\n', reply_markup=markup)
		bot.register_next_step_handler(msg, homework_next)

	elif (option == grades):
		msg = bot.send_message(chat_id, "Выберите ученика" + '\n')
		bot.register_next_step_handler(msg, grades_next)

	elif (option == exel_download):
		msg = bot.send_message(chat_id, "скачиваю...")
		bot.register_next_step_handler(msg, exel_download_next)
	else:
		return


def homework_next(message):
	markup = types.ReplyKeyboardRemove(selective=False)

	bot.reply_to(message, "f", reply_markup=markup)   # Remove markup


def grades_next(message):
	markup = types.ReplyKeyboardRemove(selective=False)
	
	bot.reply_to(message, "f", reply_markup=markup)  


def exel_download_next(message):
	markup = types.ReplyKeyboardRemove(selective=False)

	bot.reply_to(message, "f", reply_markup=markup)




# Message is not a command
@bot.message_handler(func=lambda message: True)
def echo_all(message):
	markup = types.ReplyKeyboardRemove(selective=False)
	bot.reply_to(message, "Sorry, I don't speek that language", reply_markup=markup) # Remove markup
	pass

bot.polling()
