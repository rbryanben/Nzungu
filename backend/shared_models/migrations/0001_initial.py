# Generated by Django 5.1.2 on 2025-08-01 10:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReferencedObject',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ref', models.CharField(blank=True, max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('ref', models.CharField(max_length=256, unique=True)),
                ('url', models.CharField(max_length=512)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('referencedobject_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='shared_models.referencedobject')),
                ('name', models.CharField(max_length=128)),
                ('icon', models.CharField(max_length=32)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            bases=('shared_models.referencedobject',),
        ),
        migrations.CreateModel(
            name='ProductStockStatusFilter',
            fields=[
                ('referencedobject_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='shared_models.referencedobject')),
                ('name', models.CharField(max_length=256)),
                ('icon', models.CharField(max_length=32)),
                ('theme', models.CharField(max_length=32)),
                ('value', models.CharField(max_length=32)),
                ('subtext', models.CharField(max_length=128)),
            ],
            bases=('shared_models.referencedobject',),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('referencedobject_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='shared_models.referencedobject')),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=128)),
                ('price_usd', models.FloatField(default=0)),
                ('price_zwg', models.FloatField(default=0)),
                ('reorder_point', models.IntegerField(default=0)),
                ('expiry_day_buffer', models.IntegerField(default=5)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('image_uploaded', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='shared_models.upload')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='shared_models.productcategory')),
                ('product_stock_status_filter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='shared_models.productstockstatusfilter')),
            ],
            bases=('shared_models.referencedobject',),
        ),
    ]
