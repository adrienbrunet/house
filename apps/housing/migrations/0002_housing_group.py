# Generated by Django 2.1.2 on 2018-10-14 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
        ('housing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='housing',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='groups.Group', verbose_name='Group'),
            preserve_default=False,
        ),
    ]