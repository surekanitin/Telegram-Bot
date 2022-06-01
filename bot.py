#import libraries
from telegram import Update,InlineQueryResultArticle,InputTextMessageContent
from telegram.ext import Updater,InlineQueryHandler,CommandHandler,CallbackContext,MessageHandler,Filters
import logging
from Utils.covid_data_fetch import covid
from Utils.stock import stock
from Utils.cmd import start,echo,dogImage,unknown
from Utils.owm import weatherbycity
from Data.my_keys import telegram_token
# lOG
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

#main program
def main():
    #add token
    updater=Updater(telegram_token,use_context=True)
    dp=updater.dispatcher
    dp.add_handler(CommandHandler("start",start))  
    dp.add_handler(CommandHandler('dog',dogImage))
    dp.add_handler(CommandHandler("covid",covid)) 
    dp.add_handler(CommandHandler("Stock",stock))
    dp.add_handler(CommandHandler("weather",weatherbycity))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command),echo))  
    dp.add_handler(MessageHandler(Filters.command, unknown))                          
    updater.start_polling()
    updater.idle()

#calling main
if __name__ == '__main__':
    main()   
    