import pymysql

HOST = 'q-note-nazarrudenok.e.aivencloud.com'
USER = 'avnadmin'
PASSWORD = 'AVNS_TtF4mkbe35BWIDWBbPz'
DATABASE = 'defaultdb'
PORT = 21199

conn = pymysql.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE,
    port=PORT
)

cursor = conn.cursor()