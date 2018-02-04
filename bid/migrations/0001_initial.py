# Generated by Django 2.0.1 on 2018-02-04 02:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid_action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diff', models.IntegerField()),
                ('refer_time', models.FloatField()),
                ('bid_time', models.FloatField()),
                ('delay_time', models.FloatField()),
                ('ahead_price', models.FloatField()),
                ('action_date', models.DateTimeField()),
                ('action_result', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Bid_auction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('auction_name', models.CharField(max_length=10)),
                ('ID_number', models.CharField(max_length=18)),
                ('Bid_number', models.CharField(max_length=8)),
                ('Bid_password', models.CharField(max_length=4)),
                ('status', models.IntegerField()),
                ('count', models.IntegerField()),
                ('expired_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Bid_hander',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hander_name', models.CharField(max_length=32)),
                ('basic_salary', models.FloatField(default=50)),
                ('extra_bonus', models.FloatField(default=0)),
                ('total_income', models.FloatField(default=0)),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='handers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='bid_action',
            name='auction_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bid_actions', to='bid.Bid_auction'),
        ),
        migrations.AddField(
            model_name='bid_action',
            name='hander_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bid_actions', to=settings.AUTH_USER_MODEL),
        ),
    ]
