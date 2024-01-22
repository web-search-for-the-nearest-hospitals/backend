from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('organizations', '0008_added_max_length_to_org_about_field'),
    ]

    operations = [

        migrations.AlterField(
            model_name='organization',
            name='phone',
            field=models.CharField(
                blank=True, help_text='Телефон организации',
                                   max_length=20, null=True,
                                   verbose_name='Номер телефона'),
        ),
    ]
