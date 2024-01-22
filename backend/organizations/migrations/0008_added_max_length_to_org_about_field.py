from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('organizations', '0007_added_org_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='about',
            field=models.TextField(
                blank=True,
                help_text='Дополнительная информация об организации',
                max_length=500, null=True,
                verbose_name='Дополнительная информация'),
        ),
    ]
