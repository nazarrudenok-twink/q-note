import pymysql

HOST = 'localhost'
USER = 'root'
PASSWORD = ''
DATABASE = 'q-note'

conn = pymysql.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE
)

cursor = conn.cursor()