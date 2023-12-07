# Generated by Django 4.2.7 on 2023-12-07 10:02

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Наименование района')),
            ],
            options={
                'verbose_name': 'Район',
                'verbose_name_plural': 'Районы',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(help_text='Идентификатор организации в БД', primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('full_name', models.TextField(help_text='Полное наименование организации', verbose_name='Полное наименование')),
                ('short_name', models.TextField(blank=True, help_text='Сокращенное наименование организации', null=True, verbose_name='Сокращенное наименование')),
                ('inn', models.CharField(blank=True, help_text='ИНН организации', max_length=12, null=True, verbose_name='ИНН')),
                ('factual_address', models.TextField(help_text='Адрес местонахождения организации', verbose_name='Адрес')),
                ('date_added', models.DateTimeField(auto_now=True, help_text='Дата внесения организации в БД', verbose_name='Дата создания организации в БД')),
                ('longitude', models.FloatField(help_text='Долгота расположения организации', verbose_name='Долгота')),
                ('latitude', models.FloatField(help_text='Широта расположения организации', verbose_name='Широта')),
                ('site', models.CharField(blank=True, help_text='Сайт организации', max_length=100, null=True, verbose_name='Сайт организации')),
                ('email', models.EmailField(blank=True, help_text='E-mail организации', max_length=100, null=True, verbose_name='E-mail организации')),
                ('is_gov', models.BooleanField(default=False, help_text='Является ли организация государственной', verbose_name='Государственная?')),
                ('is_full_time', models.BooleanField(default=False, help_text='Является ли организация круглосуточной', verbose_name='Круглосуточная?')),
                ('about', models.TextField(blank=True, help_text='Дополнительная информация об организации', null=True, verbose_name='Дополнительная информация')),
                ('district', models.ForeignKey(help_text='Район организации', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='organizations', to='organizations.district', verbose_name='Район организации')),
            ],
            options={
                'verbose_name': 'Организация',
                'verbose_name_plural': 'Организации',
                'ordering': ['full_name'],
            },
        ),
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('code', models.CharField(max_length=8, primary_key=True, serialize=False, verbose_name='Код')),
                ('name', models.CharField(max_length=150, verbose_name='Наименование')),
                ('skill', models.CharField(max_length=150, verbose_name='Врач')),
            ],
            options={
                'verbose_name': 'Специальность',
                'verbose_name_plural': 'Специальности',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Town',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, verbose_name='Наименование города')),
                ('longitude', models.FloatField(help_text='Долгота расположения центра города', verbose_name='Долгота')),
                ('latitude', models.FloatField(help_text='Широта расположения центра города', verbose_name='Широта')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='OrganizationSpecialty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_the_week', models.PositiveIntegerField(choices=[(1, 'Понедельник'), (2, 'Вторник'), (3, 'Среда'), (4, 'Четверг'), (5, 'Пятница'), (6, 'Суббота'), (7, 'Воскресение')], verbose_name='День недели')),
                ('working_hours', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=11), size=None, verbose_name='Часы работы')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specialties', to='organizations.organization', verbose_name='Организация')),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organizations', to='organizations.specialty', verbose_name='Специальность')),
            ],
            options={
                'verbose_name': 'Расписание специальностей',
                'verbose_name_plural': 'Расписания специальностей',
                'ordering': None,
            },
        ),
        migrations.AddField(
            model_name='organization',
            name='town',
            field=models.ForeignKey(help_text='Город организации', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='organizations', to='organizations.town', verbose_name='Город организации'),
        ),
        migrations.AddField(
            model_name='district',
            name='town',
            field=models.ForeignKey(help_text='Город', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='districts', to='organizations.town', verbose_name='Город'),
        ),
        migrations.AddConstraint(
            model_name='organizationspecialty',
            constraint=models.UniqueConstraint(fields=('organization', 'specialty', 'day_of_the_week'), name='unique_orgspec_organization_specialty_day'),
        ),
    ]
