# Generated by Django 2.0.3 on 2018-03-20 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='content',
            field=models.CharField(default='RT', max_length=4000),
        ),
    ]