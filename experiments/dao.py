from sqlalchemy import update

from database.db import Session

from .models import Devices, ExperimentDistribution, Experiments


class BaseDAO:
    _model = None

    @classmethod
    def find_all(cls, **filter_by):
        with Session() as session:
            query = session.query(cls._model).filter_by(**filter_by)
            return query.all()

    @classmethod
    def find_one_or_none(cls, **filter_by):
        with Session() as session:
            query = session.query(cls._model).filter_by(**filter_by)
            return query.one_or_none()

    @classmethod
    def add(cls, **kwargs):
        with Session() as session:
            obj = cls._model(**kwargs)
            session.add(obj)
            session.commit()
            return obj


class DevicesDAO(BaseDAO):
    _model = Devices


class ExperimentsDAO(BaseDAO):
    _model = Experiments


class ExperimentDistributionDAO(BaseDAO):
    _model = ExperimentDistribution

    @classmethod
    def update_device_count(cls, device_count, **filter_by):
        with Session() as session:
            query = update(cls._model).filter_by(**filter_by).values(device_count=device_count)
            obj = session.execute(query)
            session.commit()
            return obj
