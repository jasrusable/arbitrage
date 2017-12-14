from decimal import Decimal
from collections import namedtuple
import networkx as nx

Pair = namedtuple('Pair', ['have', 'want'])

EXAMPLE_PRICES = {
    'luno': {
        Pair('rand', 'btc'): Decimal('245000'),
        Pair('btc', 'rand'): Decimal('0.00004')
    },
    'fnb': {
        Pair('rand', 'usd'): Decimal('0.1'),
        Pair('usd', 'rand'): Decimal('11'),
    }
}


def get_prices():
    for institution, pairs in prices.items():
        for pair, price in pairs.items():


def raise_if_negative_cycle(prices):
            reverse = Pair(pair.want, pair.have)
            reverse_price = prices[institution].get(reverse)
            if reverse_price and price * reverse_price < 1:
                raise ValueError(f'Insane cycle {pair}={price} {reverse}={reverse_price}')


def sanity_check(prices):
    raise_if_negative_cycle(prices)
