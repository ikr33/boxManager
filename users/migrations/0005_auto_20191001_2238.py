# Generated by Django 2.1.7 on 2019-10-01 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_sharedmessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sharedmessage',
            name='message_id',
        ),
        migrations.AddField(
            model_name='sharedmessage',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]