import pytest
from backend.organizations.models import Organization, Town, District


@pytest.fixture
def Just_town():
    return Town.objects.create(
        name='Just Town',
        longitude=0.0,
        latitude=0.0
    )


@pytest.fixture
def Just_district(Just_town):
    return District.objects.create(
        name='Just District',
        town=Just_town
    )


@pytest.fixture
def Just_organization(Just_town, Just_district):
    return Organization.objects.create(
        full_name='Just Organization',
        short_name='Just Org',
        inn='1234567890',
        factual_address='Just Address',
        longitude=0.0,
        latitude=0.0,
        site='http://Just.ru',
        email='Just@gmail.com',
        phone='123-456-789',
        is_gov=False,
        is_full_time=True,
        about='Just description',
        town=Just_town,
        district=Just_district
    )
