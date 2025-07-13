from django.db.models import Q
from .models import MarketTicker, ExchangeRate, Commodity, Cryptocurrency


def market_data(request):
    """
    Context processor to provide market data globally for the ticker
    """
    try:
        # Get market tickers for the top ticker
        market_tickers = MarketTicker.objects.filter(is_active=True).order_by('symbol')[:5]
        
        # Get exchange rates 
        exchange_rates = ExchangeRate.objects.filter(is_active=True).order_by('base_currency', 'quote_currency')[:3]
        
        # Get commodities
        commodities = Commodity.objects.filter(is_active=True).order_by('name')[:2]
        
        return {
            'ticker_market_data': market_tickers,
            'ticker_exchange_rates': exchange_rates,
            'ticker_commodities': commodities,
        }
    except Exception:
        # Return empty context if there's any error
        return {
            'ticker_market_data': [],
            'ticker_exchange_rates': [],
            'ticker_commodities': [],
        }
