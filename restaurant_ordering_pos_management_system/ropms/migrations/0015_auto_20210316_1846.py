# Generated by Django 3.1.5 on 2021-03-16 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ropms', '0014_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]