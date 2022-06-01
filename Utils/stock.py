from telegram import Update
from telegram.ext import CallbackContext
import yfinance as yf

#stock real-time price
def stock(update:Update,context:CallbackContext):
    context.bot.send_chat_action(update.effective_chat.id, 'typing')
    symbol=' '.join(map(str, context.args))
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
    context.bot.send_chat_action(update.effective_chat.id,'typing')
    context.bot.send_message(update.effective_chat.id,result)