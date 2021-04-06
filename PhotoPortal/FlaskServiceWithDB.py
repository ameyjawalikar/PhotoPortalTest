import os
import datetime
import pyodbc
import textwrap
import json
from azure.storage.blob import PublicAccess
from azure.storage.blob import BlockBlobService
from processing import views
from flask import Flask
app = Flask(__name__)
@app.route('/AzureEndPoint')
def hello():
#    return "Hello World!"
# SQL Part declaration
   driver= '{ODBC Driver 17 for SQL Server}'
   server_name= 'tcp:sqlserveruat2021'
   database_name= 'TestDB'
   server= '{server_name}.database.windows.net, 1433'.format(server_name=server_name)
   #server='tcp:sqlserveruat2021.database.windows.net, 1433'
   #print(server)
   user_name='systemadmin'
   password='Test@123'
   connection_string= textwrap.dedent('''
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
   cnxn = pyodbc.connect(connection_string)
   cursor = cnxn.cursor()
   block_blob_service = BlockBlobService(account_name='testphotoprtal', account_key='cUXDLNJQI6m5lJbBa1B4LXuZPX77hLkv5D+u9Lu2iIjaAs7m798ovJU1g2bMwauRQF6xGgv9n0HxtVOjqlgqDw==')
   block_blob_service.set_container_acl('unprocessed', public_access=PublicAccess.Container)
   generator = block_blob_service.list_blobs('unprocessed')
   datetimes = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
   #FileName='Result_'+datetimes+'.txt'
   datetimes = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
   FileName = 'Result_' + datetimes + '.txt'
   f = open(FileName, "w")
   for blob in generator:
      filename=blob.name
   #   print(blob)
      block_blob_service.get_blob_to_path('unprocessed', blob.name, blob.name)
      a = views.quality_detection(filename)
      #print(a)
      res = json.loads(a)
      sql = "INSERT INTO ImageDetails (Name, quality, bluriness, darkness, brightness) VALUES (?, ?, ?, ?, ?)"
      val = (filename, res['quality'], res['bluriness'], res['darkness'], res['brightness'])
      cursor.execute(sql, val)
      cnxn.commit()
      f.write(filename +" -- "+ a + "\n")
      os.remove(blob.name)
   f.close()
   container_name ='resultfiles'
   block_blob_service.create_blob_from_path(container_name,FileName,FileName)
   os.remove(FileName)
   return ('Success Executed At: '+datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
if __name__ == '__main__':
    app.run()

