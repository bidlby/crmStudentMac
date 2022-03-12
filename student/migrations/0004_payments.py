# Generated by Django 4.0.1 on 2022-03-12 08:30

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_delete_testtable'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('transactionId', models.AutoField(primary_key=True, serialize=False)),
                ('Payment_Ref', models.CharField(max_length=200)),
                ('transactionDate', models.DateField(default=datetime.datetime.now)),
                ('paymentAmount', models.IntegerField()),
                ('currency', models.CharField(default='AED', max_length=20)),
                ('gbFlag', models.BooleanField(default=False)),
                ('StudentId', models.ForeignKey(max_length=20, on_delete=django.db.models.deletion.DO_NOTHING, to='student.customerinfo')),
            ],
        ),
    ]