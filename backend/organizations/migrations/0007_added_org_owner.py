from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizations', '0006_added_long_lat_to_district'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='owner',
            field=models.ForeignKey(
                help_text='Пользователь, создавший организацию', null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='orgs', to=settings.AUTH_USER_MODEL,
                verbose_name='Владелец'),
        ),
    ]
