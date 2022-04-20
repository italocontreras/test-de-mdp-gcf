from google.cloud import storage as gcs
import os
import pip
import platform
import re

from datetime import datetime

from src import (
  GoogleCloudStorage,
  Email,

  HdEarthSurfaceTemperature,
  
  get_env,
  load_yml_gcf,
  load_yml_local
  
)

def main(data, context=None):
  # check version
  print('')
  print(f'python: {platform.python_version()}')#3.7.9
  print(f'pip: {pip.__version__}')#20.1.1

  try:
    print('')
    print(f'data: {data}')
    print(f'context: {context}')

    bucket = data['bucket']
    filename = data['name']
    print('')
    print(f'bucket: {bucket}')
    print(f'filename: {filename}')

    # storage

    options = {
      'earth-surface-temperature': re.compile('earth-surface-temperature/.{4}/.{8}.xlsx')
    }

    flag = False
    for option in options.values():
      if option.match(filename):
        client_gcs = gcs.Client()
        flag = True
        break

    if flag:
      blob = GoogleCloudStorage(client_gcs,bucket,filename)
    else:
      return



    print('')
    print('downloading...')
    blob.dow
    file_bytes = blob.download_to_bytesio()
    folder = filename.split('/')[0]
  
    print('')
    
    date = filename.split('/')[-1][0:8]
    date_2 = datetime.strptime(date, '%Y%m%d').date()

    if folder == 'earth-surface-temperature':
      
      earthsurfacetemperature = HdEarthSurfaceTemperature()

      earthsurfacetemperature.process(file_bytes, date_2)

    
    print('')
    print('done')
  except Exception as e:
    print('')
    print(repr(e))

    email = Email(repr(e))
    email.connect()
    email.send_message()

env = get_env()
if env == 'gcf':
  load_yml_gcf()
elif env == 'local':
  #os.system('pip list --outdated > requirements-outdated.txt')
  load_yml_local()
  
  folder = 'earth-surface-temperature'

  if folder == 'earth-surface-temperature':
    filenames = ['20220419.csv']
    for filename in filenames:
      main({
        'bucket': os.environ['BUCKET_INPUT'],
        'name': f'{folder}/{filename[0:4]}/{filename}'
      })
  
  