# Generated by Django 3.2.6 on 2021-08-20 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Prices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datep', models.DateTimeField(verbose_name='Дата')),
                ('store', models.CharField(max_length=128, verbose_name='Место покупки')),
                ('product', models.CharField(max_length=256, verbose_name='Продукт (товар)')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Цена')),
                ('details', models.TextField(blank=True, null=True, verbose_name='Подробности')),
            ],
            options={
                'db_table': 'prices',
            },
        ),
        migrations.AddIndex(
            model_name='prices',
            index=models.Index(fields=['datep'], name='prices_datep_906236_idx'),
        ),
        migrations.AddIndex(
            model_name='prices',
            index=models.Index(fields=['store'], name='prices_store_3a7df0_idx'),
        ),
        migrations.AddIndex(
            model_name='prices',
            index=models.Index(fields=['product'], name='prices_product_519819_idx'),
        ),
    ]
