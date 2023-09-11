from experiments.dao import ExperimentDistributionDAO
from tests.conftest import generate_hex_string


async def test_distributions(client):
    for _ in range(600):
        client.headers = {
            'device-token': generate_hex_string(24)
        }
        await client.get("/api/experiments")

    distributions_color = ExperimentDistributionDAO.find_all(experiment_key='button_color')
    distributions_price = ExperimentDistributionDAO.find_all(experiment_key='price')

    for distribution in distributions_color:
        assert distribution.device_count == 200

    distributions_price_sorted = sorted(distributions_price, key=lambda x: x.experiment_value)

    assert distributions_price_sorted[0].device_count == 450
    assert distributions_price_sorted[1].device_count == 60
    assert distributions_price_sorted[2].device_count == 60
    assert distributions_price_sorted[3].device_count == 30


async def test_get_experiments(client):
    client.headers = {
        'device-token': generate_hex_string(24)
    }

    response = await client.get("/api/experiments")

    assert response.status_code == 200
    assert response.json()['button_color'] in ['#FF0000', '#00FF00', '#0000FF']
    assert response.json()['price'] in [10.0, 20.0, 50.0, 5.0]


async def test_get_experiments_with_dt(client_with_dt):
    response = await client_with_dt.get("/api/experiments")

    assert response.status_code == 200
    assert response.json()['button_color'] == client_with_dt.data['button_color']
    assert response.json()['price'] == client_with_dt.data['price']


async def test_server_response_time(client):
    response = await client.get("/api/experiments")
    assert response.elapsed.total_seconds() < 0.1


async def test_get_stats(client):
    response = await client.get("/api/stats")

    assert len(response.json()) == 2
    assert response.json()[0]['button_color']
    assert response.json()[1]['price']
