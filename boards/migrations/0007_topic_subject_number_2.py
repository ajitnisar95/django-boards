# Generated by Django 3.2.6 on 2021-08-20 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0006_alter_topic_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='subject_number_2',
            field=models.CharField(default='NULL', max_length=8),
        ),
    ]
