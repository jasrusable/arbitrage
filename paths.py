from decimal import Decimal
from collections import namedtuple, defaultdict


Hub = namedtuple('Hub', ['name', 'currency'])
Institution = namedtuple('Institution', ['name', 'accounts'])
Account = namedtuple('Account', ['institution', 'name', 'currency', 'recieve', 'send'])
Config = namedtuple('Config', ['currencies', 'hubs', 'institutions', 'pairs'])
Pair = namedtuple('Pair', ['institution', 'account', 'hub', 'rate'])

config = Config(
    currencies=['zar', 'usd', 'btc'],
    hubs={
        'usd-cheque-card': Hub(name='usd-cheque-card', currency='usd'),
        'zar-eft': Hub(name='zar-eft', currency='zar'),
        'usd-iban-transfer': Hub('iban-transfer', currency='usd'),
        'btc-transfer': Hub(name='btc-transfer', currency='btc'),
    },
    institutions={
        'fnb': Institution(
            name='fnb',
            accounts=[
                Account(
                    institution='fnb',
                    name='cheque',
                    currency='zar',
                    recieve=('eft', ),
                    send=('eft', 'usd-cheque-card', )
                )
            ]
        ),
        'luno': Institution(
            name='luno',
            accounts=[
                Account(
                    institution='luno',
                    name='btc-wallet',
                    currency='btc',
                    recieve=('btc-transfer', ),
                    send=('btc-transfer', ),
                ),
                Account(
                    institution='luno',
                    name='zar-wallet',
                    currency='zar',
                    recieve=('eft', ),
                    send=('eft', ),
                )
            ]
        ),
        'cex': Institution(
            name='cex',
            accounts=[
                Account(
                    institution='cex',
                    name='btc-wallet',
                    currency='btc',
                    recieve=('btc-transfer', ),
                    send=('btc-transfer', )
                ),
                Account(
                    institution='cex',
                    name='usd-wallet',
                    currency='btc',
                    recieve=('cheque-card', ),
                    send=('iban-transfer', ),
                )
            ]
        )
    },
    pairs=[
        Pair('fnb', 'cheque', 'usd-cheque-card', Decimal(0.1)),
    ]
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
    hubs = defaultdict(lambda: set())
    for institution in config.institutions.values():
        for account in institution.accounts:
            for hub in account.send:
                print(f'linking {account.institution}-{account.name} => {hub}')
                graph.add_nodes_from([account, hub])
                graph.add_edge(account, hub)
        for account in institution.accounts:
            for hub in account.recieve:
                print(f'linking {account.institution}-{account.name} <= {hub}')
                graph.add_nodes_from([account, hub])
                graph.add_edge(hub, account)
    # plt.subplot(121)
    nx.draw(graph, with_labels=True, font_weight='bold')
    plt.show()


if __name__ == '__main__':
    get_paths()
