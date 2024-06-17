import requests
from flask import Flask, Response, make_response
from flask import render_template,  request, jsonify
from manage_db import *
from datetime import datetime, timedelta
# import locale
# locale.setlocale(locale.LC_ALL, 'ru_RU')

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True



global CURRENT_USER
global CURRENT_TRIP
global BASE_PARAMS


def calc_period (dates, status_trip, status=''):
    if type(dates) == str:
        dates = dates.split(',')
    # if status_trip == 'new':
    #     dates = dates.split(',')
    dates = [i.split('.') for i in dates]
    start_date = datetime(int(dates[0][2]), int(dates[0][1]), int(dates[0][0]))
    end_date = datetime(int(dates[1][2]), int(dates[1][1]), int(dates[1][0]))
    current_date = start_date
    date_list = []
    while current_date <= end_date:
        if status == 'meteo_data':
            formatted_date = current_date.strftime('%m-%d')
            date_list.append(formatted_date)
        else:
            formatted_date = current_date.strftime('%d - %B - %A')
            date_list.append({"day": formatted_date.split(' - ')[0],
                              "month": formatted_date.split(' - ')[1], "day_week":formatted_date.split(' - ')[2]})
        current_date += timedelta(days=1)
    return date_list


def check_country_distination(country, data, status_trip):
    global CURRENT_USER
    global BASE_PARAMS
    categories = get_saved_categories_user(CURRENT_USER)
    # print(categories)
    # categories = categories[0]['saved_categories']
    if country == 'Китай':
        climat = get_climat_data(country)
        if status_trip == 'new':
            print('new')
            if len(BASE_PARAMS['dates']) != 0:
                per = calc_period(BASE_PARAMS['dates'], status_trip='new')
                weather = get_meteo_data_from_DB(calc_period(BASE_PARAMS['dates'], status_trip='new',
                                                             status='meteo_data'), per,
                                                 BASE_PARAMS['location'].split(', ')[1], country)
            else:
                per = 0
                weather = []
            return render_template('trip.html', data=data['data'], period=per, weather=weather, data_climat=climat,
                                   status_weather='true', categories=categories, location=data['location'], status='save')
        elif status_trip == 'old':
            print('old')
            per = calc_period(data['base_params']['dates'], '')
            weather = get_meteo_data_from_DB(calc_period(data['base_params']['dates'], status_trip='old',
                                                         status='meteo_data'), per,
                                             data['base_params']['location'].split(', ')[1], country)
            # params = {'data_trip': eval(data['trip_data']),
            #           'period': eval(data['calendar_data']),
            #           'weather': weather,
            #           'data_climat': climat,
            #           'status_weather': 'true',
            #           'categories': categories,
            #           'location': data['base_params']['location'],
            #           'status': 'edit'
            # }
            # print(type(data['trip_data']))
            # print(isinstance(data['trip_data'], dict))
            # print(not(isinstance(data['trip_data'], dict)))
            if not(isinstance(data['trip_data'], dict)):
                data['trip_data'] = eval(data['trip_data'])
            if not(isinstance(data['calendar_data'], list)):
                data['calendar_data'] = eval(data['calendar_data'])
            # return render_template('trip_existing.html', params)
            return render_template('trip_existing.html', data_trip=data['trip_data'],
                                   period=data['calendar_data'], weather=weather, data_climat=climat,
                                   status_weather='true', status='edit', categories=categories,
                                   location=data['base_params']['location'])
    #         return render_template('trip_existing.html', data_trip=eval(data['trip_data']),
    #                                period=eval(data['calendar_data']),
    #                                weather=weather, data_climat=climat, status_weather='true', categories=categories,
    #                                location=data['base_params']['location'], status='edit')
    # else:
        if status_trip == 'new':
            if len(BASE_PARAMS['dates']) != 0:
                per = calc_period(BASE_PARAMS['dates'], status_trip='new')
            else:
                per = []
            return render_template('trip.html', data=data, period=per,  categories=categories, status='save')
        elif status_trip == 'old':
            return render_template('trip_existing.html', data_trip=data['trip_data'], period=data['calendar_data'],
                                   status_weather='true', categories=categories, status='edit')


def check_name(name):
    if len(name) >= 3:
        data = get_data_for_check()
        print(name)
        name = name.split(', ')
        for item in data:
            # print(item)
            if (name[0] == item[0]) and (name[1] == item[1]) and (name[2] == item[2]):
                return True
        return False
    else:
        return False



@app.route('/')
def hello_world():
    return render_template('authorization.html')


@app.route('/load_lk', methods=['post', 'get'])
def load_lk():
    global CURRENT_USER
    print(CURRENT_USER)
    trips = select_trips(CURRENT_USER)
    return render_template('lk.html', trips=trips, number_trips=len(trips))


@app.route('/edit_list_categories', methods=['post', 'get'])
def edit_list_categories():
    categories = request.json
    print(categories)
    return render_template('settings.html', business='', vacation='', status='', month='',
                           list_categories=categories['categories'])


def enter_lk(login):
    trips = select_trips(login)
    return render_template('lk.html', trips=trips, number_trips=len(trips))  # render lk


@app.route('/submit_auth', methods=['post', 'get'])
def main_page():
    global CURRENT_USER
    login = request.form.get('username').replace(" ", "").replace("\t", "")
    password = request.form.get('password').replace(" ", "").replace("\t", "")
    if authorization(app, login, password):
        CURRENT_USER = login
        return enter_lk(login)
    else:
        return render_template('authorization.html', answer=False)


@app.route('/delete_trip', methods=['post', 'get'])
def del_trip():
    global CURRENT_USER
    data = request.json
    print(request.json)
    # print(id_trip)
    # return True
    delete_trip_from_user(CURRENT_USER, data['id_trip'])
    return enter_lk(CURRENT_USER)


@app.route('/search')
def search():

    query = request.args.get('q')
    data = get_data_for_seacrh(query.lower())
    results = []
    # print(data)
    return jsonify(data)
    # for item in data:
    #     s = item['name'].lower() + ' ' + item['region'].lower() + ' ' + item['country']
    #     # if query.lower() in item['name'].lower():
    #     if query.lower() in s:
    #         results.append(f"{item['name']}, {item['region']}, {item['country']}")
    # return jsonify(results)


@app.route('/new_trip', methods=['post', 'get'])
def new_trip():
    return render_template('base_settings.html', data={'trip_name': '', 'busines': '', 'vacation': '', 'dates': ''},
                           alert='false')


@app.route('/settings', methods=['post', 'get'])
def base_settings():
    global BASE_PARAMS
    BASE_PARAMS = request.form.to_dict()
    if type(BASE_PARAMS['dates']) == str:
        BASE_PARAMS['dates'] = BASE_PARAMS['dates'].split(',')
    print(BASE_PARAMS)
    if not check_name(BASE_PARAMS['location']):
        return render_template('base_settings.html', data=BASE_PARAMS, alert='true')
    else:
        if BASE_PARAMS['location'].split(', ')[2] == 'Китай':
            return render_template('settings.html', business=BASE_PARAMS['business'], vacation=BASE_PARAMS['vacation'],
                                   status='china',
                                   month=calc_period(BASE_PARAMS['dates'], status_trip='new')[0]['month'])
        else:
            return render_template('settings.html', business=BASE_PARAMS['business'], vacation=BASE_PARAMS['vacation'],
                                   month=calc_period(BASE_PARAMS['dates'], status_trip='new')[0]['month'])


@app.route('/trip', methods=['post', 'get'])
def settings():
    global BASE_PARAMS
    categories = request.form.to_dict()
    data = eval(categories['data'])
    data = {k: ('true' if v == 'true' else 'false') for (k, v) in data.items()}
    data = [k for (k, v) in data.items() if v == 'true']
    data = {'data': ','.join(data), 'location': BASE_PARAMS['location']}
    return check_country_distination(BASE_PARAMS['location'].split(', ')[2], data, 'new')


def save_t(data):
    global BASE_PARAMS
    global CURRENT_USER
    print(base_params)
    # base_params['dates'] = base_params['dates'].split(',')
    data["base_params"] = BASE_PARAMS
    data['trip_data'] = eval(data['trip_data'].replace('false', 'False').replace('true', 'True'))
    data['calendar_data'] = eval(data['calendar_data'])
    saved_categories = eval(data['saved_categories'].replace('false', 'False').replace('true', 'True'))
    insert_data_trip(login_user, {'trip_data': data['trip_data'], 'calendar_data': data['calendar_data'],
                                  'base_params': data['base_params']})
    if saved_categories:
        insert_saved_categories(CURRENT_USER, saved_categories)


@app.route('/save_trip', methods=['post', 'get'])
def get_data_to_save():
    data = request.form.to_dict()
    print('save in app')
    print(data)
    if data:
        return save_data(data)
    else:
        data = request.json
        print(data)
        if data:
            save_t(data)
            return make_response("OK", 200)
        else:
            save_t({})
            return make_response("OK", 200)

def save_data(data):
    # base_params['dates'] = base_params['dates'].split(',')

    print(base_params['dates'])
    print(data)
    global BASE_PARAMS
    global CURRENT_USER
    if BASE_PARAMS:
        data["base_params"] = BASE_PARAMS
    data['trip_data'] = eval(data['trip_data'].replace('false', 'False').replace('true', 'True'))
    data['calendar_data'] = eval(data['calendar_data'])
    saved_categories = eval(data['saved_categories'].replace('false', 'False').replace('true', 'True'))
    insert_data_trip(login_user, {'trip_data': data['trip_data'], 'calendar_data': data['calendar_data'], 'base_params': data['base_params']})
    print(saved_categories)
    if saved_categories:
        insert_saved_categories(CURRENT_USER, saved_categories)
    return check_country_distination(data['base_params']['location'].split(', ')[2], data, 'old')


@app.route('/edit_trip', methods=['post', 'get'])
def edit_trip():

    def save_data_trip(data):
        # print(uuid_selected_trip)
        if 'uuid_selected_trip' in globals():
            global CURRENT_TRIP
            print('uuid')
            if CURRENT_TRIP:
                global CURRENT_USER
                data_old = select_trip(CURRENT_TRIP)
                print(data)
                print(data_old)
                data_old = data_old[0]
                data_old['trip_data'] = data['trip_data'].replace('false', 'False').replace('true', 'True')
                data_old['calendar_data'] = data['calendar_data']
                saved_categories = data['saved_categories'].replace('false', 'False').replace('true', 'True')
                edit_data_trip(CURRENT_TRIP, {'trip_data': data_old['trip_data'], 'calendar_data': data_old['calendar_data'],
                                          'base_params': data_old['base_params']})
                if saved_categories:
                    insert_saved_categories(CURRENT_USER, saved_categories)
                return data_old

        else:
            if 'base_params' in globals():
                print('base_params')
                save_t(data)

            # insert_data_trip(login_user, {'trip_data': data_old['trip_data'], 'calendar_data': data_old['calendar_data'],
            #                           'base_params': data_old['base_params']})

    data = request.form.to_dict()
    if data:
        data = save_data_trip(data)
        return check_country_distination(data['base_params']['location'].split(', ')[2], data, 'old')
    else:
        data = request.json
        if data:
            save_data_trip(data)
            return load_lk()
    # data_old = select_trip(uuid_selected_trip)
    # print(data)
    # print(eval(data))
    # data_old['trip_data'] = eval(data['trip_data'].replace('false', 'False').replace('true', 'True'))
    # data_old['calendar_data'] = eval(data['calendar_data'])
    # saved_categories = eval(data['saved_categories'].replace('false', 'False').replace('true', 'True'))
    # insert_data_trip(login_user, {'trip_data': data_old['trip_data'], 'calendar_data': data_old['calendar_data'],
    #                               'base_params': data_old['base_params']})
    # insert_saved_categories(login_user, saved_categories)



@app.route('/load_trip', methods=['post', 'get'])
def load_trip():
    select_trip = request.form.to_dict()
    select_trip = eval(select_trip['params_trip'])
    # print(select_trip)
    # print(select_trip['uuid'])
    global CURRENT_TRIP
    global CURRENT_USER
    CURRENT_TRIP = select_trip['uuid']
    trips = select_trips(CURRENT_USER)
    for trip in trips:
        if str(trip[1]) == uuid_selected_trip:
            print(trip[0])
            return check_country_distination(trip[0]['base_params']['location'].split(', ')[2], trip[0], 'old')


if __name__ == '__main__':
    app.run(debug=True)
