# -*- coding: utf-8 -*-
from lib import *

def dialog():
	answer = yield HTML("""Добрый день!<br>Вас приветствует бот-ассистент гостиницы \"Украина\"<br>
		Вы можете узнать <b>адрес</b> гостиницы или проверить возможность <b>бронирования</b><br>
		Что Вас интересует?""")
	gotoAddress = yield from first_of_two("", "Адрес", "Бронирование")
	if gotoAddress:
		answer = yield from getAddress(False)
	else:
		answer = yield from getBooking(False)

def first_of_two(question, lhs, rhs):
	answer = yield (question, [lhs, rhs])
	l_lhs = lhs.text.lower()
	l_rhs = rhs.text.lower()
	while not (l_lhs in answer.text.lower() or l_rhs in answer.text.lower()):
		answer = yield HTML("Я Вас не понимаю, <b>"+l_lhs+"</b> или <b>"+l_rhs+"</b>?")
	return l_lhs in answer.text.lower()

def getAddress(was):
	answer = yield "Наша гостиница расположена по адресу %s" % hotelAddress
	goBooking = yield from first_of_two("Хотите проверить возможность бронирования?", "Да", "Нет")
	if goBooking and not was:
		answer = yield from getBooking(False)
	else:
		answer = yield "До свидания!"

def getBooking(was):
	answer = yield HTML("Введите, пожалуйста, даты Вашего предполагаемого приезда в формате <b>YYYY-MM-DD</b>")
	date = answer.text
	answer = yield "На сколько ночей Вы планируете остановиться?"
	nights = answer.text
	answer = yield "Сколько человек приедет с Вами?"
	adults = str(int(answer.text) + 1)
	answer = yield HTML("Вы можете просмотреть список подходящих номеров <a href=\"%s\">по этой ссылке</a>" % hotelHost + hotelBookingLink + "?date=" + date + "&nights=" + nights + "&adults=" + adults)
	goAddress = yield from first_of_two("Хотите узнать адрес гостиницы?", "Да", "Нет")
	if goBooking and not was:
		answer = yield from getAddress(False)
	else:
		answer = yield "До свидания!"

if __name__ == "__main__":
	dialog_bot = DialogBot(token, dialog)
	dialog_bot.start()