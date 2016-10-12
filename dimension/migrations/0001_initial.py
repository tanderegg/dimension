# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import otree.db.models
import otree_save_the_change.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('otree', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_is_missing_players', otree.db.models.BooleanField(default=False, db_index=True, choices=[(True, 'Yes'), (False, 'No')])),
                ('id_in_subsession', otree.db.models.PositiveIntegerField(null=True, db_index=True)),
                ('round_number', otree.db.models.PositiveIntegerField(null=True, db_index=True)),
                ('session', otree.db.models.ForeignKey(related_name='dimension_group', to='otree.Session')),
            ],
            options={
                'db_table': 'dimension_group',
            },
            bases=(otree_save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_index_in_game_pages', otree.db.models.PositiveIntegerField(default=0, null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(null=True, db_index=True)),
                ('id_in_group', otree.db.models.PositiveIntegerField(null=True, db_index=True)),
                ('payoff', otree.db.models.CurrencyField(null=True, max_digits=12)),
                ('role_int', otree.db.models.PositiveIntegerField(null=True, blank=True)),
                ('seller_price0', otree.db.models.CurrencyField(null=True, max_digits=12, blank=True)),
                ('seller_price1', otree.db.models.CurrencyField(null=True, max_digits=12, blank=True)),
                ('seller_price2', otree.db.models.CurrencyField(null=True, max_digits=12, blank=True)),
                ('seller_price3', otree.db.models.CurrencyField(null=True, max_digits=12, blank=True)),
                ('seller_price4', otree.db.models.CurrencyField(null=True, max_digits=12, blank=True)),
                ('seller_price5', otree.db.models.CurrencyField(null=True, max_digits=12, blank=True)),
                ('seller_price6', otree.db.models.CurrencyField(null=True, max_digits=12, blank=True)),
                ('seller_price7', otree.db.models.CurrencyField(null=True, max_digits=12, blank=True)),
                ('seller_total_price', otree.db.models.CurrencyField(null=True, max_digits=12, blank=True)),
                ('sales', otree.db.models.PositiveIntegerField(null=True, blank=True)),
                ('earnings', otree.db.models.PositiveIntegerField(null=True, blank=True)),
                ('buyer_choice', otree.db.models.PositiveIntegerField(blank=True, null=True, verbose_name=b'And you will', choices=[(0, b'Buy from seller 0'), (1, b'Buy from seller 1')])),
                ('price_paid', otree.db.models.PositiveIntegerField(null=True, blank=True)),
                ('identifier', otree.db.models.PositiveIntegerField(null=True, blank=True)),
                ('clicks', otree.db.models.PositiveIntegerField(default=0, null=True)),
                ('group', otree.db.models.ForeignKey(to='dimension.Group', null=True)),
                ('participant', otree.db.models.ForeignKey(related_name='dimension_player', to='otree.Participant')),
                ('session', otree.db.models.ForeignKey(related_name='dimension_player', to='otree.Session')),
            ],
            options={
                'db_table': 'dimension_player',
            },
            bases=(otree_save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.CreateModel(
            name='Subsession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('round_number', otree.db.models.PositiveIntegerField(null=True, db_index=True)),
                ('num_prices', otree.db.models.PositiveIntegerField(null=True)),
                ('sellers_per_group', otree.db.models.PositiveIntegerField(null=True)),
                ('buyers_per_group', otree.db.models.PositiveIntegerField(null=True)),
                ('session', otree.db.models.ForeignKey(related_name='dimension_subsession', to='otree.Session', null=True)),
            ],
            options={
                'db_table': 'dimension_subsession',
            },
            bases=(otree_save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.AddField(
            model_name='player',
            name='subsession',
            field=otree.db.models.ForeignKey(to='dimension.Subsession'),
        ),
        migrations.AddField(
            model_name='group',
            name='subsession',
            field=otree.db.models.ForeignKey(to='dimension.Subsession'),
        ),
    ]
