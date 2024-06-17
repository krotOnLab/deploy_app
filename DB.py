from sqlalchemy import create_engine
from sqlalchemy import Integer, String, Column, Text, JSON, UUID, Float, ForeignKey, PrimaryKeyConstraint, Boolean, ARRAY
from sqlalchemy.orm import declarative_base
# engine = create_engine("postgresql+psycopg2://postgres:hf,jnf67yt@localhost/fqw")
engine = create_engine("postgresql+psycopg2://fqw_owner:9ZtOP6dnYbKC@ep-snowy-rain-a2h4f9s6.eu-central-1.aws.neon.tech/fqw?sslmode=require")
engine.connect()
Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    login = Column(Text, primary_key=True, nullable=False)
    telegram_id_user = Column(Text, nullable=False)
    password = Column(Text, nullable=False)


class SavedCategory(Base):
    __tablename__ = 'saved_category'
    __table_args__ = (PrimaryKeyConstraint('login'),)
    login = Column(Text, ForeignKey('users.login'), nullable=False)
    saved_category = Column(JSON, nullable=False)


class Trips(Base):
    __tablename__ = 'trips'
    id_trip = Column(UUID, primary_key=True, nullable=False)
    trip = Column(JSON, nullable=False)


class UserTrips(Base):
    __tablename__ = 'user_trips'
    __table_args__ = (PrimaryKeyConstraint('id_trip'),)
    login = Column(Text, ForeignKey('users.login'), nullable=False)
    id_trip = Column(UUID, ForeignKey('trips.id_trip'), unique=True, nullable=False)


class DymanicSearchTips(Base):
    __tablename__ = 'names_cities'
    name = Column(Text, primary_key=True, nullable=False)
    region = Column(Text, primary_key=True, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    country = Column(Text, nullable=False)


class DataMeteostations(Base):
    __tablename__ = 'data_meteostations'
    index_meteostation = Column(Integer, nullable=False, primary_key=True)
    date_time = Column(String(50), nullable=False, primary_key=True)
    temperature = Column(String(10))
    Tn = Column(String(10))
    Tx = Column(String(10))


class ClimatData(Base):
    __tablename__ = 'climat_data'
    country = Column(String(20), nullable=False, primary_key=True)
    climat_data = Column(JSON, nullable=False)


class MeteostationAverageDATA(Base):
    __tablename__ = 'meteostation_average_data'
    region = Column(Text, nullable=False, primary_key=True)
    date = Column(String(10), nullable=False, primary_key=True)
    t = Column(Float)
    t_max = Column(Float)
    t_min = Column(Float)
    country = Column(String(30), nullable=False, primary_key=True)


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


