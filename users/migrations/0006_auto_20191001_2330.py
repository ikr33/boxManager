# Generated by Django 2.1.7 on 2019-10-01 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20191001_2238'),
    ]

    operations = [
        migrations.AddField(
            model_name='sharedmessage',
            name='note',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='sharedmessage',
            name='link',
            field=models.TextField(default=''),
        ),
    ]