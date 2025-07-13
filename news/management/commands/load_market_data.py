from django.core.management.base import BaseCommand
from news.models import MarketTicker, Commodity, Cryptocurrency


class Command(BaseCommand):
    help = 'Load sample market data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Loading sample market data...')
        
        # Sample Market Tickers
        market_tickers = [
            {
                'symbol': 'AAPL',
                'company_name': 'Apple Inc.',
                'exchange': 'NASDAQ',
                'current_price': 178.25,
                'price_change': 2.15,
                'percentage_change': 1.22,
                'volume': 45234567,
                'market_cap': 2800000000000,
                'high_52_week': 198.23,
                'low_52_week': 124.17,
            },
            {
                'symbol': 'GOOGL',
                'company_name': 'Alphabet Inc.',
                'exchange': 'NASDAQ',
                'current_price': 142.56,
                'price_change': -1.23,
                'percentage_change': -0.86,
                'volume': 28567234,
                'market_cap': 1750000000000,
                'high_52_week': 151.55,
                'low_52_week': 83.34,
            },
            {
                'symbol': 'TSLA',
                'company_name': 'Tesla Inc.',
                'exchange': 'NASDAQ',
                'current_price': 245.67,
                'price_change': 8.45,
                'percentage_change': 3.56,
                'volume': 67890123,
                'market_cap': 780000000000,
                'high_52_week': 414.50,
                'low_52_week': 101.81,
            },
            {
                'symbol': 'MSFT',
                'company_name': 'Microsoft Corporation',
                'exchange': 'NASDAQ',
                'current_price': 378.85,
                'price_change': 4.22,
                'percentage_change': 1.13,
                'volume': 34567890,
                'market_cap': 2800000000000,
                'high_52_week': 384.30,
                'low_52_week': 213.43,
            },
            {
                'symbol': 'NVDA',
                'company_name': 'NVIDIA Corporation',
                'exchange': 'NASDAQ',
                'current_price': 421.32,
                'price_change': 12.87,
                'percentage_change': 3.15,
                'volume': 87654321,
                'market_cap': 1000000000000,
                'high_52_week': 502.66,
                'low_52_week': 108.13,
            }
        ]
        
        for ticker_data in market_tickers:
            ticker, created = MarketTicker.objects.get_or_create(
                symbol=ticker_data['symbol'],
                defaults=ticker_data
            )
            if created:
                self.stdout.write(f'Created market ticker: {ticker.symbol}')
            else:
                # Update existing ticker
                for key, value in ticker_data.items():
                    setattr(ticker, key, value)
                ticker.save()
                self.stdout.write(f'Updated market ticker: {ticker.symbol}')
        
        # Sample Commodities
        commodities = [
            {
                'name': 'Gold',
                'symbol': 'XAU',
                'unit': 'oz',
                'current_price': 1987.45,
                'price_change': 13.27,
                'percentage_change': 0.67,
                'exchange': 'COMEX',
                'high_52_week': 2067.15,
                'low_52_week': 1810.20,
            },
            {
                'name': 'Silver',
                'symbol': 'XAG',
                'unit': 'oz',
                'current_price': 24.78,
                'price_change': -0.31,
                'percentage_change': -1.23,
                'exchange': 'COMEX',
                'high_52_week': 26.41,
                'low_52_week': 20.15,
            },
            {
                'name': 'Crude Oil (WTI)',
                'symbol': 'WTI',
                'unit': 'barrel',
                'current_price': 78.45,
                'price_change': 1.65,
                'percentage_change': 2.14,
                'exchange': 'NYMEX',
                'high_52_week': 123.70,
                'low_52_week': 66.74,
            },
            {
                'name': 'Natural Gas',
                'symbol': 'NG',
                'unit': 'MMBtu',
                'current_price': 2.87,
                'price_change': -0.15,
                'percentage_change': -4.97,
                'exchange': 'NYMEX',
                'high_52_week': 9.68,
                'low_52_week': 1.93,
            },
            {
                'name': 'Copper',
                'symbol': 'HG',
                'unit': 'lb',
                'current_price': 3.87,
                'price_change': 0.02,
                'percentage_change': 0.52,
                'exchange': 'COMEX',
                'high_52_week': 4.79,
                'low_52_week': 3.33,
            }
        ]
        
        for commodity_data in commodities:
            commodity, created = Commodity.objects.get_or_create(
                name=commodity_data['name'],
                defaults=commodity_data
            )
            if created:
                self.stdout.write(f'Created commodity: {commodity.name}')
            else:
                # Update existing commodity
                for key, value in commodity_data.items():
                    setattr(commodity, key, value)
                commodity.save()
                self.stdout.write(f'Updated commodity: {commodity.name}')
        
        # Sample Cryptocurrencies
        cryptocurrencies = [
            {
                'name': 'Bitcoin',
                'symbol': 'BTC',
                'current_price': 43567.89,
                'price_change': 1456.78,
                'percentage_change': 3.45,
                'market_cap': 855000000000,
                'volume_24h': 18500000000,
                'circulating_supply': 19600000,
                'total_supply': 21000000,
                'ath': 69045.00,
                'atl': 67.81,
            },
            {
                'name': 'Ethereum',
                'symbol': 'ETH',
                'current_price': 2567.23,
                'price_change': 47.65,
                'percentage_change': 1.89,
                'market_cap': 308000000000,
                'volume_24h': 12000000000,
                'circulating_supply': 120000000,
                'total_supply': None,
                'ath': 4878.26,
                'atl': 0.432979,
            },
            {
                'name': 'Tether',
                'symbol': 'USDT',
                'current_price': 1.0001,
                'price_change': 0.0001,
                'percentage_change': 0.01,
                'market_cap': 91000000000,
                'volume_24h': 45000000000,
                'circulating_supply': 91000000000,
                'total_supply': 91000000000,
                'ath': 1.21,
                'atl': 0.572521,
            },
            {
                'name': 'Binance Coin',
                'symbol': 'BNB',
                'current_price': 234.56,
                'price_change': -1.85,
                'percentage_change': -0.78,
                'market_cap': 36000000000,
                'volume_24h': 650000000,
                'circulating_supply': 153000000,
                'total_supply': 200000000,
                'ath': 686.31,
                'atl': 0.0398177,
            },
            {
                'name': 'Solana',
                'symbol': 'SOL',
                'current_price': 67.89,
                'price_change': 2.34,
                'percentage_change': 3.57,
                'market_cap': 29000000000,
                'volume_24h': 1200000000,
                'circulating_supply': 427000000,
                'total_supply': 571000000,
                'ath': 259.96,
                'atl': 0.500801,
            }
        ]
        
        for crypto_data in cryptocurrencies:
            crypto, created = Cryptocurrency.objects.get_or_create(
                symbol=crypto_data['symbol'],
                defaults=crypto_data
            )
            if created:
                self.stdout.write(f'Created cryptocurrency: {crypto.name}')
            else:
                # Update existing cryptocurrency
                for key, value in crypto_data.items():
                    setattr(crypto, key, value)
                crypto.save()
                self.stdout.write(f'Updated cryptocurrency: {crypto.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully loaded sample market data!')
        )
