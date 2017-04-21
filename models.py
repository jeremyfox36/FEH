from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import BigInteger, Boolean, Column, Date, Float, Integer, String, Table, Text, text
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

from FEH import app
from FEH import config

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://jem:secret@localhost:5432/feh1'
app.debug = True
db = SQLAlchemy(app)


def db_connect():
    """
        Performs database connection using database settings from settings.py.
        Returns sqlalchemy engine instance
    """
    return create_engine(URL(**config.DATABASE))

# coding: utf-8
Base = declarative_base()
metadata = Base.metadata


class AmDetail(Base):
    __tablename__ = 'am_details'

    stationnum = Column(Integer, primary_key=True)
    yeartype = Column(String)
    wateryear = Column(String)
    amrejected = Column(String)


t_amaxdata = Table(
    'amaxdata', metadata,
    Column('stationnum', Integer),
    Column('mon_date', Date),
    Column('flow', Float)
)


class Cd3Datum(Base):
    __tablename__ = 'cd3_data'

    stationnum = Column(Integer, primary_key=True)
    ver = Column(Float)
    stname = Column(String)
    loc = Column(String)
    nomarea = Column(Float)
    nomngre = Column(Integer)
    nomngrn = Column(Integer)
    ihdtmngre = Column(Integer)
    ihdtmngrn = Column(Integer)
    centroidngre = Column(Integer)
    centroidngrn = Column(Integer)
    dtmarea = Column(Float)
    altbar = Column(Integer)
    aspbar = Column(Integer)
    aspvar = Column(Float)
    bfihost = Column(Float)
    dplbar = Column(Float)
    dpsbar = Column(Float)
    farl = Column(Float)
    fpext = Column(Float)
    ldp = Column(Float)
    propwet = Column(Float)
    rmed1h = Column(Float)
    rmed1d = Column(Float)
    rmed2d = Column(Float)
    saar = Column(Integer)
    saar_1470 = Column(Integer)
    sprhost = Column(Float)
    urbconc1990 = Column(Float)
    urbext1990 = Column(Float)
    urbloc1990 = Column(Float)
    urbconc2000 = Column(Float)
    urbext2000 = Column(Float)
    urbloc2000 = Column(Float)
    suitqmed = Column(Boolean)
    suitpooling = Column(Boolean)
    station_comments = Column(String)
    catchment_comments = Column(String)
    qmed_comments = Column(String)
    pooling_comments = Column(String)

    def __repr__(self):
        return ''


t_ungauged_catchment = Table(
    'ungauged_catchment', metadata,
    Column('index', BigInteger, index=True),
    Column('altbar', Float(53)),
    Column('area', Float(53)),
    Column('aspbar', Float(53)),
    Column('aspvar', Float(53)),
    Column('bfihost', Float(53)),
    Column('c', Float(53)),
    Column('c_1km', Float(53)),
    Column('catchment', Text),
    Column('catchment_name', Text),
    Column('centroid', Text),
    Column('centroid_e', BigInteger),
    Column('centroid_n', BigInteger),
    Column('d1', Float(53)),
    Column('d1_1km', Float(53)),
    Column('d2', Float(53)),
    Column('d2_1km', Float(53)),
    Column('d3', Float(53)),
    Column('d3_1km', Float(53)),
    Column('dplbar', Float(53)),
    Column('dpsbar', Float(53)),
    Column('e', Float(53)),
    Column('e_1km', Float(53)),
    Column('f', Float(53)),
    Column('f_1km', Float(53)),
    Column('farl', Float(53)),
    Column('fpdbar', Float(53)),
    Column('fpext', Float(53)),
    Column('fploc', Float(53)),
    Column('ldp', Float(53)),
    Column('propwet', Float(53)),
    Column('rmed_1d', Float(53)),
    Column('rmed_1h', Float(53)),
    Column('rmed_2d', Float(53)),
    Column('saar', Float(53)),
    Column('saar4170', Float(53)),
    Column('sprhost', Float(53)),
    Column('urbconc1990', Float(53)),
    Column('urbconc2000', Float(53)),
    Column('urbext1990', Float(53)),
    Column('urbext2000', Float(53)),
    Column('urbloc1990', Float(53)),
    Column('urbloc2000', Float(53)),
    Column('version', Text)
)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, server_default=text("nextval('user_id_seq'::regclass)"))
    username = Column(String(80), unique=True)
    email = Column(String(120), unique=True)
