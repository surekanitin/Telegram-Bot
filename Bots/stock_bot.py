#import libraries
from telegram.ext import Updater,InlineQueryHandler,CommandHandler,CallbackContext,MessageHandler,Filters
import logging,sys,os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../Utils")
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../Data")
import menu,stock
import my_keys
from telegram import InputTextMessageContent,Update,InlineQueryResultArticle
from uuid import uuid4
# lOG
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)


def start(update:Update,context:CallbackContext):
    context.bot.send_chat_action(update.effective_chat.id, 'typing')
    update.message.reply_text(f'Hello {update.effective_user.first_name}') 
    context.bot.send_message(chat_id=update.effective_chat.id,text="I'm a bot,please talk to me!,\nHow to use the commands?\n/stock \"RELIANCE.NS\" to get real-time stock price.\n")  

def inline_stock(update:Update,context:CallbackContext):
    options= list()
    symbol = update.inline_query.query
    logging.info('Query received: %s', symbol)
    options.append(
            InlineQueryResultArticle(
                id=uuid4(),
                title="Stock",
                description="Real Time Stock Updates",
                input_message_content=InputTextMessageContent(stock.stock(symbol))))
    update.inline_query.answer(options,switch_pm_text='Switch to PM mode',switch_pm_parameter='Start')

def main():
    #add token
    updater=Updater(my_keys.realtimestockbot_token,use_context=True)
    dp=updater.dispatcher.add_handler
    dp(CommandHandler("start",start)) 
    dp(CommandHandler("stock",stock.stock_result)) 
    dp(InlineQueryHandler(inline_stock))
    dp(MessageHandler(Filters.text & (~Filters.command),menu.echo))  
    dp(MessageHandler(Filters.command, menu.unknown))                          
    updater.start_polling()
    updater.idle()

#calling main
if __name__ == '__main__':
    main()     