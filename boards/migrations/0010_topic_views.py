# Generated by Django 3.2.6 on 2021-08-25 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0009_alter_topic_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
