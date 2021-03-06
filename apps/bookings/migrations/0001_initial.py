# Generated by Django 2.1.2 on 2018-10-14 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0003_auto_20181013_1157'),
        ('housing', '0003_auto_20181014_1452'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(verbose_name='Start date')),
                ('end_date', models.DateTimeField(verbose_name='End date')),
                ('comments', models.TextField(verbose_name='Comments')),
                ('booker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserProfile', verbose_name='Booker')),
                ('housing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='housing.Housing', verbose_name='Housing')),
            ],
            options={
                'verbose_name': 'Booking',
                'verbose_name_plural': 'Bookings',
            },
        ),
    ]
