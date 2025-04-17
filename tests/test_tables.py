import pytest
from starlette import status


@pytest.mark.asyncio()
async def test_create_table(async_client):
    table_data = {
        'name': 'Стол 1',
        'seats': 6,
        'location': 'У окна'
    }

    response = await async_client.post('/tables/', json=table_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['name'] == table_data['name']
    assert response.json()['seats'] == table_data['seats']
    assert response.json()['location'] == table_data['location']


@pytest.mark.asyncio()
async def test_create_duplicate_table(async_client):
    table_data = {
        'name': 'Стол 13',
        'seats': 6,
        'location': 'У окна'
    }

    response1 = await async_client.post('/tables/', json=table_data)
    assert response1.status_code == status.HTTP_201_CREATED

    response2 = await async_client.post('/tables/', json=table_data)
    assert response2.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio()
async def test_get_table(async_client):
    table_data = {
        'name': 'Стол 1',
        'seats': 6,
        'location': 'У окна'
    }
    await async_client.post('/tables/', json=table_data)

    response = await async_client.get('/tables/')
    assert response.status_code == status.HTTP_200_OK
