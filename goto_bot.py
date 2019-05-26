import telebot as tb  # импортим библиотеки
import requests

debag = False  # отправление ошибок в лс
creator = None  # id запускателя
token = None  # токен ботяры

try:
	f = open('config.txt','r')
	exec( f.read() ) # пытаемся открыть и прочитать конфиг
	f.close()
except FileNotFoundError:  # если файл не найден
	print('Файл конфига не найден')
	input()
	exit()
except Exception as e:  # если конфиг не читается нормально
	print('Ошибка в конфиге: '+str(e))
	input()
	exit()

if creator == None or token == None:  # если в конфиге не указан токен или создатель
	print('Ошибка в конфиге')
	input()
	exit()
if debag:  # если включен дебаг
	import sys
	class Ferr:  # подменяем класс вывода ошибок для и отправления в лс
		def __init__(s):
			s.data = ''
		def write(s, t):
			s.data += t
		def flush(s):
			if s.data:
				e = '<code>'+s.data.replace('<','&lt;').replace('>','&gt;')+'</code>'
				bot.send_message(creator,e,parse_mode='HTML')
	sys.stderr = Ferr()

bot = tb.TeleBot(token)  # собственно создаём экземпляр класса ботяры

@bot.message_handler( commands=['goto'] )  # функция на команду goto
def com_goto(m):
	u = m.from_user.username  # берём ник челика
	if u==None:  # если его нет
		bot.reply_to(m, 'Сначала поставь себе ник')
		return 0
	e = requests.get( 'http://ragna.club/'+u ).text  # переходим по ссылке и сохраняем HTML как текст
	if '<h2>' in e:
		e = e.split('<h2>')[-1].split('</h2>')[0]  # если там не только текст, вырезаем только нужную фразу
	bot.reply_to(m, 'Рагна говорит:\n'+e)  # отправляем результат

bot.send_message(creator, 'бот запустился')  # пишем, что всё запустилось
print('бот запустился')

try:
	bot.infinity_polling(True)  # запускаем
except Exception as e:
	bot.send_message(creator, 'бот лёг')
	raise e
