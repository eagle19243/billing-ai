import sqlite3
import re
import string


conn = sqlite3.connect('database/db_v_2.db', check_same_thread=False)
punctuation_re = re.compile(f'[{string.punctuation}]')
