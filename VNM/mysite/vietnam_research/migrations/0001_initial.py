# Generated by Django 2.1.10 on 2019-07-22 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market_code', models.CharField(max_length=4)),
                ('symbol', models.CharField(max_length=10)),
                ('company_name', models.CharField(max_length=50)),
                ('industry1', models.CharField(max_length=10)),
                ('industry2', models.CharField(max_length=20)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
    ]
