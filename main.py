from telegram.ext import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import random
global tteam
tteam = "Ni idea"
global o1
o1 = "AAAA"
global o2
o2 = "BBBB"
global pprova
pprova= "Ni idea 2"
print('Starting up bot...')


token = '6344002418:AAERnk1LQ85-JLLrC6ysr32Ab5I5-vqGSGM'
camp_list = ["Moixons","Feres","Tomasa","Dalt","Freixe","Alzina","Pi","Om","Piset"]

tasques = {
    "Moixons" : [],
    "Feres" : [],
    "Tomasa" : [],
    "Dalt" : [],
    "Freixe" : [],
    "Alzina" : [],
    "Pi" : [],
    "Om" : [],
    "Piset" : []
}
# Lets us use the /start command
def start_command(update, context):
    update.message.reply_text('Hello there! I\'m a bot. What\'s up?')

def prova_command(update, context):
    update.message.reply_text(f'Hola! En aquests moments, la pinça la té el grup de {tteam}. La seva prova és la següent: {pprova}')


# Lets us use the /help command
def help_command(update, context):
    update.message.reply_text('Try typing anything and I will do my best to respond!')


# Lets us use the /custom command
def custom_command(update, context):
    update.message.reply_text('This is a custom command, you can add whatever text you want here.')

def jointeam_start(update, context):
    update.message.reply_text('A qui li passes la pinça?',reply_markup = jointeam_kb())

def jointeam_kb():
    red_camp_list = random.sample(camp_list, 3)
    keyboard = [
        [InlineKeyboardButton(red_camp_list[0], callback_data=red_camp_list[0]),
         InlineKeyboardButton(red_camp_list[1],  callback_data=red_camp_list[1]),
         InlineKeyboardButton(red_camp_list[2],  callback_data=red_camp_list[2]),],
    ]
    return InlineKeyboardMarkup(keyboard)

def jointeam_proceed(update, context):

    query = update.callback_query
    query.answer()
    team = query.data
    global tteam
    tteam = team
    query.edit_message_text(text=f"D'acord! Quina prova ha de fer la bona gent de {team}?")
    query.message.reply_text("Opció 1: AAAAA")
    query.message.reply_text("Opció 2: BBBBB")
    query.message.reply_text('Tria la prova',reply_markup = triaprova_kb())

def triaprova_kb():
    keyboard = [
        [InlineKeyboardButton("Opció 1", callback_data="Opció 1"),
         InlineKeyboardButton("Opció 2", callback_data="Opció 2"),],
    ]
    return InlineKeyboardMarkup(keyboard)
def triaprova_proceed(update, context):

    query = update.callback_query
    query.answer()
    opc = query.data
    if opc == "Opció 1":
        prova = o1
    else:
        prova = o2
    global pprova
    pprova = prova
    query.edit_message_text(text=f"D'acord! La gent de {tteam} haurà de fer el següent: {pprova}")


def handle_response(text) -> str:
    # Create your own response logic

    if 'hello' in text:
        return 'Hey there!'

    if 'how are you' in text:
        return 'I\'m good!'

    return 'I don\'t understand'


def handle_message(update, context):
    # Get basic info of the incoming message
    message_type = update.message.chat.type
    text = str(update.message.text).lower()
    response = ''

    # Print a log for debugging
    print(f'User ({update.message.chat.id}) says: "{text}" in: {message_type}')

    # React to group messages only if users mention the bot directly
    if message_type == 'group':
        # Replace with your bot username
        if '@bot19292bot' in text:
            new_text = text.replace('@bot19292bot', '').strip()
            response = handle_response(new_text)
    else:
        response = handle_response(text)

    # Reply normal if the message is in private
    update.message.reply_text(response)


# Log errors
def error(update, context):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('prova', prova_command))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('custom', custom_command))

    dp.add_handler(CommandHandler('novaprova', jointeam_start))
    dp.add_handler(CallbackQueryHandler(triaprova_proceed, pattern='^(|Opció 1|Opció 2)$'))
    dp.add_handler(CallbackQueryHandler(jointeam_proceed, pattern=None))



    # Messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Log all errors
    dp.add_error_handler(error)

    # Run the bot
    updater.start_polling(1.0)
    updater.idle()
