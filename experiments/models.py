from sqlalchemy import DECIMAL, JSON, Column, ForeignKey, Integer, String

from database.db import Base


class Devices(Base):
    __tablename__ = 'devices'

    device_token = Column(String, primary_key=True)
    button_color = Column(String(7), nullable=False)
    price = Column(DECIMAL(5, 2), nullable=False)


class Experiments(Base):
    __tablename__ = 'experiments'

    name = Column(String, primary_key=True)
    options = Column(JSON, nullable=False)
    values = Column(JSON, nullable=False)


class ExperimentDistribution(Base):
    __tablename__ = 'experiment_distribution'

    id = Column(Integer, primary_key=True)
    experiment_key = Column(String, ForeignKey('experiments.name'))
    experiment_value = Column(String, nullable=False)
    device_count = Column(Integer, nullable=False)

