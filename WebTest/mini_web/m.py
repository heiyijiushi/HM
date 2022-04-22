from HttpWebServer import *

import pymysql
if __name__ == '__main__':
    webServer=HttpWebServer(8080)
    webServer.start()
    # conn=pymysql.connect(host='localhost',database="stock_db",user='root',password='mysql',)
    # conn.close()