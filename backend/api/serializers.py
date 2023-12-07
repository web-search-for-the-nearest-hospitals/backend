from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import serializers

from organizations.models import (Organization, OrganizationSpecialty,
                                  Specialty)


class SpecialtySerializer(serializers.ModelSerializer):
    """Сериализатор специальности врача."""

    class Meta:
        model = Specialty
        fields = ('code', 'name', 'skill')


class OrgSpecialtySerializer(serializers.ModelSerializer):
    """Сериализатор специальностей организации."""

    code = serializers.CharField(source='specialty.code')
    name = serializers.CharField(source='specialty.name')
    skill = serializers.CharField(source='specialty.skill')

    class Meta:
        model = OrganizationSpecialty
        fields = ('code', 'name', 'skill', 'working_hours', 'day_of_the_week')


class OrganizationSerializer(serializers.ModelSerializer):
    """Сериализатор организации."""

    specialties = OrgSpecialtySerializer(many=True, required=False)
    relative_addr = serializers.SerializerMethodField(
        label='relative_addr',
        help_text='относительный адрес организации',
        read_only=True)

    class Meta:
        model = Organization
        lookup_field = 'uuid'
        fields = ('relative_addr', 'full_name', 'short_name', 'inn',
                  'factual_address',
                  'date_added', 'longitude', 'latitude',
                  'site', 'email', 'is_gov', 'is_full_time',
                  'about', 'specialties')

    def get_relative_addr(self, obj):
        return reverse('api:organizations-detail',
                       kwargs={'uuid': obj.uuid})

    @staticmethod
    def create_org_specialty(specialties: dict,
                             org: Organization) -> None:
        new_org_specialties = []

        for specialty in specialties:
            spec_data = specialty['specialty']
            code = spec_data['code']
            name = spec_data['name']
            skill = spec_data['skill']
            working_hours = specialty['working_hours']
            day_of_the_week = specialty['day_of_the_week']
            current_specialty = get_object_or_404(
                Specialty, code=code,
                name=name, skill=skill)
            new_org_specialties.append(
                OrganizationSpecialty(
                    organization=org,
                    specialty=current_specialty,
                    working_hours=working_hours,
                    day_of_the_week=day_of_the_week
                )
            )
        OrganizationSpecialty.objects.bulk_create(new_org_specialties)

    def create(self, validated_data):
        specialties = validated_data.pop('specialties')
        with transaction.atomic():
            org = Organization.objects.create(**validated_data)
            self.create_org_specialty(specialties, org)
        return org

    def update(self, instance, validated_data):
        specialties = validated_data.pop('specialties')
        with transaction.atomic():
            instance = super().update(instance, validated_data)
            OrganizationSpecialty.objects.filter(
                organization=instance
            ).delete()
            self.create_org_specialty(specialties, instance)
        return instance
