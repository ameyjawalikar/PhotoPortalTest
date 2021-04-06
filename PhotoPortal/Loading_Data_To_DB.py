import os
import pyodbc
import textwrap
import json
from processing import views

driver = '{ODBC Driver 17 for SQL Server}'
server_name = 'tcp:sqlserveruat2021'
database_name = 'TestDB'
server = '{server_name}.database.windows.net, 1433'.format(server_name=server_name)
#server='tcp:sqlserveruat2021.database.windows.net, 1433'
print(server)
user_name ='systemadmin'
password ='Test@123'

connection_string = textwrap.dedent('''
    Driver= {driver};
    Server= {server};
    Database={database_name};
    Uid={user_name};
    Pwd={password};
    Encrypt=yes;
    TrustServerCertificate=No;
    Connection Timeout=30;
'''.format(
    driver=driver,
    server=server,
    database_name=database_name,
    user_name=user_name,
    password=password
))

#Creating the connection
cnxn = pyodbc.connect(connection_string)

cursor = cnxn.cursor()

#Test select Query & result Query
#select_query='Select * from [ImageDetails]'
#cursor.execute(select_query)
#print(cursor.fetchall())

local_path = 'C:\\Users\\AJ58394.IND\\Desktop\\Testing\\PhotoApp\\ImagesToSend\\Good'
for files in os.listdir(local_path):
    a = views.quality_detection(os.path.join(local_path,files))
    res = json.loads(a)
    sql = "INSERT INTO ImageDetails (Name, quality, bluriness, darkness, brightness) VALUES (?, ?, ?, ?, ?)"
    val = (files, res['quality'], res['bluriness'], res['darkness'], res['brightness'])
    cursor.execute(sql, val)
    cnxn.commit()
    print(val)
print(cursor.rowcount, "record inserted.")

