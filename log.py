import pymysql

class Logger:
    def getCursor():
        conn = pymysql.connect(host='hattetnd.suplitter.com', user='root', password='@Qkrdnjsgh5654', charset='utf8', database="hattend") 
        cursor = conn.cursor() 
        return conn, cursor
    
    def loginLog(id, password):
        pass
        # sql = "insert into login_log (id, password, date) values (%s, %s, now())" 
        
        # conn, cursor = Logger.getCursor()
        # cursor.execute(sql, (id, password)) 

        # conn.commit()
        # conn.close()

if __name__ == "__main__":
    Logger.loginLog("test", "test")