from sqlalchemy import create_engine
from sqlalchemy import Integer, String, Column, Text, JSON, UUID, Float, ForeignKey, PrimaryKeyConstraint, Boolean, ARRAY

from sqlalchemy.orm import relationship, declarative_base, Session
# Подключение к серверу PostgreSQL на localhost с помощью psycopg2 DBAPI
#engine = create_engine("postgresql+psycopg2://default:FleEL4jqS1nd@ep-super-feather-a2pe3ypp-pooler.eu-central-1.aws.neon.tech:5432/verceldb")
engine = create_engine("postgresql+psycopg2://user_from_app:krockodi1_yt?0K@localhost:5432/fqw")
engine.connect()

print(engine)


Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    login = Column(Text, primary_key=True, nullable=False)
    telegram_id_user = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    # trips = relationship('UserTrips', backref='user')


class SavedCategory(Base):
    __tablename__ = 'saved_category'
    __table_args__ = (
        PrimaryKeyConstraint('login'),
    )
    login = Column(Text, ForeignKey('users.login'), nullable=False)
    saved_category = Column(JSON, nullable=False)
    # user = relationship('users', backref='saved_category')


class Trips(Base):
    __tablename__ = 'trips'
    id_trip = Column(UUID, primary_key=True, nullable=False)
    trip = Column(JSON, nullable=False)
    # user = relationship('UserTrips', backref='trip')


class UserTrips(Base):
    __tablename__ = 'user_trips'
    __table_args__ = (
        PrimaryKeyConstraint('id_trip'),
    )
    login = Column(Text, ForeignKey('users.login'), nullable=False)
    id_trip = Column(UUID, ForeignKey('trips.id_trip'), unique=True, nullable=False)


class DataMeteostationsChina(Base):
    __tablename__ = 'data_meteostations_china'
    index_meteostation = Column(Integer, nullable=False, primary_key=True)
    date_time = Column(String(50), nullable=False)
    temperature = Column(String(10))
    P0 = Column(String(10))
    Pressure = Column(String(10))
    Pa = Column(String(10))
    U = Column(String(10))
    DD = Column(Text)
    Ff = Column(Text)
    ff10 = Column(String(10))
    ff3 = Column(String(10))
    N = Column(Text)
    WW = Column(Text)
    W1 = Column(Text)
    W2 = Column(Text)
    Tn = Column(String(10))
    Tx = Column(String(10))
    Cl = Column(Text)
    Nh = Column(Text)
    H = Column(String(50))
    Cm = Column(Text)
    Ch = Column(Text)
    VV = Column(String(20))
    Td = Column(String(10))
    RRR = Column(Text)
    tR = Column(String(10))
    E = Column(Text)
    Tg = Column(String(10))
    Es = Column(Text)
    sss = Column(String(10))


class InfoTrip(Base):
    __tablename__ = 'info_trip'
    chapter = Column(Text, nullable=False, primary_key=True)
    section = Column(Text, nullable=False, primary_key=True)
    name_en = Column(Text, nullable=False)
    name_ru = Column(Text, nullable=False)
    status = Column(Boolean, nullable=False)
    data = Column(ARRAY(String), nullable=False)


class MeteostationInfo(Base):
    __tablename__ = 'meteostation_info'
    index_meteostation = Column(Integer, primary_key=True, nullable=False)
    name_meteostation = Column(Text, nullable=False)
    lattitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    HSL = Column(Integer, nullable=False)
    country = Column(Text, nullable=False)


Base.metadata.create_all(engine)

engine.dispose()


