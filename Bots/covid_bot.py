#import libraries
from pytz import common_timezones
from telegram.ext import Updater,InlineQueryHandler,CommandHandler,CallbackContext,MessageHandler,Filters
import logging
from telegram import InputTextMessageContent,Update,InlineQueryResultArticle
from Utils.covid import covid,covid_result
from Utils.cmd import echo,unknown
from Data.my_keys import realtimecovidbot_token
from uuid import uuid4
# lOG
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

def start(update:Update,context:CallbackContext):
    context.bot.send_chat_action(update.effective_chat.id, 'typing')
    update.message.reply_text(f'Hello {update.effective_user.first_name}') 
    context.bot.send_message(chat_id=update.effective_chat.id,text="I'm a bot,please talk to me!,\nHow to use the commands?\n/covid \"India\" to get the covid Updates")  

def inline_covid(update:Update,context:CallbackContext):
    options= list()
    user_input = update.inline_query.query
    logging.info('Query received: %s', user_input)
    options.append(
        InlineQueryResultArticle(
            id=uuid4(),
            title="Covid Updates",
            description="Real Time Covid Updates",
            input_message_content=InputTextMessageContent(covid(user_input))))
    update.inline_query.answer(options)

def main():
    #add token
    updater=Updater(realtimecovidbot_token,use_context=True)
    dp=updater.dispatcher.add_handler
    dp(CommandHandler("start",start))
    dp(CommandHandler("covid",covid_result)) 
    dp(InlineQueryHandler(inline_covid))
    dp(MessageHandler(Filters.text & (~Filters.command),echo))  
    dp(MessageHandler(Filters.command, unknown))                          
    updater.start_polling()
    updater.idle()

#calling main
if __name__ == '__main__':
    main()     