# Generated by Django 3.1.5 on 2021-03-13 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerTables',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=250)),
                ('capacity', models.IntegerField()),
                ('status', models.CharField(choices=[('Occupied', 'Occupied'), ('Unoccupied', 'Unoccupied')], default='Occupied', max_length=250)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
