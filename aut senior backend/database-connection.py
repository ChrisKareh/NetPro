import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Test@1234",
  database="senior_db"
)


cursor = mydb.cursor()


create_table_query = """
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255),
  password VARCHAR(255)
)
"""
cursor.execute(create_table_query)


insert_query = """
INSERT INTO users (email, password)
VALUES ('alainsenior@gmail.com', 'alainalain')
"""
cursor.execute(insert_query)
mydb.commit()


cursor.close()
mydb.close()
