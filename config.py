import pymysql

timeout = 10
connection = pymysql.connect(
  charset="utf8mb4",
  connect_timeout=timeout,
  cursorclass=pymysql.cursors.DictCursor,
  db="defaultdb",
  host="q-note-nazarrudenok.e.aivencloud.com",
  password="AVNS_TtF4mkbe35BWIDWBbPz",
  read_timeout=timeout,
  port=21199,
  user="avnadmin",
  write_timeout=timeout,
)
  
cursor = connection.cursor()