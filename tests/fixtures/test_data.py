import pytest
from backend.organizations.models import Organization, Town, District
from django.urls import reverse
from uuid import uuid4


@pytest.fixture
def just_town():
    return Town.objects.create(
        name='just Town',
        longitude=0.0,
        latitude=0.0
    )


@pytest.fixture
def just_district(just_town):
    return District.objects.create(
        name='just District',
        town=just_town
    )


@pytest.fixture
def just_organization(just_town, just_district):
    return Organization.objects.create(
        full_name='just Organization',
        short_name='just Org',
        inn='1234567890',
        factual_address='just Address',
        longitude=0.0,
        latitude=0.0,
        site='http://just.org',
        email='just@gmail.com',
        phone='123-456-789',
        is_gov=False,
        is_full_time=True,
        about='just description',
        town=just_town,
        district=just_district
    )


@pytest.fixture
def api_url():
    return '/api/organizations'


@pytest.fixture
def api_url_with_uuid(just_organization):
    organization_uuid = str(uuid4())
    return reverse('organization-detail', kwargs={'uuid': organization_uuid})
