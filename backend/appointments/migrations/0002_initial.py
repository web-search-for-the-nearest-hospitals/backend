import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('appointments', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('specialties', '0001_initial'),
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='client',
            field=models.ForeignKey(blank=True, null=True,
                                    on_delete=django.db.models.deletion.CASCADE,
                                    related_name='appointments',
                                    to=settings.AUTH_USER_MODEL,
                                    verbose_name='Клиент'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='appointments',
                                    to='organizations.organization',
                                    verbose_name='Организация'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='specialty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='appointments',
                                    to='specialties.specialty',
                                    verbose_name='Специальность врача'),
        ),
        migrations.AddConstraint(
            model_name='appointment',
            constraint=models.UniqueConstraint(
                fields=('organization', 'specialty', 'datetime_start'),
                name='appointments_unique_org_spec_datetimestart'),
        ),
    ]
