# Generated by Django 5.0.7 on 2025-07-04 16:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('students', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DisciplinaryAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='InfractionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('severity', models.IntegerField(choices=[(1, 'Minor'), (2, 'Moderate'), (3, 'Severe')])),
            ],
        ),
        migrations.CreateModel(
            name='BehaviorNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('note', models.TextField()),
                ('noted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='behavior_notes', to='students.student')),
            ],
        ),
        migrations.CreateModel(
            name='DisciplinaryRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('description', models.TextField()),
                ('action_date', models.DateField(blank=True, null=True)),
                ('resolved', models.BooleanField(default=False)),
                ('resolution_notes', models.TextField(blank=True)),
                ('action_taken', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='discipline.disciplinaryaction')),
                ('reported_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported_infractions', to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disciplinary_records', to='students.student')),
                ('infraction_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discipline.infractiontype')),
            ],
        ),
    ]
