
import os

CONFIG = {
    'DB_TYPE': os.environ.get('DB_TYPE'),
    'DB_ADR': os.environ.get('DB_ADR'),
    'DB_NAME': os.environ.get('DB_NAME'),
    'DB_USER': os.environ.get('DB_USER'),
    'DB_PASS': os.environ.get('DB_PASS'),
}
