# Generated by Django 3.2.6 on 2021-08-20 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0004_alter_topic_suject'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topic',
            old_name='suject',
            new_name='subject',
        ),
    ]
