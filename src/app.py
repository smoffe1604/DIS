import psycopg2
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import glob
import pandas as pd
import random

app = Flask(__name__ , static_url_path='/static')

# set your own database name, username and password
db = "dbname='postgres' user='simonpallesen' host='localhost' password=''"
conn = psycopg2.connect(db)
cursor = conn.cursor()