import pytest
from django.urls import reverse


API_BASE_URL = 'http://localhost:8000/api/organizations'


@pytest.fixture
def api_url():
    return f'{API_BASE_URL}/organizations'


@pytest.mark.django_db
def test_get_organizations(api_client):
    response = api_client.get('/api/organizations')
    assert response.status_code == 200

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
def test_get_organization_by_uuid(api_client, sample_organization):
    organization_uuid = sample_organization.uuid
    url = reverse('organization-detail', kwargs={'uuid': organization_uuid})

    response = api_client.get(url)
    assert response.status_code == 200

    expected_keys = ['full_name', 'short_name', 'inn',
                     'factual_address', 'longitude', 'latitude',
                     'site', 'email', 'is_gov', 'about']
    data = response.json()
    assert all(key in data for key in expected_keys)
