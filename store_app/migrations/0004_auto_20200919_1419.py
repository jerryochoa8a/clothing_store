# Generated by Django 3.0.8 on 2020-09-19 21:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0003_orderitem_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='orderItem',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orderItems', to='store_app.Order'),
        ),
    ]
