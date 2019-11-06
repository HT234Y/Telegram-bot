from telegram import Bot, Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
import apiai, json, requests, re
from config import *

updater = Updater(TOKEN)
dispatcher = updater.dispatcher
button_get_dog = 'Показать рандомную собачку'
button_start = 'Старт'

def show_keybord():
    keyboard = [
        [
            KeyboardButton(button_get_dog),
            KeyboardButton(button_start),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url
def get_image_url():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url
def bop(bot: Bot, update: Update):
    url = get_image_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)

def startCommand(bot : Bot, update: Update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?', reply_markup=show_keybord())
def textMessage(bot : Bot, update: Update):
    request = apiai.ApiAI(client_acces_token).text_request()
    request.lang = 'ru'
    request.session_id = 'KursachAIBot'
    request.query = update.message.text
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    elif update.message.text == button_get_dog:
        return bop(bot=bot, update=update)
    elif update.message.text == button_start:
        return startCommand(bot=bot, update=update)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял!')



start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)

dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)

dispatcher.add_handler(CommandHandler('dog',bop))
updater.start_polling()
updater.idle()
