# Generated by Django 5.1.6 on 2025-07-11 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_remove_marketticker_news_market_symbol_f5c3f5_idx_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='marketticker',
            name='currency',
            field=models.CharField(choices=[('AED', 'United Arab Emirates Dirham'), ('AUD', 'Australian Dollar'), ('BRL', 'Brazilian Real'), ('CAD', 'Canadian Dollar'), ('CHF', 'Swiss Franc'), ('CLP', 'Chilean Peso'), ('CNY', 'Chinese Yuan'), ('CZK', 'Czech Koruna'), ('EUR', 'Euro'), ('GBP', 'British Pound'), ('HKD', 'Hong Kong Dollar'), ('HUF', 'Hungarian Forint'), ('IDR', 'Indonesian Rupiah'), ('ILS', 'Israeli New Shekel'), ('INR', 'Indian Rupee'), ('JPY', 'Japanese Yen'), ('KRW', 'South Korean Won'), ('MXN', 'Mexican Peso'), ('MYR', 'Malaysian Ringgit'), ('NOK', 'Norwegian Krone'), ('NZD', 'New Zealand Dollar'), ('PHP', 'Philippine Peso'), ('PKR', 'Pakistani Rupee'), ('PLN', 'Polish Zloty'), ('RUB', 'Russian Ruble'), ('SAR', 'Saudi Riyal'), ('SEK', 'Swedish Krona'), ('SGD', 'Singapore Dollar'), ('THB', 'Thai Baht'), ('TRY', 'Turkish Lira'), ('USD', 'US Dollar'), ('VND', 'Vietnamese Dong'), ('ZAR', 'South African Rand'), ('ZIG', 'Zimbabwean Dollar')], default='USD', help_text='Currency code for all monetary values', max_length=3),
        ),
        migrations.AlterField(
            model_name='marketticker',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='Timestamp of record creation'),
        ),
        migrations.AlterField(
            model_name='marketticker',
            name='current_price',
            field=models.DecimalField(decimal_places=2, help_text='Current trading price', max_digits=12),
        ),
        migrations.AlterField(
            model_name='marketticker',
            name='high_52_week',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='52-week high price', max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='marketticker',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Whether the ticker is currently active'),
        ),
        migrations.AlterField(
            model_name='marketticker',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, help_text='Timestamp of last data update'),
        ),
        migrations.AlterField(
            model_name='marketticker',
            name='low_52_week',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='52-week low price', max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='marketticker',
            name='market_cap',
            field=models.BigIntegerField(blank=True, help_text='Market capitalization in currency units', null=True),
        ),
        migrations.AlterField(
            model_name='marketticker',
            name='percentage_change',
            field=models.DecimalField(decimal_places=2, help_text='Percentage change from previous close', max_digits=6),
        ),
        migrations.AlterField(
            model_name='marketticker',
            name='price_change',
            field=models.DecimalField(decimal_places=2, help_text='Net price change from previous close', max_digits=10),
        ),
        migrations.AlterField(
            model_name='marketticker',
            name='volume',
            field=models.BigIntegerField(default=0, help_text='Total shares traded today'),
        ),
        migrations.AddIndex(
            model_name='marketticker',
            index=models.Index(fields=['symbol'], name='news_market_symbol_f5c3f5_idx'),
        ),
        migrations.AddIndex(
            model_name='marketticker',
            index=models.Index(fields=['exchange'], name='news_market_exchang_cb4a30_idx'),
        ),
    ]
