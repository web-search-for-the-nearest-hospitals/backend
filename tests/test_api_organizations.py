import requests
import uuid

BASE_URL = 'http://localhost:8000/api/organizations'


def test_get_organizations_list():
    '''Проверяет, что сервер возвращает статус код 200,
    и ответ содержит необходимые поля для списка организаций.'''
    response = requests.get(BASE_URL)
    assert response.status_code == 200, (
        f'Ошибка запроса: {response.status_code}')

    data = response.json()

    assert 'count' in data
    assert 'next' in data
    assert 'previous' in data
    assert 'results' in data

    if data['results']:
        assert isinstance(data['results'], list)
        organization_fields = ['relative_addr', 'full_name',
                               'short_name', 'factual_address', 'longitude',
                               'latitude', 'is_gov']

        for org in data['results']:
            assert isinstance(org, dict)
            for field in organization_fields:
                assert field in org


def test_get_organization_by_uuid():
    ''''Проверяет, что сервер возвращает статус код 200 (ОК),
    и ответ содержит ожидаемые поля для информации об одной организации.'''
    organization_uuid = str(uuid.uuid4())

    response = requests.get(f'{BASE_URL}/{organization_uuid}')
    assert response.status_code == 200, (
        f'Ошибка запроса: {response.status_code}')

    data = response.json()

    organization_fields = ['full_name', 'short_name', 'inn',
                           'factual_address', 'longitude', 'latitude',
                           'site', 'email', 'is_gov', 'about']

    for field in organization_fields:
        assert field in data
