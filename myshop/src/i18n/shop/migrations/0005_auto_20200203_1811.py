# Generated by Django 3.0.2 on 2020-02-03 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20200203_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description_en',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='description_zh_hant',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='name_en',
            field=models.CharField(db_index=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='name_zh_hant',
            field=models.CharField(db_index=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='slug_en',
            field=models.SlugField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='slug_zh_hant',
            field=models.SlugField(max_length=200, null=True),
        ),
    ]
