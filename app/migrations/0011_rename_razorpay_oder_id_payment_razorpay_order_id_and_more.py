# Generated by Django 5.0.6 on 2024-06-27 03:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_payment_orderplaced'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='razorPay_oder_id',
            new_name='razorPay_order_id',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='razorPay_oder_status',
            new_name='razorPay_order_status',
        ),
    ]
