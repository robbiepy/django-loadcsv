# Generated by Django 4.2.11 on 2024-04-10 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SimpleTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a', models.CharField(max_length=255)),
                ('b', models.CharField(max_length=255)),
                ('c', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'test',
            },
        ),
    ]
