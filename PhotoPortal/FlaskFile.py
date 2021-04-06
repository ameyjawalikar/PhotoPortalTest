import os
import datetime
from azure.storage.blob import PublicAccess
from azure.storage.blob import BlockBlobService
from processing import views
from flask import Flask
app = Flask(__name__)
@app.route('/AzureEndPoint2')
def hello():
#    return "Hello World!"

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
      print(a)
      f.write(filename +" -- "+ a + "\n")
      os.remove(blob.name)
   f.close()
   container_name ='processed'
   block_blob_service.create_blob_from_path(container_name,FileName,FileName)
   os.remove(FileName)
   return ('Success Executed At: '+datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
   #return 'Success'
if __name__ == '__main__':
    app.run()
