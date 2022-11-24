import telebot as tgbot
from telebot import types
from config import keys , TOKEN
from extensions import APIException , CryptoConverter

bot = tgbot.TeleBot ( TOKEN )


@bot.message_handler ( commands=["start" , "help"] )
def help_my( message: tgbot.types.Message ) :
    markup = types.ReplyKeyboardMarkup ( resize_keyboard=True )
    btn1 = types.KeyboardButton ( "Доступные валюты" )
    btn2 = types.KeyboardButton ( "Help!" )
    markup.add ( btn1 , btn2 )
    text = ("Чтобы начать работу, введите команду в формате:\n<имя валюты, цену которой вы хотите узнать>"
            "<имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>\n"
            "увидеть список всех доступных валют: /values")
    bot.reply_to ( message , text, reply_markup= markup)


@bot.message_handler ( commands=["values"] )
def values_help( message: tgbot.types.Message ) :
    text = "Доступные валюты: "
    for key in keys.keys ( ) :
        text = "\n".join ( (text , key) )
    bot.reply_to ( message , text )


@bot.message_handler ( content_types=["text" , ] )
def convert( message: tgbot.types.Message ) :
    if message.text == "Доступные валюты":
        values_help(message)
    elif message.text == "Help!":
        help_my(message)
    else:
        try :
            values = message.text.split ( " " )
            if len ( values ) != 3 :
                raise APIException (
                    f"Неверное количество параметров - {len ( values )}\nтребуемый формат - 3:\n<имя валюты> "
                    "<в какую валюту перевести>"
                    "<количество переводимой валюты>\n" )

            base , quote , amount , = list(map(str.lower, values))
            total_base = abs ( CryptoConverter.get_price ( base , quote , amount )* float ( amount ) )
        except APIException as e :
            bot.reply_to ( message , f"Ошибка на стороне пользователя\n{e}" )
        except Exception as e :
            bot.reply_to ( message , f"Не удалось обработать команду\n{e}" )
        else :
            text = f'Цена {abs(float(amount))} {base} в {quote} : {total_base}\n'
            bot.send_message ( message.chat.id , text )


bot.polling ( )
