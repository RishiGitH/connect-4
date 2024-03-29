# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2020-09-27 18:46
from __future__ import unicode_literals

import api.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('board', models.TextField(default=api.models.get_staring_board)),
                ('move_count', models.IntegerField(default=0)),
                ('result', models.PositiveSmallIntegerField(choices=[(1, 'Red Wins the Game'), (2, 'Yellow Wins the Game'), (0, 'Game is in Progress')], default=0)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'game_records',
            },
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('player_colour', models.CharField(choices=[('Red', 'Red'), ('Yellow', 'Yellow')], max_length=20)),
                ('column', models.IntegerField(validators=[django.core.validators.MaxValueValidator(6), django.core.validators.MinValueValidator(0)])),
                ('move_number', models.IntegerField()),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Game')),
            ],
            options={
                'db_table': 'game_moves',
            },
        ),
    ]
