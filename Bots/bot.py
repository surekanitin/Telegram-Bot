#import libraries
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters
import logging
from Utils.covid import covid_result
from Utils.stock import stock_result
from Utils.cmd import start,echo,dogImage,unknown
from Utils.weather import weather_result
from Data.my_keys import pu_project_bot_token
#lOG
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

#main program
def main():
    #add token
    updater=Updater(pu_project_bot_token,use_context=True)
    dp=updater.dispatcher.add_handler
    dp(CommandHandler("start",start))  
    dp(CommandHandler('dog',dogImage))
    dp(CommandHandler("covid",covid_result)) 
    dp(CommandHandler("Stock",stock_result))
    dp(CommandHandler("weather",weather_result))
    dp(MessageHandler(Filters.text & (~Filters.command),echo))  
    dp(MessageHandler(Filters.command, unknown))                          
    updater.start_polling()
    updater.idle()

#calling main
if __name__ == '__main__':
    main()      
    