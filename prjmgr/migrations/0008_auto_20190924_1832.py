# Generated by Django 2.2.1 on 2019-09-24 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prjmgr', '0007_auto_20190924_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='consignee',
            field=models.ManyToManyField(blank=True, related_name='Customer', to='prjmgr.Customer'),
        ),
    ]