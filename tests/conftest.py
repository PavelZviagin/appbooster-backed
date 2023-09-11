import asyncio
import json
import random

import pytest as pytest
from httpx import AsyncClient
from sqlalchemy import insert

from database.db import Base, Session, engine
from experiments.models import Experiments
from main import app as fastapi_app
from settings import settings


def generate_hex_string(length=16):
    """Generate a random hexadecimal string of given length."""
    characters = '0123456789abcdef'
    return ''.join(random.choice(characters) for _ in range(length))


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with Session() as session:
        def open_mock_json(model: str):
            with open(f"tests/data/{model}.json", encoding="utf-8") as file:
                return json.load(file)

        data = open_mock_json('experiments')

        query = insert(Experiments).values(data)
        session.execute(query)
        session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def client():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="function")
async def client_with_dt():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as client:
        client.headers = {
            'device-token': generate_hex_string(24)
        }

        data = await client.get('/api/experiments')
        client.data = data.json()

        yield client
