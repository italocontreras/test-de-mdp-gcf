from google.cloud import storage as gcs
from base64 import b64decode,b64encode
import copy as cp
from datetime import date,datetime as dt,timedelta
from dateutil import tz
from google.cloud import secretmanager
from io import BytesIO
import json
import locale
import os
import yaml as yml
from zipfile import ZipFile as zf
import chardet
import xlrd

def download_gcsql():
  os.system(f'mkdir -p /tmp/{os.environ["DB_DATA_CERTS_PATH"]}')

  client_gcs = gcs.Client()
  
  bucket = client_gcs.bucket(os.environ['DB_DATA_CERTS_BUCKET'])
  
  blob = bucket.blob(os.environ['DB_DATA_SSL_SERVER_CA'])
  blob.download_to_filename(f'/tmp/{os.environ["DB_DATA_SSL_SERVER_CA"]}')
  
  blob = bucket.blob(os.environ['DB_DATA_SSL_CLIENT_CERT'])
  blob.download_to_filename(f'/tmp/{os.environ["DB_DATA_SSL_CLIENT_CERT"]}')

  blob = bucket.blob(os.environ['DB_DATA_SSL_CLIENT_KEY'])
  blob.download_to_filename(f'/tmp/{os.environ["DB_DATA_SSL_CLIENT_KEY"]}')

  os.system(f'chmod -R 0700 /tmp/{os.environ["DB_DATA_CERTS_PATH"]}')

def add_days(date,days):
  result = date + timedelta(days=days)
  return result

def cast_date_to_YYYYMMDD(date):
  date = str(date)[:10].replace('-','')
  return date

def cast_YYYYMMDD_to_date(date):
  date = dt.strptime(date,'%Y%m%d').date()
  return date

def change_utc_to_tz(date,timezone):
  from_zone = tz.gettz('UTC')
  to_zone = tz.gettz(timezone)

  date = date.replace(tzinfo=from_zone)
  return date.astimezone(to_zone)

def get_all_sundays_of_year(year):
  d = date(year,1,1)
  d += timedelta(days=6-d.weekday())
  while d.year == year:
    yield d
    d += timedelta(days=7)

def get_days_between_two_dates(begin_date,end_date):
  days = []
  delta = end_date - begin_date
  for i in range(delta.days + 1):
    day = begin_date + timedelta(days=i)
    days.append(day)

  return days

def get_env():
  env = os.environ['PYTHON_ENV']
  return env

def get_env_var(env):
  if env == 'gcf':
    env_var = {
      'TIMEZONE': os.environ['TIMEZONE'],

      'DB_DATA_HOST': os.environ['DB_DATA_HOST'],
      'DB_DATA_PORT': int(os.environ['DB_DATA_PORT']),
      'DB_DATA_USER': os.environ['DB_DATA_USER'],
      'DB_DATA_PASS': os.environ['DB_DATA_PASS'],
      'DB_DATA_NAME': os.environ['DB_DATA_NAME'],

      'DB_LOG_HOST': os.environ['DB_LOG_HOST'],
      'DB_LOG_PORT': int(os.environ['DB_LOG_PORT']),
      'DB_LOG_USER': os.environ['DB_LOG_USER'],
      'DB_LOG_PASS': os.environ['DB_LOG_PASS'],
      'DB_LOG_NAME': os.environ['DB_LOG_NAME']
    }
  elif env == 'local':
    with open(f'{env}/.env.yml') as f:
      env_var = yml.full_load(stream=f)

  return env_var

def get_lines_from_binary_file(binary_file):
  binary_file = cp.deepcopy(binary_file)
  lines = len(list(filter(lambda x: x.strip(),binary_file)))
  return lines

def get_now_utc():
  now = dt.utcnow()
  return now

def get_now_YYYYMMDD():
  date = get_now('%Y-%m-%d')
  YYYYMMDD = cast_date_to_YYYYMMDD(date)
  return YYYYMMDD

def get_now(format):
  return dt.now().strftime(format)

def get_today_tz(timezone):
  to_zone = tz.gettz(timezone)
  today = dt.now(to_zone).date()
  return today

def get_today_utc():
  today = dt.utcnow().date()
  return today

def is_base64(string):
  try:
    if type(string) is str:
      string = string.encode('utf-8')
    elif type(string) is not bytes:
      pass
    else:
      raise Exception('Argument must be string or bytes')
    return b64encode(b64decode(string)) == string
  except Exception as e:
    print('error:',repr(e))
    return False

def load_yml_gcf():
  client = secretmanager.SecretManagerServiceClient()
  name = f"projects/{os.environ['SECRET_PROJECT']}/secrets/{os.environ['SECRET_SERVICE']}/versions/{os.environ['SECRET_VERSION']}"
  response = client.access_secret_version(request={'name':name})
  payload = response.payload.data.decode('utf-8')

  env_vars = yml.full_load(stream=payload)
  for k in env_vars:
    os.environ[k] = str(env_vars[k])

def load_yml_local():
  with open('local/.env.yml') as f:
    env_vars = yml.full_load(stream=f)
    for k in env_vars:
      os.environ[k] = str(env_vars[k])

def set_LC_TIME(value):
  locale.setlocale(locale.LC_TIME,value)

def set_TZ(value):
  os.environ['TZ'] = value

def unzip_file_in_binaries(file):
  content = zf(file)
  files = []
  for f in content.namelist():
    file = BytesIO(content.open(f,'r').read())
    files.append(file)
  return files

def get_file_encoding(filename):
  with open(filename, 'rb') as rawdata:
    result = chardet.detect(rawdata.read(10000))
  return result['encoding']

def substract_days(date, days):
  result = date - timedelta(days=days)
  return result

def seriedate_to_stringdate(serie_date):

  datetime_date = xlrd.xldate_as_datetime(int(serie_date), 0)
  date_object = datetime_date.date()
  string_date = date_object.isoformat()
  
  return string_date
