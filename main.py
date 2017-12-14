import pricing


def main():
    prices = pricing.get_prices()
    pricing.sanity_check(prices)

if __name__ == '__main__':
    main()
