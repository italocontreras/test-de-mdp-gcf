from datetime import datetime
from . import Database
import pandas as pd
import numpy as np
import xlrd
from io import StringIO
pd.options.mode.chained_assignment = None

from ..utils import (
  seriedate_to_stringdate
)

class HdEarthSurfaceTemperature():  
  def __init__(self):
    super().__init__()

  def process(self, file_bytes,date_2):

    try:

      #read input csv in bucket
      df_input = pd.read_csv(file_bytes)
      df_input.insert(0,'day_id', date_2)
      
      df_input = df_input.applymap(lambda s: s.upper() if type(s) == str else s)
      
      #put csvs outputs in buckets
      countries = df_input['Country'].unique()
      
      for country in countries:
        df_output =  df_input[df_input["Country"] == country]
        
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(os.environ['BUCKET_OUTPUT'])
        blob.upload_from_string(data=df_output)
        

    except Exception as e:
      print('error:',repr(e))
      raise e
    
    
    