import sqlite3

def DBSql(sqlCommand,mod=""):
    con = sqlite3.connect("personalData.db")
    c = con.cursor()
    result = c.execute(sqlCommand)
    if mod == "fetchone":
        result = result.fetchone()
    else:
        result = (result.rowcount == 1)
    con.commit()
    con.close()
    return result

def sqliteAskUser(idUser):
    hesapBilgiDetay = DBSql("select H.accountName, H.apiKey, H.secretKey from data H where H.telegramId = "+str(idUser),"fetchone")
    return hesapBilgiDetay

