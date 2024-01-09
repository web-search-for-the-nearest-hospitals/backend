from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('organizations', '0005_added_appointments_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='district',
            name='latitude',
            field=models.FloatField(
                help_text='Широта расположения центра района', null=True,
                verbose_name='Широта'),
        ),
        migrations.AddField(
            model_name='district',
            name='longitude',
            field=models.FloatField(
                help_text='Долгота расположения центра района', null=True,
                verbose_name='Долгота'),
        )
    ]
