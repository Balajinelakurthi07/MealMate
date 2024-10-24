# Generated by Django 5.0 on 2024-05-18 10:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_menusection_delete_menuitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='main.menusection')),
            ],
        ),
    ]
