# Generated by Django 3.0 on 2020-07-06 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_store_search_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='storediscount',
            name='picture',
            field=models.CharField(default=True, help_text='商家圖片', max_length=128, null=True),
        ),
    ]
