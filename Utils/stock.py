from telegram import Update
from telegram.ext import CallbackContext
import yfinance as yf


def stock(symbol):
    intra = yf.download(tickers=symbol, period='1d', interval='5m')
    daily = yf.download(tickers=symbol, period='2d', interval='1d')
    price=[]
    for col in intra.iloc[-1]:
        price.append(round(col,2))
    prev_close=daily['Close']
    percentage_change=prev_close.pct_change()*100
    result=f'''
Real Time Share Price of {symbol}
Time : {intra.index[-1]} HRS
Open : {price[0]}
High : {price[1]}
Low : {price[2]}
Close : {price[3]}
Adj Close : {price[4]}
Volume : {price[5]}
Change : {round(percentage_change[-1],2)} %
    '''
    return result
    

#stock real-time price
def stock_result(update:Update,context:CallbackContext):
    context.bot.send_chat_action(update.effective_chat.id, 'typing')
    try:
        symbol=' '.join(map(str,context.args))
        if symbol == '':
            context.bot.send_chat_action(update.effective_chat.id,'typing')
            context.bot.send_message(update.effective_chat.id,text="Please type the country name like \"/symbol TCS.NS\".\n")
        else:
            context.bot.send_chat_action(update.effective_chat.id,'typing')
            context.bot.send_message(update.effective_chat.id,text="Displaying Results for "+symbol)
            try:
                ans=stock(symbol)
                context.bot.send_chat_action(update.effective_chat.id,'typing')
                context.bot.send_message(update.effective_chat.id,ans)
            except:
                context.bot.send_chat_action(update.effective_chat.id,'typing')
                context.bot.send_message(update.effective_chat.id,text="Stock does not exist!!")
    except:
        context.bot.send_chat_action(update.effective_chat.id,'typing')
        context.bot.send_message(update.effective_chat.id,text="Please type the stock symbol name like \"/stock TCS.NS\".\n")

    # symbol=''.join(map(str, context.args))
    # if symbol == '':
    #     context.bot.send_chat_action(update.effective_chat.id,'typing')
    #     context.bot.send_message(update.effective_chat.id,text="Please type the stock symbol like \"/stock TCS.NS\".\n")
    # else:
    #     context.bot.send_chat_action(update.effective_chat.id,'typing')
    #     context.bot.send_message(update.effective_chat.id,text="Displaying Results for "+symbol)
    #     try:
    #         data=stock(symbol)
    #         context.bot.send_chat_action(update.effective_chat.id,'typing')
    #         context.bot.send_message(update.effective_chat.id,data)
    #     except:
    #         context.bot.send_chat_action(update.effective_chat.id,'typing')
    #         context.bot.send_message(update.effective_chat.id,text="Symbol does not exist!!")
        