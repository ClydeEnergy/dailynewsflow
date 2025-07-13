from django.core.management.base import BaseCommand
from news.models import MarketTicker, Commodity, Cryptocurrency
from decimal import Decimal


class Command(BaseCommand):
    help = 'Load sample market data for testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Loading sample market data...'))

        # Sample Market Tickers
        market_tickers = [
            {
                'symbol': 'SPX',
                'company_name': 'S&P 500',
                'exchange': 'NYSE',
                'current_price': Decimal('4567.23'),
                'price_change': Decimal('25.67'),
                'percentage_change': Decimal('1.24'),
                'volume': 2500000000,
                'market_cap': 45000000000000,
                'high_52_week': Decimal('4800.00'),
                'low_52_week': Decimal('3900.00'),
            },
            {
                'symbol': 'IXIC',
                'company_name': 'NASDAQ Composite',
                'exchange': 'NASDAQ',
                'current_price': Decimal('14234.56'),
                'price_change': Decimal('89.45'),
                'percentage_change': Decimal('0.89'),
                'volume': 1800000000,
                'market_cap': 20000000000000,
                'high_52_week': Decimal('15000.00'),
                'low_52_week': Decimal('12000.00'),
            },
            {
                'symbol': 'DJI',
                'company_name': 'Dow Jones Industrial Average',
                'exchange': 'NYSE',
                'current_price': Decimal('35678.90'),
                'price_change': Decimal('-45.23'),
                'percentage_change': Decimal('-0.34'),
                'volume': 800000000,
                'market_cap': 12000000000000,
                'high_52_week': Decimal('37000.00'),
                'low_52_week': Decimal('32000.00'),
            },
            {
                'symbol': 'UKX',
                'company_name': 'FTSE 100',
                'exchange': 'LSE',
                'current_price': Decimal('7456.78'),
                'price_change': Decimal('34.56'),
                'percentage_change': Decimal('0.56'),
                'volume': 450000000,
                'market_cap': 2500000000000,
                'high_52_week': Decimal('7800.00'),
                'low_52_week': Decimal('6800.00'),
            },
            {
                'symbol': 'N225',
                'company_name': 'Nikkei 225',
                'exchange': 'TSE',
                'current_price': Decimal('33245.67'),
                'price_change': Decimal('234.89'),
                'percentage_change': Decimal('1.12'),
                'volume': 650000000,
                'market_cap': 6500000000000,
                'high_52_week': Decimal('35000.00'),
                'low_52_week': Decimal('28000.00'),
            },
        ]

        for ticker_data in market_tickers:
            ticker, created = MarketTicker.objects.get_or_create(
                symbol=ticker_data['symbol'],
                defaults=ticker_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created market ticker: {ticker.symbol}')
                )
            else:
                # Update existing ticker with new data
                for key, value in ticker_data.items():
                    setattr(ticker, key, value)
                ticker.save()
                self.stdout.write(
                    self.style.WARNING(f'Updated market ticker: {ticker.symbol}')
                )

        # Sample Commodities
        commodities = [
            {
                'name': 'Gold',
                'symbol': 'XAU',
                'unit': 'oz',
                'current_price': Decimal('1987.45'),
                'price_change': Decimal('12.34'),
                'percentage_change': Decimal('0.67'),
                'exchange': 'COMEX',
                'high_52_week': Decimal('2100.00'),
                'low_52_week': Decimal('1800.00'),
            },
            {
                'name': 'Silver',
                'symbol': 'XAG',
                'unit': 'oz',
                'current_price': Decimal('24.78'),
                'price_change': Decimal('-0.45'),
                'percentage_change': Decimal('-1.23'),
                'exchange': 'COMEX',
                'high_52_week': Decimal('30.00'),
                'low_52_week': Decimal('20.00'),
            },
            {
                'name': 'Crude Oil WTI',
                'symbol': 'WTI',
                'unit': 'barrel',
                'current_price': Decimal('78.45'),
                'price_change': Decimal('1.67'),
                'percentage_change': Decimal('2.14'),
                'exchange': 'NYMEX',
                'high_52_week': Decimal('95.00'),
                'low_52_week': Decimal('65.00'),
            },
            {
                'name': 'Natural Gas',
                'symbol': 'NG',
                'unit': 'MMBtu',
                'current_price': Decimal('3.45'),
                'price_change': Decimal('-0.12'),
                'percentage_change': Decimal('-1.45'),
                'exchange': 'NYMEX',
                'high_52_week': Decimal('6.00'),
                'low_52_week': Decimal('2.50'),
            },
            {
                'name': 'Copper',
                'symbol': 'HG',
                'unit': 'lb',
                'current_price': Decimal('3.89'),
                'price_change': Decimal('0.08'),
                'percentage_change': Decimal('0.78'),
                'exchange': 'COMEX',
                'high_52_week': Decimal('4.50'),
                'low_52_week': Decimal('3.20'),
            },
        ]

        for commodity_data in commodities:
            commodity, created = Commodity.objects.get_or_create(
                symbol=commodity_data['symbol'],
                defaults=commodity_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created commodity: {commodity.name}')
                )
            else:
                # Update existing commodity with new data
                for key, value in commodity_data.items():
                    setattr(commodity, key, value)
                commodity.save()
                self.stdout.write(
                    self.style.WARNING(f'Updated commodity: {commodity.name}')
                )

        # Sample Cryptocurrencies
        cryptocurrencies = [
            {
                'name': 'Bitcoin',
                'symbol': 'BTC',
                'current_price': Decimal('43567.89'),
                'price_change': Decimal('1234.56'),
                'percentage_change': Decimal('3.45'),
                'market_cap': 850000000000,
                'volume_24h': 25000000000,
                'circulating_supply': 19500000,
                'total_supply': 21000000,
                'ath': Decimal('69000.00'),
                'atl': Decimal('3200.00'),
            },
            {
                'name': 'Ethereum',
                'symbol': 'ETH',
                'current_price': Decimal('2567.23'),
                'price_change': Decimal('45.67'),
                'percentage_change': Decimal('1.89'),
                'market_cap': 308000000000,
                'volume_24h': 15000000000,
                'circulating_supply': 120000000,
                'total_supply': 120000000,
                'ath': Decimal('4800.00'),
                'atl': Decimal('8.00'),
            },
            {
                'name': 'Binance Coin',
                'symbol': 'BNB',
                'current_price': Decimal('234.56'),
                'price_change': Decimal('-1.89'),
                'percentage_change': Decimal('-0.78'),
                'market_cap': 36000000000,
                'volume_24h': 2000000000,
                'circulating_supply': 153000000,
                'total_supply': 200000000,
                'ath': Decimal('690.00'),
                'atl': Decimal('0.10'),
            },
            {
                'name': 'Cardano',
                'symbol': 'ADA',
                'current_price': Decimal('0.45'),
                'price_change': Decimal('0.02'),
                'percentage_change': Decimal('2.34'),
                'market_cap': 15000000000,
                'volume_24h': 800000000,
                'circulating_supply': 35000000000,
                'total_supply': 45000000000,
                'ath': Decimal('3.10'),
                'atl': Decimal('0.02'),
            },
            {
                'name': 'Solana',
                'symbol': 'SOL',
                'current_price': Decimal('89.45'),
                'price_change': Decimal('4.56'),
                'percentage_change': Decimal('5.67'),
                'market_cap': 38000000000,
                'volume_24h': 3200000000,
                'circulating_supply': 400000000,
                'total_supply': 500000000,
                'ath': Decimal('260.00'),
                'atl': Decimal('0.50'),
            },
        ]

        for crypto_data in cryptocurrencies:
            crypto, created = Cryptocurrency.objects.get_or_create(
                symbol=crypto_data['symbol'],
                defaults=crypto_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created cryptocurrency: {crypto.name}')
                )
            else:
                # Update existing cryptocurrency with new data
                for key, value in crypto_data.items():
                    setattr(crypto, key, value)
                crypto.save()
                self.stdout.write(
                    self.style.WARNING(f'Updated cryptocurrency: {crypto.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully loaded sample market data!')
        )
