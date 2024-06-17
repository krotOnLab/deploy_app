import json

from sqlalchemy import update, URL, create_engine, insert, text, or_, func
from sqlalchemy.orm import sessionmaker
from DB import Users, Trips, UserTrips, SavedCategory, ClimatData, DymanicSearchTips, MeteostationAverageDATA
import uuid
from flask_bcrypt import Bcrypt

try:
    # connection_string = URL.create(
    #     'postgresql',
    #     username='fqw_owner',
    #     password='9ZtOP6dnYbKC',
    #     host='ep-snowy-rain-a2h4f9s6.eu-central-1.aws.neon.tech',
    #     database='fqw',
    #     connect_args={'sslmode': 'require'}
    # )

    # engine = create_engine(connection_string)
    # psql
    # "postgres://default:FleEL4jqS1nd@ep-super-feather-a2pe3ypp.eu-central-1.aws.neon.tech:5432/verceldb?sslmode=require"
    # engine = create_engine("postgresql+psycopg2://postgres:hf,jnf67yt@localhost/fqw")
    # engine = create_engine("postgresql+psycopg2://default:FleEL4jqS1nd@ep-super-feather-a2pe3ypp.eu-central-1.aws.neon.tech:5432/verceldb?sslmode=require")
    engine = create_engine(
        "postgresql+psycopg2://fqw_owner:9ZtOP6dnYbKC@ep-snowy-rain-a2h4f9s6.eu-central-1.aws.neon.tech/fqw?sslmode=require"
    )
    engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # session.execute(text("SET lc_collate = 'C'"))
    # session.commit()


    def newUser(app, login, telegram_id, password):
        bcrypt = Bcrypt(app)
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = Users(
                login=login,
                telegram_id_user=telegram_id,
                password=hashed_password
            )
        session.add(new_user)
        session.flush()


    def authorization(app, login, password):
        bcrypt = Bcrypt(app)
        user = session.query(Users.login, Users.password).filter(Users.login == login).first()
        # session.flush()
        result = bcrypt.check_password_hash(user[1], password)
        return result


    def select_trips(login):
        data = session.query(Trips.trip, Trips.id_trip).join(UserTrips).filter(UserTrips.login == login).all()
        print(data)
        # session.flush()
        return data

    def select_trip(uuid):
        print(type(uuid))
        print(uuid)
        data = session.query(Trips.trip).filter(Trips.id_trip==uuid).first()
        # session.flush()
        print(data)
        print('end')
        return data

    def edit_data_trip(uuid, data):
        # trip = session.query(Trips).filter(Trips.id_trip==uuid).update(Trips.trip==data)
        session.execute(text(f"""INSERT INTO trips (id_trip, trip) 
                                        VALUES ('{uuid}', '{json.dumps(data, ensure_ascii=False).replace('False', 'fls')}') 
                     ON CONFLICT (id_trip) DO UPDATE SET trip='{json.dumps(data, ensure_ascii=False).replace('False', 'fls')}'"""))

        session.commit()

    def insert_data_trip(login, data):
        id_trip = uuid.uuid4()
        print('save trip')
        user_trip = UserTrips(login=login, id_trip=id_trip)
        trip = Trips(id_trip=id_trip, trip=data)
        session.add(user_trip)
        session.add(trip)
        session.commit()


    def insert_saved_categories(login, data):

        # stmt = insert(SavedCategory).values({'login': login, 'saved_category': {'saved_categories': data}})
        # stmt = stmt.onconflict_do_update(
        #     index_elements=['login'],
        #     set_={'saved_category': data}
        # )
        # json.dumps()
        prepare_data = {"saved_categories": data}
        prepare_data = json.dumps(prepare_data, ensure_ascii=False).replace('True', "true").replace('False', "false")
        print(prepare_data)
        # str(prepare_data).replace("'", '"').replace('True', 'true')
        session.execute(text(f"""INSERT INTO saved_category (login, saved_category) 
                                VALUES ('{login}', '{prepare_data}') 
             ON CONFLICT (login) DO UPDATE SET saved_category='{prepare_data}'"""))
        session.commit()

        # session.query(SavedCategory).filter(SavedCategory.login==login)
        # session.execute(update(SavedCategory).where(SavedCategory.login==login, {'saved_categories': data }))
        # session.commit()


    def get_all_trips(telegram_id):
        # s = session.query(DymanicSearchTips).update({DymanicSearchTips.name: func.replace(DymanicSearchTips.name,
        #                                                                                   ", ", ",")},
        #                                             synchronize_session='fetch')
        login = session.query(Users.login).filter(Users.telegram_id_user == telegram_id).first()
        # session.flush()
        data_trips = select_trips(login)
        return data_trips


    def get_meteo_data_from_DB(dates_search, dates, region, country):
        print(dates_search, dates, region, country)
        average_data = session.query(MeteostationAverageDATA.t_max, MeteostationAverageDATA.t_min).filter(
            MeteostationAverageDATA.date.in_(dates_search), MeteostationAverageDATA.region==region,
            MeteostationAverageDATA.country==country
        ).all()
        session.commit()
        print('average')
        print(average_data)
        # average_data = session.query(DataMeteostationsChinaAverage.t_max,
        #                              DataMeteostationsChinaAverage.t_min).filter(DataMeteostationsChinaAverage.date.in_(dates_search)).all()
        # session.flush()
        return [(dates[i], int(item[0]), int(item[1])) for i, item in enumerate(average_data)]


    def get_climat_data(country):
        climat = session.query(ClimatData.climat_data).filter(ClimatData.country == f'{country}').first()
        # session.flush()
        return eval(climat[0])

    def get_data_for_check():
        data = session.query(DymanicSearchTips.name, DymanicSearchTips.region, DymanicSearchTips.country).all()
        # session.flush()
        return data

    def get_data_for_seacrh(query_s):

        # print(query_s)
        data = session.query(DymanicSearchTips.name, DymanicSearchTips.region, DymanicSearchTips.country).filter(or_(
            DymanicSearchTips.name.ilike(f'%{query_s}'), DymanicSearchTips.region.ilike(f'%{query_s}'),
            DymanicSearchTips.country.ilike(f'%{query_s}'))).order_by(DymanicSearchTips.name).limit(5)
        # print(data)
        # session.flush()
        # temp = [{'name': item[0], 'region': item[1], 'country': item[2]} for item in data]
        temp = [', '.join(item) for item in data]
        return temp


    def get_saved_categories_user(login):
        categories = session.query(SavedCategory.saved_category).filter(SavedCategory.login==login).first()
        # session.flush()
        if categories is None:
            return {}
        else:
            print(categories)
            try:
                categories = eval(categories[0]['saved_categories'])
                return eval(categories[0]['saved_categories'])
            except Exception as e:
                print(e)
                return categories[0]['saved_categories']
            # print(eval(categories[0]['saved_categories']))


    def delete_trip_from_user(login, id_trip):
        session.query(UserTrips).filter(UserTrips.login==login, UserTrips.id_trip==id_trip).delete()
        session.query(Trips).filter(Trips.id_trip==id_trip).delete()
        print(f'delete trip{id_trip}')
        session.commit()



except Exception as e:
    print(e)
    session.close()
    engine.dispose()
finally:
    # session.commit()
    session.close()
    engine.dispose()