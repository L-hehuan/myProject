import pymysql
def doIt(query):
    conn=pymysql.Connect(database='mysql_python',
        host='localhost',
        user='root',
        password='root',
        port=3306)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
def Excuit(query):
    conn=pymysql.Connect(database='mysql_python',
        host='localhost',
        user='root',
        password='root',
        port=3306)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    cursor.connection.commit()
    cursor.close()
    conn.close()
    return 1
def getone(query):
    conn=pymysql.Connect(database='mysql_python',
        host='localhost',
        user='root',
        password='root',
        port=3306)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result