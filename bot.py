import telebot
from telebot import types
import scenarios.homework

bot = telebot.TeleBot("1422565102:AAERHvM0_GEG4IK7RWn-TdJ1AYmcFwy8Ahg")


# User control
from Group import Group
from Role import Role
from User import User
from db import has_user, get_user, create_user, get_group

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	chat_id = message.chat.id
	chat = message.chat
	bot.send_message(chat_id, 'Nice to meet you ' + '\n' + str(chat.username))
	bot.send_message(chat_id, 'Current ID of the chat is ' + str(chat_id))
	if has_user(chat_id):
		user = get_user(chat_id)
		user_groups = user.group_list
		markup = types.ReplyKeyboardMarkup()
		for group, _roles in user_groups:
			group_name = types.KeyboardButton(group.name)
			markup.row(group_name)
		msg = bot.send_message(chat_id, 'Выберите группу: ' + '\n', reply_markup=markup)
		bot.register_next_step_handler(msg, select_group)

def select_group(message):
	user = get_user(chat_id)
	user_groups = user.group_list
	current_group_name = message.text
	for group, roles in user_groups:
		if current_group_name == group.name:
			current_roles = roles
			break
	else:
		raise Exception("no group")

	markup = types.ReplyKeyboardMarkup() 


	if Role.ADMIN in roles:
		itembtna = types.KeyboardButton(homework_download)
		itembtnv = types.KeyboardButton(grades_student)
		itembtnc = types.KeyboardButton(deadlines_watch)

		markup.row(itembtna)
		markup.row(itembtnv)
		markup.row(itembtnc)
	
	if Role.TEACHER in roles:
		itembtna = types.KeyboardButton(homework_add, callback_data="add homework")
		itembtnv = types.KeyboardButton(grades_teacher, callback_data="add grades")
		itembtnc = types.KeyboardButton(exel_download, callback_data="download excel")

		markup.row(itembtna)
		markup.row(itembtnv)
		markup.row(itembtnc)

	if Role.STUDENT in roles:
		itembtna = types.KeyboardButton(homework_download)
		itembtnv = types.KeyboardButton(grades_student)
		itembtnc = types.KeyboardButton(deadlines_watch)

		markup.row(itembtna)
		markup.row(itembtnv)
		markup.row(itembtnc)

	msg = bot.send_message(chat_id, ' ', reply_markup=markup)
	








# options functions
# 
homework_add = 'Добавить домашнее задание'
grades_teacher = 'Выставить оценки'
exel_download = 'Скачать exel-таблицу'

homework_download = "Загрузить дз"
grades_student = "Посмотреть баллы"
deadlines_watch = "Посмотреть дедлайны"


# @bot.message_handler(commands=['teacher'])
# def teacher_start(message):
# 	chat_id = message.chat.id
# 	markup = types.ReplyKeyboardMarkup() 
# 	itembtna = types.KeyboardButton(homework_add)
# 	itembtnv = types.KeyboardButton(grades_teacher)
# 	itembtnc = types.KeyboardButton(exel_download)

# 	markup.row(itembtna)
# 	markup.row(itembtnv)
# 	markup.row(itembtnc)
# 	msg = bot.send_message(chat_id, 'Your current options: ' + '\n', reply_markup=markup)
# 	bot.register_next_step_handler(msg, teacher_next)



# Student options functions
#
homework_download = "Загрузить дз"
grades_student = "Посмотреть баллы"
deadlines_watch = "Посмотреть дедлайны"

@bot.message_handler(commands=['student'])
def student_start(message):
	chat_id = message.chat.id
	markup = types.ReplyKeyboardMarkup() 
	itembtna = types.KeyboardButton(homework_download)
	itembtnv = types.KeyboardButton(grades_student)
	itembtnc = types.KeyboardButton(deadlines_watch)

	markup.row(itembtna)
	markup.row(itembtnv)
	markup.row(itembtnc)
	msg = bot.send_message(chat_id, 'Your current options: ' + '\n', reply_markup=markup)
	bot.register_next_step_handler(msg, student_next)


def student_next(message):
	chat_id = message.chat.id
	option = message.text
	if (option == homework_download):
		msg = bot.send_message(chat_id, "Скачать дз функция" + '\n')
		bot.register_next_step_handler(msg, homework_next)

	elif (option == grades_student):
		msg = bot.send_message(chat_id, "Оценки студент функция" + '\n')

	elif (option == deadlines_watch):
		msg = bot.send_message(chat_id, "дедлайны ученик функция")
	else:
		return











# Message is not a command
@bot.message_handler(func=lambda message: True)
def echo_all(message):
	markup = types.ReplyKeyboardRemove(selective=False)
	bot.reply_to(message, "Пожалуйста, снова введите команду", reply_markup=markup) # Remove markup


bot.polling()
