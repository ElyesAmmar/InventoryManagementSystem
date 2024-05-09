# Generated by Django 5.0.4 on 2024-05-08 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('order_num', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('customer_id', models.IntegerField()),
                ('total_amount', models.FloatField()),
                ('shipping_address', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='OrdersItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.IntegerField()),
                ('product_id', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('unit_price', models.FloatField()),
                ('total_price', models.FloatField()),
            ],
        ),
    ]
