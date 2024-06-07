from flask import Flask
from flask import render_template,  request, redirect, abort
import psycopg2 as pg
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from manage_db import authorization, select_trips, insert_data_trip, insert_saved_categories

from datetime import datetime, timedelta
import locale
#locale.setlocale(locale.LC_ALL, 'ru_RU')

app = Flask(__name__) 




@app.route('/')
def hello_world():  # put application's code here
    return render_template('authorization.html')

    
    
    
    
if __name__ == "__main__": 
    app.run()

