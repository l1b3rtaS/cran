from datetime import timedelta, datetime
from random import randint
from telebot import types
from config import *
import telebot
import shutil
import os
bot = telebot.TeleBot(bnbtoken) 

bnbbot = telebot.TeleBot(bnbtoken) 
bnb_username = bnbbot.get_me().username
trxbot = telebot.TeleBot(trxtoken) 
trx_username = trxbot.get_me().username
btcbot = telebot.TeleBot(btctoken) 
btc_username = btcbot.get_me().username


@bot.message_handler(func=lambda message: True)
def reply_to_user(message):
	user_id = message.from_user.id
	if not os.path.exists(f"users/{user_id}"):
		os.mkdir(f"users/{user_id}")
		file = open(f"users/{user_id}/bnb_balance.txt", "w" , encoding="utf-8")
		file.write("0")
		file.close()
		file = open(f"users/{user_id}/trx_balance.txt", "w" , encoding="utf-8")
		file.write("0")
		file.close()
		file = open(f"users/{user_id}/btc_balance.txt", "w" , encoding="utf-8")
		file.write("0")
		file.close()

		# Получаем текущую дату и время
		current_datetime = datetime.now()

		# Вычитаем 2 часа
		new_datetime = current_datetime - timedelta(hours=2)

		# Преобразуем время в строку
		formatted_datetime = new_datetime.strftime("%Y-%m-%d %H:%M:%S")
		print(formatted_datetime)

		file = open(f"users/{user_id}/bnb_last.txt", "w" , encoding="utf-8")
		file.write(formatted_datetime)
		file.close()
		file = open(f"users/{user_id}/trx_last.txt", "w" , encoding="utf-8")
		file.write(formatted_datetime)
		file.close()
		file = open(f"users/{user_id}/btc_last.txt", "w" , encoding="utf-8")
		file.write(formatted_datetime)
		file.close()



	if message.text == "/start":
		rkey = types.ReplyKeyboardMarkup(True, True)
		rkey.row('👛 Кошелек', '🉑 BNB')
		rkey.row('📙 Информация')
		bot.send_message(message.chat.id, f"🐳 Приветствую тебя в BNB кране! 🚀 \n\n- Получай BNB каждый час\n- Бот НЕ требует вложений\n- Вывод осуществляется в течении 24 часов\n\nКран BNB - @{bnb_username}\nКран TRX - @{trx_username}\nКран BTC - @{btc_username}", reply_markup=rkey, parse_mode="HTML")
	if message.text == "📙 Информация":
		users = len(os.listdir(f"users"))
		users = users + 620100

		with open('start_date.txt', 'r') as file:
		    date_str = file.read().strip()
		file_datetime = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
		current_datetime = datetime.now()
		time_difference = current_datetime - file_datetime
		days_passed = time_difference.days

		days_passed = int(days_passed+135)

		rkey = types.ReplyKeyboardMarkup(True, True)
		rkey.row('👛 Кошелек', '🉑 BNB')
		rkey.row('📙 Информация')
		bot.send_message(message.chat.id, f"📙 <b>Информация</b>\n\n⏳ Работаем: <b>{days_passed} дней</b>\n🐳 Участников: <b>{users}</b>", reply_markup=rkey, parse_mode="HTML", disable_web_page_preview = True)
	if message.text == "🉑 BNB":
		with open(f"users/{user_id}/bnb_last.txt", 'r') as file:
		    date_str = file.read().strip()
		file_datetime = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
		current_datetime = datetime.now()
		time_difference = current_datetime - file_datetime
		if time_difference > timedelta(hours=1):
			current_datetime = datetime.now()
			formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
			file = open(f"users/{user_id}/bnb_last.txt", "w" , encoding="utf-8")
			file.write(formatted_datetime)
			file.close()

			file = open(f"users/{user_id}/bnb_balance.txt", "r" , encoding="utf-8")
			old_balance = file.read()
			file.close()
			new_balance = float(old_balance) + 0.0003
			file = open(f"users/{user_id}/bnb_balance.txt", "w" , encoding="utf-8")
			file.write(f"{new_balance}")
			file.close()


			rkey = types.ReplyKeyboardMarkup(True, True)
			rkey.row('👛 Кошелек', '🉑 BNB')
			rkey.row('📙 Информация')
			bot.send_message(message.chat.id, f"🐳 Ваш баланс пополнен на 0,0003 BNB", reply_markup=rkey, parse_mode="HTML", disable_web_page_preview = True)
		else:
			time_remaining = timedelta(hours=1) - time_difference
			formatted_time_remaining = str(time_remaining).split('.')[0]  
			rkey = types.ReplyKeyboardMarkup(True, True)
			rkey.row('👛 Кошелек', '🉑 BNB')
			rkey.row('📙 Информация')
			bot.send_message(message.chat.id, f"⚠️ Сегодня вы уже получили BNB приходи через <b>{formatted_time_remaining}</b> чтобы получить ещё!", reply_markup=rkey, parse_mode="HTML", disable_web_page_preview = True)
	if message.text == "👛 Кошелек":
		file = open(f"users/{user_id}/bnb_balance.txt", "r" , encoding="utf-8")
		balance = file.read()
		file.close()
		inline = types.InlineKeyboardMarkup()
		inline.add(types.InlineKeyboardButton("📤 Вывод", callback_data=f"balout"))
		bot.send_message(message.chat.id, f"👛 <b>Кошелек</b>\n\n🐳 {message.from_user.username}\n🆔 <code>{message.from_user.id}</code>\n\n🉑 BNB <b>{balance}</b>", reply_markup=inline, parse_mode="HTML", disable_web_page_preview = True)
	if message.text == "/admin" and message.chat.id in admins:
		users = len(os.listdir(f"users"))
		inline = types.InlineKeyboardMarkup()
		inline.add(types.InlineKeyboardButton("Рассылка", callback_data=f"textmm"))
		bot.send_message(message.chat.id, f"Пользователей в боте: {users}", reply_markup=inline, parse_mode="HTML", disable_web_page_preview = True)


@bot.callback_query_handler(func=lambda call: True)
def pressed(call: types.CallbackQuery):
	chatid = call.message.chat.id
	message_id = call.message.message_id
	fromuserid = call.from_user.id
	command = call.data[:6]
	data = call.data[6:]
	data_main_list = data.split(")")
	bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)

	if command == "balout":
		file = open(f"users/{chatid}/bnb_balance.txt", "r" , encoding="utf-8")
		balance = file.read()
		file.close()
		if float(balance) >= 0.031:	
			msg = bot.edit_message_text(chat_id=chatid, message_id=message_id, text="📤Введите сумму вывода: ", parse_mode="HTML")
			bot.register_next_step_handler(msg, balout1, message_id)
		else:
			bot.send_message(chat_id=chatid, text="⛔️ На вашем балансе, недостаточно <b>BNB\n\nМинимальный вывод 0.031 BNB</b>", parse_mode="HTML", disable_web_page_preview = True)
	if command == "textmm":
		inline = types.InlineKeyboardMarkup()
		inline.add(types.InlineKeyboardButton("Отмена", callback_data=f"delmsg"))
		msg = bot.edit_message_text(chat_id=chatid, message_id=message_id, text="Введите сообщение которое отправится всем пользователям: ", reply_markup=inline, parse_mode="HTML")
		bot.register_next_step_handler(msg, textmam, message_id)
	if command == "delmsg":
		bot.delete_message(chatid, message_id)



def balout1(message, message_id):
	bot.delete_message(message.chat.id, message.message_id)
	if message.text:
		file = open(f"users/{message.chat.id}/bnb_balance.txt", "r" , encoding="utf-8")
		balance = file.read()
		file.close()

		if message.text.replace('.', "").isdigit():
			if float(message.text) <= float(balance):
				msg = bot.edit_message_text(chat_id=message.chat.id, message_id=message_id, text="📤Введите кошелёк для вывода: ", parse_mode="HTML")
				bot.register_next_step_handler(msg, balout2, message_id, message.text)
			else:
				bot.send_message(chat_id=message.chat.id, text="⛔️ Недостаточно баланса", parse_mode="HTML", disable_web_page_preview = True)
		else:
			bot.send_message(chat_id=message.chat.id, text="⛔️ Введите сумму числом", parse_mode="HTML", disable_web_page_preview = True)
	else:
		bot.send_message(chat_id=message.chat.id, text="⛔️ Неверная сумма", parse_mode="HTML", disable_web_page_preview = True)

def balout2(message, message_id, summa):
	bot.delete_message(message.chat.id, message.message_id)
	if message.text:
		file = open(f"users/{message.chat.id}/bnb_balance.txt", "r" , encoding="utf-8")
		old_balance = file.read()
		file.close()
		new_balance = float(old_balance) - float(summa)
		file = open(f"users/{message.chat.id}/bnb_balance.txt", "w" , encoding="utf-8")
		file.write(f"{new_balance}")
		file.close()

		bot.edit_message_text(chat_id=message.chat.id, message_id=message_id, text="✅ Заявка на вывод создана, средства будут зачисленны в течении 24 часов!", parse_mode="HTML", disable_web_page_preview = True)

	else:
		bot.send_message(chat_id=message.chat.id, text="⛔️ Неверный кошелёк", parse_mode="HTML", disable_web_page_preview = True)


def balout1(message, message_id):
	bot.delete_message(message.chat.id, message.message_id)
	if message.text:
		bot.edit_message_text(chat_id=message.chat.id, message_id=message_id, text="Ожидайте, рассылка начата...", parse_mode="HTML")
		for user in os.listdir(f"users"):
			good = 0
			try:
				bot.send_message(user, f"{message.text}", parse_mode="HTML")
				good += 1
			except:
				pass
		bot.edit_message_text(chat_id=message.chat.id, message_id=message_id, text=f"Рассылка завершена, сообщение отправлено {good} пользователям", parse_mode="HTML")
	else:
		bot.edit_message_text(chat_id=message.chat.id, message_id=message_id, text="Неверный текст", parse_mode="HTML")




print("BNB BOt Start")

while True:
    try:
        bot.polling()
    except Exception as e:
    	try:
    		print(e)
    	except:
    		pass