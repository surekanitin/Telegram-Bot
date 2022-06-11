#import libraries
import logging,sys,os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../Utils")
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../Data")
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater,InlineQueryHandler
import menu,covid,stock,weather
import my_keys

#lOG
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)


#main program
def main():
    #add token
    updater=Updater(my_keys.pu_project_bot_token,use_context=True)
    dp=updater.dispatcher.add_handler
    dp(CommandHandler("start",menu.start))  
    dp(InlineQueryHandler(menu.inline_pu))
    dp(CommandHandler('dog',menu.dogImage))
    dp(CommandHandler("covid",covid.covid_result)) 
    dp(CommandHandler("Stock",stock.stock_result))
    dp(CommandHandler("weather",weather.weather_result))
    dp(MessageHandler(Filters.text & (~Filters.command),menu.echo))  
    dp(MessageHandler(Filters.command, menu.unknown))                          
    updater.start_polling()
    updater.idle()


#calling main
if __name__ == '__main__':
    main()      
    