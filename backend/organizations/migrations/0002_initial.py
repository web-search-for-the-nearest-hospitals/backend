from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('geography', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizations', '0001_initial'),
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
        migrations.AddField(
            model_name='organization',
            name='town',
            field=models.ForeignKey(
                help_text='Город организации', null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='organizations',
                to='geography.town',
                verbose_name='Город организации'),
        ),
        migrations.AddConstraint(
            model_name='organizationspecialty',
            constraint=models.UniqueConstraint(
                fields=('organization', 'specialty', 'day_of_the_week'),
                name='organizations_unique_orgspec_schedule'),
        ),
        migrations.AddConstraint(
            model_name='organizationbusinesshour',
            constraint=models.UniqueConstraint(
                fields=('organization', 'day'),
                name='unique_orgbusinesshour_org_day'),
        ),
        migrations.AddIndex(
            model_name='organization',
            index=models.Index(fields=['short_name', 'factual_address'],
                               name='organizatio_short_n_32d8d1_idx'),
        ),
        migrations.AddConstraint(
            model_name='organization',
            constraint=models.UniqueConstraint(
                fields=('short_name', 'factual_address'),
                name='unique_organization_short_name_factual_address'),
        ),
    ]
