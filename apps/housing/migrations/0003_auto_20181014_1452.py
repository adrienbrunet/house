# Generated by Django 2.1.2 on 2018-10-14 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('housing', '0002_housing_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housing',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='housing', to='groups.Group', verbose_name='Group'),
        ),
    ]