from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='phone',
            field=models.CharField(
                blank=True,
                help_text='Телефон организации',
                max_length=18,
                null=True,
                verbose_name='Номер телефона'),
        )
    ]
