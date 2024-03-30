# Imports
import requests
from datetime import date, datetime

key = 'API-KEY'

today_date = str(date.today())

bonus_bet_amount = float(input('Please set your bonus bet amount: '))
max_days = int(input('Please select the max amount of days to search: '))
min_profit = int(input('Please enter the minimum percentage of profit: '))

sports = requests.get(f'https://api.the-odds-api.com/v4/sports/?apiKey={key}')
sports = sports.json()


# Collecting all sports and odds
for sport in sports:
    sport = sport['key']
    odds = requests.get(f'https://api.the-odds-api.com/v4/sports/{sport}/odds/?regions=au&markets=h2h&apiKey={key}')
    odds = odds.json()

    # If there are no odds for that sport
    if 'message' in odds:
        continue

    for sports in odds:
        head1_prices_list = []
        head2_prices_list = []
        head1_betfair_prices_list = []
        head2_betfair_prices_list = []

        sport = sports['sport_key']
        head1_name = sports['away_team']
        head2_name = sports['home_team']

        start_date = sports['commence_time']
        start_date = start_date.split('T', 1)[0]
        d1 = datetime.strptime(start_date, "%Y-%m-%d")
        d2 = datetime.strptime(today_date, "%Y-%m-%d")
        days = abs((d2 - d1).days)

        if days <= max_days:

            bookmakers = sports['bookmakers']

            if len(bookmakers) == 0:
                continue
            for bookmaker in bookmakers:
                bookie = bookmaker['key']
                markets = bookmaker['markets']

                for market in markets:
                    prices_temp_list = []
                    betfair_prices_temp_list = []
                    outcomes = market['outcomes']

                    for outcome in outcomes:
                        price = outcome['price']
                        if bookie == 'betfair_ex_au':
                            betfair_prices_temp_list.append(price)
                        else:
                            prices_temp_list.append(price)

                    if len(betfair_prices_temp_list) != 0:
                        head1_betfair_prices_list.extend((betfair_prices_temp_list[0], bookie))
                        head2_betfair_prices_list.extend((betfair_prices_temp_list[1], bookie))
                    else:
                        head1_prices_list.extend((prices_temp_list[0], bookie))
                        head2_prices_list.extend((prices_temp_list[1], bookie))

            # Head 1
            # Finding lay price
            if len(head1_betfair_prices_list) != 0:
                lay_price = head1_betfair_prices_list[2]

                # Finding Arbitrage
                for iteration in range(2, len(head1_prices_list), 2):
                    # Calculations
                    price = head1_prices_list[iteration - 2]
                    bookmaker = head1_prices_list[iteration - 1]
                    strategy = ((price - 1) / lay_price) * bonus_bet_amount
                    liability = (lay_price * strategy) - strategy

                    if strategy > (min_profit / 100) * bonus_bet_amount:
                        print('Sport:', sport, '\n', 'Days:', days, '\n', 'Team:', head1_name, '\n', 'Bookmaker 1:',
                              bookmaker, '\n', 'Price:', price, '\n', 'Bookmaker 2: Betfair', '\n',
                              'Price:',
                              lay_price, '\n', bookmaker, 'Strategy:', bonus_bet_amount, '\n',
                              'Betfair Strategy:', strategy,
                              '\n', 'Liability:', liability, '\n', 'Profit:', strategy, '\n')

            # Head 2
            # Finding lay price
            if len(head2_betfair_prices_list) != 0:
                lay_price = head2_betfair_prices_list[2]

                # Finding Arbitrage
                for iteration in range(2, len(head2_prices_list), 2):
                    # Calculations
                    price = head2_prices_list[iteration - 2]
                    bookmaker = head2_prices_list[iteration - 1]
                    strategy = ((price - 1) / lay_price) * bonus_bet_amount
                    liability = (lay_price * strategy) - strategy

                    if strategy > (min_profit / 100) * bonus_bet_amount:
                        print('Sport:', sport, '\n', 'Days:', days, '\n', 'Team:', head2_name, '\n',
                              'Bookmaker 1:',
                              bookmaker, '\n', 'Price:', price, '\n', 'Bookmaker 2: Betfair', '\n',
                              'Price:',
                              lay_price, '\n', bookmaker, 'Strategy:', bonus_bet_amount, '\n',
                              'Betfair Strategy:', strategy,
                              '\n', 'Liability:', liability, '\n', 'Profit:', strategy, '\n')
