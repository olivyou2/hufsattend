import pymysql

class Logger:
    def getCursor():
        conn = pymysql.connect(host='localhost', user='root', password='password', charset='utf8') 
        cursor = conn.cursor() 
        return conn, cursor
    
    def loginLog(id, password):
        sql = "insert into login_log (id, password, date) values (%s, %s, now())" 
        
        conn, cursor = Logger.getCursor()
        cursor.execute(sql, (id, password)) 

        conn.commit()
        conn.close()