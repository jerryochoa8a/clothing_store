# Generated by Django 3.0.8 on 2020-10-02 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0007_auto_20201002_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='desc',
            field=models.TextField(max_length=200),
        ),
    ]