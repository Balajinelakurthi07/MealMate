# Generated by Django 5.0 on 2024-06-16 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_order_orderitem_order_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='item',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
