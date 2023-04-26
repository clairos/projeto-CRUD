import mysql.connector 

conexao = mysql.connector(
    host='localhost',
    user='root',
    password='',
    database='bd_prog'
)

cursor = conexao.cursor()

# CRUD

cursor.close()
conexao.close()