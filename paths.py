from decimal import Decimal
from collections import namedtuple


Hub = namedtuple('Hub', ['name', 'currency'])
Hub.__str__ = lambda self: f'Hub({self.name})'
Institution = namedtuple('Institution', ['name', 'accounts', 'exchanges'])
Account = namedtuple('Account', ['institution', 'name', 'currency', 'recieve', 'send'])
Account.__str__ = lambda self: f'Account({self.institution} {self.name})'
Exchange = namedtuple('Exchange', ['source', 'destination', 'buy', 'sell'])
Config = namedtuple('Config', ['currencies', 'hubs', 'institutions'])

config = Config(
    currencies=['zar', 'usd', 'btc'],
    hubs={
        'usd-cheque-card': Hub(name='usd-cheque-card', currency='usd'),
        'zar-eft': Hub(name='zar-eft', currency='zar'),
        'usd-iban-transfer': Hub('usd-iban-transfer', currency='usd'),
        'btc-transfer': Hub(name='btc-transfer', currency='btc'),
    },
    institutions={
        'fnb': Institution(
            name='fnb',
            accounts={
                'cheque': Account(
                    institution='fnb',
                    name='cheque',
                    currency='zar',
                    recieve=('zar-eft', ),
                    send=('zar-eft', 'usd-cheque-card', )
                )
            },
            exchanges=[],
        ),
        'luno': Institution(
            name='luno',
            accounts={
                'zar-wallet': Account(
                    institution='luno',
                    name='zar-wallet',
                    currency='zar',
                    recieve=('zar-eft', ),
                    send=('zar-eft', ),
                ),
                'btc-wallet': Account(
                    institution='luno',
                    name='btc-wallet',
                    currency='btc',
                    recieve=('btc-transfer', ),
                    send=('btc-transfer', ),
                )
            },
            exchanges=[
                Exchange('zar-wallet', 'btc-wallet', Decimal(1), Decimal(1))
            ]
        ),
        'cex': Institution(
            name='cex',
            accounts={
                'usd-wallet': Account(
                    institution='cex',
                    name='usd-wallet',
                    currency='btc',
                    recieve=('usd-cheque-card', ),
                    send=('usd-iban-transfer', ),
                ),
                'btc-wallet': Account(
                    institution='cex',
                    name='btc-wallet',
                    currency='btc',
                    recieve=('btc-transfer', ),
                    send=('btc-transfer', )
                )
            },
            exchanges=[
                Exchange('usd-wallet', 'btc-wallet', Decimal(1), Decimal(1))
            ]
        )
    },
)


class Leg(object):
    def __init__(self, source, destination):
        pass


class Plan(object):
    def __init__(self, legs):
        pass


import networkx as nx
import matplotlib.pyplot as plt


def get_paths():
    graph = nx.Graph()
    for institution in config.institutions.values():
        for account in institution.accounts.values():
            for hub_name in account.send:
                hub = config.hubs[hub_name]
                print(f'linking {account.institution}-{account.name} => {hub.name}')
                graph.add_edge(account, hub)
        for account in institution.accounts.values():
            for hub_name in account.recieve:
                hub = config.hubs[hub_name]
                print(f'linking {account.institution}-{account.name} <= {hub.name}')
                graph.add_edge(hub, account)
        for exchange in institution.exchanges:
            source = institution.accounts[exchange.source]
            destination = institution.accounts[exchange.destination]
            graph.add_edge(source, destination)
    # plt.subplot(121)
    nx.draw(graph, with_labels=True, font_weight='bold')
    plt.show()


if __name__ == '__main__':
    get_paths()
