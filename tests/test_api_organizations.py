import pytest
from fixtures.test_data import (api_url, api_url_with_uuid, just_organization)

API_BASE_URL = 'http://localhost:8000/api'


@pytest.mark.django_db
def test_get_organizations(api_client, just_organization):
    response = api_client.get(api_url)
    assert response.status_code == 200, (
        f'Ошибка запроса: {response.status_code}')

    data = response.json()
    assert all(key in data for key in ['count', 'next', 'previous', 'results'])

    results = data.get('results', [])
    assert isinstance(results, list)

    for result in results:
        assert isinstance(result, dict)
        expected_keys = ['relative_addr', 'full_name', 'short_name',
                         'factual_address', 'longitude', 'latitude', 'is_gov']
        assert all(key in result for key in expected_keys)


@pytest.mark.django_db
def test_get_organization_by_uuid(api_client, just_organization):
    response = api_client.get(api_url_with_uuid)
    assert response.status_code == 200, (
        f'Ошибка запроса: {response.status_code}')

    expected_keys = ['full_name', 'short_name', 'inn',
                     'factual_address', 'longitude', 'latitude',
                     'site', 'email', 'is_gov', 'about']
    data = response.json()
    assert all(key in data for key in expected_keys)
