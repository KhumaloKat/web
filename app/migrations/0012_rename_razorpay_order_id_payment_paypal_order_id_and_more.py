# Generated by Django 5.0.6 on 2024-06-27 04:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_rename_razorpay_oder_id_payment_razorpay_order_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='razorPay_order_id',
            new_name='PayPal_order_id',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='razorPay_order_status',
            new_name='PayPal_order_status',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='razorPay_payment_id',
            new_name='Paypal_payment_id',
        ),
    ]
