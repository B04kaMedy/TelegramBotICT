import db
import telebot
from filters import everything

bot = telebot.TeleBot("1422565102:AAERHvM0_GEG4IK7RWn-TdJ1AYmcFwy8Ahg")

from telebot import apihelper
apihelper.ENABLE_MIDDLEWARE = True

from scenarios import register
from scenarios.groups import create as create_group
from scenarios.groups import set_current as set_current_group
from scenarios.admin import invite, remove
from scenarios.homework import add, check, delete, download, push, get_marks

@bot.message_handler(func=everything)
def wrong_message(msg):
	bot.reply_to(msg, "Вы кажеца ашиблись")
