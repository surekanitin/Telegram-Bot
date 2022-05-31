from telegram import Update
from telegram.ext import CallbackContext
import requests

#sending start message
def start(update:Update,context:CallbackContext):
    context.bot.send_chat_action(update.effective_chat.id, 'typing')
    update.message.reply_text(f'Hello {update.effective_user.first_name}') 
    context.bot.send_message(chat_id=update.effective_chat.id,text="I'm a bot,please talk to me!,Hey There,\nExamples Use /dog to get random images of dog\nUse /covid \"India\" to get the covid Updates,\nUse /stock \"RELIANCE.NS\" to get real-time stock price.")  

#Sending the message/url using two   parameters, the image URL and the recipient’s ID — this can be group ID or user ID
def dogImage(update:Update,context:CallbackContext):  
    context.bot.send_chat_action(update.effective_chat.id, 'typing')
    contents=requests.get('https://random.dog/woof.json').json()
    url=contents['url']
    chat_id= update.effective_chat.id #getting user id
    context.bot.send_photo(chat_id=chat_id,photo=url)#got error in update.message.chat_id so changed it to context

#Echo same messaage sent by the user
def echo(update:Update,context:CallbackContext):
    context.bot.send_chat_action(update.effective_chat.id, 'typing')
    context.bot.send_message(chat_id=update.effective_chat.id,text=update.message.text)

#for handling unkown commands
def unknown(update: Update, context: CallbackContext):
     context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")
