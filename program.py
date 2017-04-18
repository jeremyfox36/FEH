
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, REAL
Base = declarative_base()


class Catchment(Base):
    __tablename__ = 'ungauged_catchments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    catchment_name = Column(String)
    version = Column(String)
    catchment = Column(String)
    centroid = Column(String)
    centroid_e = Column(Integer)
    centroid_n = Column(Integer)
    area = Column(REAL)
    altbar = Column(Integer)
    aspbar = Column(Integer)
    aspvar = Column(REAL)
    bfihost = Column(REAL)
    dplbar = Column(REAL)
    dpsbar = Column(REAL)
    farl = Column(REAL)
    fpext = Column(REAL)
    fpdbar = Column(REAL)
    fploc = Column(REAL)
    ldp = Column(REAL)
    propwet = Column(REAL)
    rmed_1h = Column(REAL)
    rmed_1d = Column(REAL)
    rmed_2d = Column(REAL)
    saar = Column(REAL)
    saar4170 = Column(REAL)
    sprhost = Column(REAL)
    urbconc1990 = Column(REAL)
    urbext1990 = Column(REAL)
    urbloc1990 = Column(REAL)
    urbconc2000 = Column(REAL)
    urbext2000 = Column(REAL)
    urbloc2000 = Column(REAL)
    c = Column(REAL)
    d1 = Column(REAL)
    d2 = Column(REAL)
    d3 = Column(REAL)
    e = Column(REAL)
    f = Column(REAL)
    c_1km = Column(REAL)
    d1_1km = Column(REAL)
    d2_1km = Column(REAL)
    d3_1km = Column(REAL)
    e_1km = Column(REAL)
    f_1km = Column(REAL)