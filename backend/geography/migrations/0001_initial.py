import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Town',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Наименование города',
                                          max_length=25,
                                          verbose_name='Наименование города')),
                ('longitude', models.FloatField(
                    help_text='Долгота расположения центра города',
                    verbose_name='Долгота')),
                ('latitude', models.FloatField(
                    help_text='Широта расположения центра города',
                    verbose_name='Широта')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Наименование района',
                                          max_length=40,
                                          verbose_name='Наименование района')),
                ('longitude', models.FloatField(
                    help_text='Долгота расположения центра района', null=True,
                    verbose_name='Долгота')),
                ('latitude', models.FloatField(
                    help_text='Широта расположения центра района', null=True,
                    verbose_name='Широта')),
                ('town', models.ForeignKey(help_text='Город', null=True,
                                           on_delete=django.db.models.deletion.CASCADE,
                                           related_name='districts',
                                           to='geography.town',
                                           verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Район',
                'verbose_name_plural': 'Районы',
                'ordering': ['name'],
            },
        ),
    ]
