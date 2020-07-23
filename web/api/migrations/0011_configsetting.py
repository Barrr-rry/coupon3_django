# Generated by Django 3.0 on 2020-07-23 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_store_pop'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_status', models.BooleanField(default=False, help_text='資料刪除狀態')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='建立時間')),
                ('updated_at', models.DateTimeField(help_text='更新時間', null=True)),
                ('deleted_at', models.DateTimeField(blank=True, help_text='刪除時間', null=True)),
                ('in_maintenance', models.BooleanField(default=False, help_text='維護中')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
