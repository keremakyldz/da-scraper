# Generated by Django 5.1.1 on 2024-10-21 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brands',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=50)),
                ('model_name', models.CharField(max_length=150)),
                ('price_tag', models.IntegerField(default='Unknown-?€')),
            ],
        ),
    ]
