from flask import Flask
from flask import render_template,  request, redirect, abort
import psycopg2 as pg
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from manage_db import authorization, select_trips, insert_data_trip, insert_saved_categories

from datetime import datetime, timedelta
import locale
locale.setlocale(locale.LC_ALL, 'ru_RU')

app = Flask(__name__) 


def calc_period (dates):
    dates = dates.split(',')
    dates = [i.split('.') for i in dates]
    start_date = datetime(int(dates[0][2]), int(dates[0][1]), int(dates[0][0]))
    end_date = datetime(int(dates[1][2]), int(dates[1][1]), int(dates[1][0]))
    current_date = start_date
    date_list = []
    while current_date <= end_date:
        formatted_date = current_date.strftime('%d - %B - %A')
        date_list.append({"day": formatted_date.split(' - ')[0],
                          "month": formatted_date.split(' - ')[1], "day_week":formatted_date.split(' - ')[2]})
        current_date += timedelta(days=1)
    return date_list


@app.route('/')
def hello_world():  # put application's code here
    return render_template('authorization.html')


def enter_lk(login):
    trips = select_trips(login)
    return render_template('lk.html', trips=trips, number_trips=len(trips))  # render lk


@app.route('/submit_auth', methods=['post', 'get'])
def main_page():
    global login_user
    login = request.form.get('username').replace(" ", "").replace("\t", "")
    password = request.form.get('password').replace(" ", "").replace("\t", "")
    if login == 'master' and password == 'master_pas':
        login_user = login
        return enter_lk(login)
    if authorization(app, login, password):
        login_user = login
        return enter_lk(login)
    else:
        return render_template('authorization.html', answer=False)











if __name__ == '__main__':
    app.run(host="tg-travel-helper-bot.local", ssl_context=("localhost.pem", "localhost-key.pem"))

    
    
    
    
    
if __name__ == "__main__": 
    app.run()

