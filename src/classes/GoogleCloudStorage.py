from google.cloud import storage
from io import BytesIO

class GoogleCloudStorage:
  def __init__(
    self,
    client: storage.Client,
    bucket: str,
    blob: str
  ):
    self.__client = client
    self.__bucket = self.__client.bucket(bucket)
    self.__blob = self.__bucket.blob(blob)

  def exists(self):
    return self.__blob.exists()

  def download_to_bytes(self):
    try:
      return self.__blob.download_as_string()
    except Exception as e:
      print('error:',repr(e))
      return False

  def download_to_bytesio(self):
    try:
      return BytesIO(self.download_to_bytes())
    except Exception as e:
      print('error:',repr(e))
      return False

  def download_to_filename(self,path):
    self.__blob.download_to_filename(path)
    return True

  def upload_from_filename(self,path):
    self.__blob.upload_from_filename(path)
    return True

  def upload_from_string(self):
    try:
      return self.__blob.upload_from_string()
    except Exception as e:
      print('error:',repr(e))
      return False

  def upload_from_stringio(self):
    try:
      return BytesIO(self.upload_from_string())
    except Exception as e:
      print('error:',repr(e))
      return False  