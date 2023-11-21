from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

SESSION_PERMANENT = False
SESSION_TYPE = 'filesystem'

MAX_CONTENT_LENGTH = 1_048_576 * 1_048_576
UPLOAD_EXTENSIONS = ['.mp4', '.mov', '.mp3', '.mkv']
UPLOAD_PATH = 'static//uploads'

SQLALCHEMY_DATABASE_URI = \
    f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
SQLALCHEMY_TRACK_MODIFICATIONS= False

PFP_PATH = 'images/pfps/'
VIDEOS_PATH = 'videos/'

PIPELINE_ID = '1700512479814-8qgmq1'
