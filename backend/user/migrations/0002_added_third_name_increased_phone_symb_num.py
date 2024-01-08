from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='third_name',
            field=models.CharField(blank=True,
                                   help_text='Отчество пользователя',
                                   max_length=150, null=True,
                                   verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, help_text='Имя пользователя',
                                   max_length=150, null=True,
                                   verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, help_text='Фамилия пользователя',
                                   max_length=150, null=True,
                                   verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True,
                                   help_text='Номер телефона пользователя',
                                   max_length=20, null=True,
                                   verbose_name='Номер телефона'),
        ),
    ]
