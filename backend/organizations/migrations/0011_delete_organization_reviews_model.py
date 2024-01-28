from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0010_added_reviews_model'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='author',
        ),
        migrations.RemoveField(
            model_name='review',
            name='organization',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]
