# Generated by Django 2.2.4 on 2020-07-08 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Faves_app', '0003_city_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='likes',
            name='web_url',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
