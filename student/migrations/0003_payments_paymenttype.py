# Generated by Django 4.0.1 on 2022-03-13 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_rename_gbflag_payments_gb1'),
    ]

    operations = [
        migrations.AddField(
            model_name='payments',
            name='paymenttype',
            field=models.CharField(choices=[('Card', 'Card'), ('Cash', 'Cash')], default='Cash', max_length=50),
        ),
    ]