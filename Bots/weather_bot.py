#import libraries
from telegram.ext import Updater,InlineQueryHandler,CommandHandler,CallbackContext,MessageHandler,Filters
import logging,sys,os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../Utils")
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../Data")
import cmd,weather,my_keys
from telegram import InputTextMessageContent,Update,InlineQueryResultArticle
from uuid import uuid4
# lOG
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

def start(update:Update,context:CallbackContext):
    context.bot.send_chat_action(update.effective_chat.id, 'typing')
    update.message.reply_text(f'Hello {update.effective_user.first_name}') 
    context.bot.send_message(chat_id=update.effective_chat.id,text="I'm a bot,please talk to me!,\nHow to use the commands?\n/weather \"Pondicherry\" to get real-time weather updates.")  
def inline_weather(update:Update,context:CallbackContext):
    options= list()
    city = update.inline_query.query
    logging.info('Query received: %s', city)
    options.append(
            InlineQueryResultArticle(
                id=uuid4(),
                title="Weather",
                description="Real Time Weather Updates",
                input_message_content=InputTextMessageContent(weather(city))))
    update.inline_query.answer(options)

def main():
    #add token
    updater=Updater(my_keys.weatherrealtimebot_token,use_context=True)
    dp=updater.dispatcher.add_handler
    dp(CommandHandler("start",start)) 
    dp(CommandHandler("weather",weather.weather_result)) 
    dp(InlineQueryHandler(inline_weather))
    dp(MessageHandler(Filters.text & (~Filters.command),cmd.echo))  
    dp(MessageHandler(Filters.command, cmd.unknown))                          
    updater.start_polling()
    updater.idle()

#calling main
if __name__ == '__main__':
    main()     