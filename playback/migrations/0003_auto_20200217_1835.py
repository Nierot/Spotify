# Generated by Django 2.1.15 on 2020-02-17 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playback', '0002_user_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='token',
            field=models.CharField(blank=True, default=None, max_length=500, null=True),
        ),
    ]
