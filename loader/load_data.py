import json

from sqlalchemy import insert

from database.db import Session
from experiments.dao import ExperimentsDAO
from experiments.models import Experiments


def load_data():
    exprmts = ExperimentsDAO.find_all()

    if exprmts:
        return

    with Session() as session:  # noqa
        def open_mock_json(model: str):
            with open(f"tests/data/{model}.json", encoding="utf-8") as file:
                return json.load(file)

        data = open_mock_json('experiments')

        query = insert(Experiments).values(data)
        session.execute(query)
        session.commit()
