# Generated by Django 3.1.5 on 2021-03-14 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ropms', '0006_menu'),
    ]

    operations = [
        migrations.AddField(
            model_name='customertable',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='customer_table', to='ropms.customer'),
        ),
    ]
