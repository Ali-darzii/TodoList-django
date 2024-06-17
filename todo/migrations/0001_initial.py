# Generated by Django 5.0.6 on 2024-06-16 15:37

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth_service', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('start_date', models.DateTimeField(default=datetime.datetime(2024, 6, 16, 15, 37, 55, 861617, tzinfo=datetime.timezone.utc))),
                ('dead_line', models.DateTimeField()),
                ('completed', models.BooleanField(default=False)),
                ('completed_date', models.DateTimeField(blank=True, null=True)),
                ('priority', models.PositiveIntegerField(default=0)),
                ('user_logins', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todos', to='auth_service.userlogins')),
            ],
            options={
                'verbose_name': 'Todo',
                'verbose_name_plural': 'Todos',
                'db_table': 'Todo_DB',
                'ordering': ('priority', 'start_date'),
            },
        ),
    ]
