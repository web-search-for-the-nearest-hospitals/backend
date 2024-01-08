import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('user', '0002_added_third_name_increased_phone_symb_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(
                blank=True, max_length=150, null=True,
                validators=[
                    django.contrib.auth.validators.UnicodeUsernameValidator()],
                verbose_name='Никнейм пользователя'),
        ),
    ]
