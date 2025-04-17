import pytest
from fastapi import status


@pytest.mark.asyncio()
async def test_create_reservation(async_client):
    table_data = {
        'name': 'Стол 1',
        'seats': 6,
        'location': 'У окна'
    }
    res = await async_client.post('/tables/', json=table_data)

    reservation_data = {
        'customer_name': 'Иван',
        'table_id': res.json()['id'],
        'reservation_time': '2025-04-15T19:00:00',
        'duration_minutes': 60
    }
    response = await async_client.post('/reservations/', json=reservation_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['customer_name'] == reservation_data['customer_name']
    assert response.json()['table_id'] == reservation_data['table_id']
    assert response.json()['reservation_time'] == reservation_data['reservation_time']
    assert response.json()['duration_minutes'] == reservation_data['duration_minutes']

async def test_reservation_conflict(async_client):
    table_data = {
        'name': 'Стол 1',
        'seats': 6,
        'location': 'У окна'
    }
    res_table = await async_client.post('/tables/', json=table_data)

    reservation1_data = {
        'customer_name': 'Иван',
        'table_id': res_table.json()['id'],
        'reservation_time': '2025-04-15T19:00:00',
        'duration_minutes': 60
    }
    reservation2_data = {
        'customer_name': 'Иван',
        'table_id': res_table.json()['id'],
        'reservation_time': '2025-04-15T18:30:00',
        'duration_minutes': 60
    }

    await async_client.post('/reservations/', json=reservation1_data)
    response = await async_client.post('/reservations/', json=reservation2_data)


    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == 'Table is already reserved for this time slot'


@pytest.mark.asyncio()
async def test_get_reservations(async_client):
    table_data = {
        'name': 'Стол 1',
        'seats': 6,
        'location': 'У окна'
    }
    res_table = await async_client.post('/tables/', json=table_data)

    reservation_data = {
        'customer_name': 'Иван',
        'table_id': res_table.json()['id'],
        'reservation_time': '2025-04-15T18:30:00',
        'duration_minutes': 60
    }
    await async_client.post('/reservations/', json=reservation_data)

    response = await async_client.get('/reservations/')
    assert response.status_code == status.HTTP_200_OK
