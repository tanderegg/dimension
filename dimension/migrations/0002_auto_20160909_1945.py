# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('dimension', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='cum_profits',
            field=otree.db.models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='player',
            name='q1',
            field=otree.db.models.CharField(blank=True, max_length=500, null=True, verbose_name=b"How many tokens will you receive if you don't sell an object?", choices=[(b'0 Tokens', b'0 Tokens'), (b'800 Tokens', b'800 Tokens'), (b'It depends on the prices I set', b'It depends on the prices I set')]),
        ),
        migrations.AddField(
            model_name='player',
            name='q2',
            field=otree.db.models.CharField(blank=True, max_length=500, null=True, verbose_name=b'How many tokens will you receive if you sell an object?', choices=[(b'0 tokens', b'0 tokens'), (b'800 tokens', b'800 tokens'), (b'It depends on the prices I set', b'It depends on the prices I set')]),
        ),
        migrations.AddField(
            model_name='player',
            name='seller_price10',
            field=otree.db.models.CurrencyField(null=True, verbose_name=b'Price 11', max_digits=12, blank=True),
        ),
        migrations.AddField(
            model_name='player',
            name='seller_price11',
            field=otree.db.models.CurrencyField(null=True, verbose_name=b'Price 12', max_digits=12, blank=True),
        ),
        migrations.AddField(
            model_name='player',
            name='seller_price12',
            field=otree.db.models.CurrencyField(null=True, verbose_name=b'Price 13', max_digits=12, blank=True),
        ),
        migrations.AddField(
            model_name='player',
            name='seller_price13',
            field=otree.db.models.CurrencyField(null=True, verbose_name=b'Price 14', max_digits=12, blank=True),
        ),
        migrations.AddField(
            model_name='player',
            name='seller_price14',
            field=otree.db.models.CurrencyField(null=True, verbose_name=b'Price 15', max_digits=12, blank=True),
        ),
        migrations.AddField(
            model_name='player',
            name='seller_price15',
            field=otree.db.models.CurrencyField(null=True, verbose_name=b'Price 16', max_digits=12, blank=True),
        ),
        migrations.AddField(
            model_name='player',
            name='seller_price8',
            field=otree.db.models.CurrencyField(null=True, verbose_name=b'Price 9', max_digits=12, blank=True),
        ),
        migrations.AddField(
            model_name='player',
            name='seller_price9',
            field=otree.db.models.CurrencyField(null=True, verbose_name=b'Price 10', max_digits=12, blank=True),
        ),
        migrations.AddField(
            model_name='player',
            name='seller_selected',
            field=otree.db.models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='buyer_choice',
            field=otree.db.models.PositiveIntegerField(blank=True, null=True, verbose_name=b'And you will', choices=[(0, b'Buy from seller 1'), (1, b'Buy from seller 2')]),
        ),
        migrations.AlterField(
            model_name='player',
            name='seller_price0',
            field=otree.db.models.CurrencyField(null=True, verbose_name=b'Price 1', max_digits=12, blank=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='seller_price1',
            field=otree.db.models.CurrencyField(null=True, verbose_name=b'Price 2', max_digits=12, blank=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='seller_price2',
            field=otree.db.models.CurrencyField(null=True, verbose_name=b'Price 3', max_digits=12, blank=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='seller_price3',
            field=otree.db.models.CurrencyField(null=True, verbose_name=b'Price 4', max_digits=12, blank=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='seller_price4',
            field=otree.db.models.CurrencyField(null=True, verbose_name=b'Price 5', max_digits=12, blank=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='seller_price5',
            field=otree.db.models.CurrencyField(null=True, verbose_name=b'Price 6', max_digits=12, blank=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='seller_price6',
            field=otree.db.models.CurrencyField(null=True, verbose_name=b'Price 7', max_digits=12, blank=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='seller_price7',
            field=otree.db.models.CurrencyField(null=True, verbose_name=b'Price 8', max_digits=12, blank=True),
        ),
    ]
