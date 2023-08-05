from random import choice, randint


version = "2022.0.2"


def foxVersion():
	return version

def foxInt(xInt = None, yInt = None):
	if xInt == None and yInt == None:
		return print('Аргументы не введены в функции foxInt, "xInt" и "yInt"!')
	elif xInt == None:
		return print('Аргумент не введён в функции foxInt, "xInt"!')
	elif yInt == None:
		yInt = xInt
		xInt = 0
	try:
		return randint(xInt, yInt)
	except ValueError:
		print('Произошла ошибка: Похоже X(икс) или Y(игрик) (foxRandomInt) не являются числом или вы используете десятичные числа и т.п.! Данная функция принимает только обычные цифры например "-1", "5"!')
		return '-----------------------------------------------------------'
	except:
		print('Произошла неизвестная ошибка с функцией foxInt! Если вы хотите, можете скинуть ошибку(или скрин ошибки) мне на почту bfire1999@gmail.com!')
		return '-----------------------------------------------------------'

def foxChoice(list = None):
	if list == None:
		return print('Отсутствует список в функции foxChoice!')
	try:
		return choice(list)
	except:
		print('Произошла неизвестная ошибка с функцией foxChoice! Если вы хотите, можете скинуть ошибку(или скрин ошибки) мне на почту bfire1999@gmail.com!')
		return '-----------------------------------------------------------'

def foxTime(style = None, token = None, types=1):
	if types == 2:
		if style != None:
			style == None
			print('Предупреждение: Вы использовали аргумент "types=2" в функции foxTime, вы также указали style, но с данным аргументом он не работает!')
		if token != None:
			token == None
			print('Предупреждение: Вы использовали аргумент "types=2" в функции foxTime, вы также указали token, но с данным аргументом он не работает!')

	if types == 1:
		if token == None:
			if style == None: token = ':'
			if style == 'one': token = '-'
			if style == 'two': token = '∙'
			else: style == 'None'

		if style == None:
			minutes = randint(1, 59)
			hours = randint(1, 12)
			if minutes < 10: minutes = f'0{minutes}'
			if hours < 10: hours = f'0{hours}'
			return f"{hours}{token}{minutes}"
		if style == 'one':
			minutes = randint(1, 59)
			hours = randint(1, 12)
			if minutes < 10: minutes = f'0{minutes}'
			if hours < 10: hours = f'0{hours}'
			return f"{hours}{token}{minutes}"
		if style == 'two':
			minutes = randint(1, 59)
			hours = randint(1, 12)
			if minutes < 10: minutes = f'0{minutes}'
			if hours < 10: hours = f'0{hours}'
			return f"{hours}{token}{minutes}"
		else:
			return 'Не существующий стиль! (foxTime)'
	if types == 2:
		day: Int = randint(1, 30)
		month: Int = randint(1, 12)
		if month == 1: month = 'Января'
		if month == 2: month = 'Февраля'
		if month == 3: month = 'Марта'
		if month == 4: month = 'Апреля'
		if month == 5: month = 'Мая'
		if month == 6: month = 'Июня'
		if month == 7: month = 'Июля'
		if month == 8: month = 'Августа'
		if month == 9: month = 'Сентября'
		if month == 10: month = 'Октября'
		if month == 11: month = 'Ноября'
		if month == 12: month = 'Декабря'
		return f"{day} {month}"
	else:
		return 'Такого типа не существует! (foxTime)'