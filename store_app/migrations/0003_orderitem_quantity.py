# Generated by Django 3.0.8 on 2020-09-19 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0002_remove_orderitem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]