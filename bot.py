#import libraries
from telegram.ext import Updater,InlineQueryHandler,CommandHandler,CallbackContext,MessageHandler,Filters
import logging
from telegram import InlineQueryResult,InputTextMessageContent,Update,InlineQueryResultArticle
from Utils.covid_data_fetch import covid,covid_result
from Utils.stock import stock,stock_result
from Utils.cmd import start,echo,dogImage,unknown
from Utils.owm import weather,weather_result
from Data.my_keys import telegram_token
from uuid import uuid4
# lOG
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

def inline_bot(update:Update,context:CallbackContext):
    user_input = update.inline_query.query
    # input_split=user_input.split()
    # if input_split[0]=='stock' or '/stock' or '/Stock' or 'Stock':
    #     symbol=input_split[-1]
    # elif input_split[0]=='covid' or '/covid' or '/Covid' or 'covid':
    #     country=input_split[-1]
    # elif input_split[0]=='weather' or '/weather' or '/Weather' or 'Weather':
    #     city=input_split[-1]
    # else:
    #     pass

    options= list()
    options=[
            InlineQueryResultArticle(
                id=uuid4(),
                title="stock",
                description="Stock Updates",
                input_message_content=InputTextMessageContent(stock(user_input))),
            InlineQueryResultArticle(
                id=uuid4(),
                title="covid",
                description="Covid Updates",
                input_message_content=InputTextMessageContent(covid(user_input))),
            InlineQueryResultArticle(
                id=uuid4(),
                title="weather",
                description="Weather Updates",
                input_message_content=InputTextMessageContent(weather(user_input)))]
    #update.inline_query.answer(options)
    context.bot.answerInlineQuery(update.inline_query.id, options)
    

#main program
def main():
    #add token
    updater=Updater(telegram_token,use_context=True)
    dp=updater.dispatcher.add_handler
    dp(CommandHandler("start",start))  
    dp(CommandHandler('dog',dogImage))
    dp(CommandHandler("covid",covid_result)) 
    dp(CommandHandler("Stock",stock_result))
    dp(CommandHandler("weather",weather_result))
    dp(InlineQueryHandler(inline_bot))
    dp(MessageHandler(Filters.text & (~Filters.command),echo))  
    dp(MessageHandler(Filters.command, unknown))                          
    updater.start_polling()
    updater.idle()

#calling main
if __name__ == '__main__':
    main()      
    