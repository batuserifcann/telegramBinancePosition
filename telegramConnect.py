import telegram.ext
from telegram.ext import CommandHandler, MessageHandler, Filters
from telegramSql import DBSql,sqliteAskUser
from binance.client import Client

TOKEN = "6052650335:AAHFjkTgWmROj-nhmtqKBEXizQlq1aL6Fbo"

def ApiKey(update,context):
    answerMessage = "Usage /apiKey yourApiKey yourSecretKey : /apiKey 0x12312312312312 129837912837129"
    chatId = update.message.chat.id
    accountName = update.message.chat.username
    print(context.args)
    if context.args and len(context.args) == 2:
        binanceApiKey = context.args[0]
        binanceSecretKey = context.args[1]
        addAccountSql = f"insert into data (telegramId, accountName, apiKey, secretKey) values({chatId},'{accountName}', '{binanceApiKey}', '{binanceSecretKey}')"
        add = DBSql(addAccountSql)
        if add:
            answerMessage = "Your account has been added successfully"
            userData = sqliteAskUser(chatId)
        else:
            answerMessage = "Your account has not been added successfully"
    else:
        answerMessage = "Usage: /setApi yourApiKey yourSecretKey"
    update.message.reply_text(answerMessage)

def help(update,context):
    update.message.reply_text("If you are new, first of all add your user. For this enter /setApi . If you are not new user and if you want to see your positions please enter /checkPositions")
def start(update,context):
    update.message.reply_text("/setApi == For add your api's.\n/checkPositions == For check your positions")
def checkPositions(update,context):
    userData = sqliteAskUser(update.message.chat.id)
    apiKey = userData[1]
    secretKey = userData[2]
    client = Client(apiKey, secretKey)

    # Açık pozisyonları alın
    positions = client.futures_position_information()

    # Pozisyonları yazdırın
    if positions:
        for position in positions:
            if float(position['positionAmt']) > 0:
                symbol = position['symbol']
                position_size = float(position['positionAmt'])
                entry_price = float(position['entryPrice'])
                unrealized_pnl = float(position['unRealizedProfit'])
                message = f"Symbol: {symbol}\nPosition Size: {position_size}\nEntry Price: {entry_price}\nUnrealized Pnl: {unrealized_pnl}"
                update.message.reply_text(message)

    else:
        message = "Açık Pozisyon Bulunamadı"
        update.message.reply_text(message)
        

def echo(update, context):
    output = "You've erroneously processed. Please select one of these:\n/start\n/help\n/setApi\n/checkPositions"
    update.message.reply_text(output)

    
updater = telegram.ext.Updater(TOKEN, use_context=True)
disp = updater.dispatcher


disp.add_handler(CommandHandler("setApi", ApiKey))
disp.add_handler(CommandHandler("start", start))
disp.add_handler(CommandHandler("help", help))
disp.add_handler(CommandHandler("checkPositions", checkPositions))
disp.add_handler(MessageHandler(Filters.text, echo))



updater.start_polling()
updater.idle()