import sqlite3

connection = sqlite3.connect('Customer.db')
cursor = connection.cursor()

cursor.execute("drop table CUSTOMER;")
sql_cmd='''CREATE TABLE CUSTOMER(
           NAME VARCHAR(15), 
           MAIL VARCHAR(25) PRIMARY KEY, 
           PASSWORD VARCHAR(8) NOT NULL);'''

cursor.execute(sql_cmd)
print("Table created successfully")

# cursor.execute("DESC Customer;")

sql_cmd='''INSERT INTO CUSTOMER VALUES(
           'admin','admin@gmail.com','admin');'''

cursor.execute(sql_cmd)
print("admin record added succesfully")

sql_cmd='''INSERT INTO CUSTOMER VALUES(
           'Ram','ram@gmail.com','ram001');'''

cursor.execute(sql_cmd)
print("customer record added succesfully")

connection.commit()

sql_cmd='''SELECT NAME, MAIL, PASSWORD FROM CUSTOMER;'''
cursor.execute(sql_cmd)
rows=cursor.fetchall()
print(rows)

connection.commit()
connection.close()

