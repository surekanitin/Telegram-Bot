from telegram import Update
from telegram.ext import CallbackContext
import requests

#sending start message
def start(update:Update,context:CallbackContext):
    context.bot.send_chat_action(update.effective_chat.id, 'typing')
    update.message.reply_text(f'Hello {update.effective_user.first_name}') 
    context.bot.send_message(chat_id=update.effective_chat.id,text="I'm a bot,please talk to me!,\nHow to use the commands?\n/dog to get random images of dog\n/covid \"India\" to get the covid Updates,\n/stock \"RELIANCE.NS\" to get real-time stock price.\n/weather \"Chenai\" to get real-time weather updates.")  

def getImage():
    contents=requests.get('https://random.dog/woof.json').json()
    url=contents['url']
    return url
#Sending the message/url using two   parameters, the image URL and the recipient’s ID — this can be group ID or user ID
def dogImage(update:Update,context:CallbackContext):  
    context.bot.send_chat_action(update.effective_chat.id,action='upload_photo')
    url=getImage()
    context.bot.send_photo(chat_id=update.effective_chat.id ,photo=url)#got error in update.message.chat_id so changed it to context

#Echo same messaage sent by the user
def echo(update:Update,context:CallbackContext):
    context.bot.send_chat_action(update.effective_chat.id, 'typing')
    context.bot.send_message(chat_id=update.effective_chat.id,text=update.message.text)

#for handling unkown commands
def unknown(update: Update, context: CallbackContext):
     context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")
