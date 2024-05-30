from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker, relationship, declarative_base
from sqlalchemy import Integer, String, Column, Text, JSON, UUID, Float, ForeignKey, PrimaryKeyConstraint
from DB import Users, Trips, UserTrips, InfoTrip, SavedCategory
import uuid
import pandas as pd


from flask_bcrypt import Bcrypt





# Подключение к серверу PostgreSQL на localhost с помощью psycopg2
try:
    #engine = create_engine("postgresql+psycopg2://default:FleEL4jqS1nd@ep-super-feather-a2pe3ypp-pooler.eu-central-1.aws.neon.tech:5432/verceldb")
    engine = create_engine("postgresql+psycopg2://user_from_app:krockodi1_yt?0K@localhost:5432/fqw")
    engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    
    
    res = session.query(InfoTrip).all
    session.commit()
    print(res)
    print(1)


    def newUser(app, login, telegram_id, password):
        bcrypt = Bcrypt(app)
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = Users(
                login=login,
                telegram_id_user=telegram_id,
                password=hashed_password
            )
        session.add(new_user)
        session.commit()

    # def newUserV(login, password):
    #     bcrypt = Bcrypt()
    #     hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    #     new_user = Users(login=login, telegram_id_user='',
    #                      password=hashed_password)
    #     session.add(new_user)
    #     session.commit()


    def authorization(app, login, password):
        bcrypt = Bcrypt(app)
        user = session.query(Users.login, Users.password).filter(Users.login == login).first()
        session.commit()
        print(user)
        print(user[1])
        result = bcrypt.check_password_hash(user[1], password)
        print(f'enter pas:{password}, hash_pas_in_db:{user[1]}, result:{bcrypt.generate_password_hash(password).decode("utf-8")}')
        return result


    def select_trips(login):
        data = session.query(Trips.trip).join(UserTrips).filter(UserTrips.login == login).all()
        # data = session.execute(text("SELECT trip FROM trips INNER JOIN user_trips ON trips.id_trip = user_trips.id_trip WHERE login=:login"), {'login': login}).all()
        session.commit()
        print(f'data from trip: {data}')
        return data


    def insert_data_trip(login, data):
        id_trip = uuid.uuid4()
        user_trip = UserTrips(login=login, id_trip=id_trip)
        trip = Trips(id_trip=id_trip, trip=data)
        session.add(user_trip)
        session.add(trip)
        session.commit()


    def insert_saved_categories(login, data):
        session.add(SavedCategory(login=login, saved_category=data))
        session.commit()


    def get_all_trips(telegram_id):
        login = session.query(Users.login).filter(Users.telegram_id_user == telegram_id).first()
        # login = session.execute(text("SELECT login FROM users WHERE telegram_id_user=:telegram_id_user"), {'telegram_id_user':telegram_id}).first()
        session.commit()
        data_trips = select_trips(login)
        print(f'data from trip: {data_trips}')
        return data_trips

    # newUserV('123', 'new_pas')
except Exception as e:
    print(e)
    session.close()
    engine.dispose()


# Base = declarative_base()
# class Users(Base):
#     __tablename__ = 'users'
#     login = Column(Text, primary_key=True, nullable=False)
#     telegram_id_user = Column(Text, primary_key=True, nullable=False)
#     password = Column(Text, nullable=False)
#     trips = relationship('UserTrips', backref='user')
