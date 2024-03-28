# Imports
import requests
from datetime import date, datetime

key = 'API-KEY'

today_date = str(date.today())

bonus_bet_amount = float(input('Please set your bonus bet amount: '))
max_days = int(input('Please select the max amount of days to search: '))

sports = requests.get(f'https://api.the-odds-api.com/v4/sports/?apiKey={key}')
sports = sports.json()


# Collecting all sports and odds
for sport in sports:
    sport = sport['key']
    odds = requests.get(f'https://api.the-odds-api.com/v4/sports/{sport}/odds/?regions=au&markets=h2h&apiKey={key}')
    odds = odds.json()
    print(odds)

    # If there are no odds for that sport
    if 'message' in odds:
        continue

    for sports in odds:
        head1_prices_list = []
        head2_prices_list = []

        sport = sports['sport_key']

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
                    names_temp_list = []
                    betfair_list = []
                    outcomes = market['outcomes']

                    for outcome in outcomes:
                        name = outcome['name']
                        names_temp_list.append(name)
                        price = outcome['price']
                        prices_temp_list.append(price)

                    head1_prices_list.extend((prices_temp_list[0], names_temp_list[0], bookie))
                    head2_prices_list.extend((prices_temp_list[1], names_temp_list[1], bookie))

            # Finding Arbitrage

            # Pre-setting highest odds
            highest_price = head1_prices_list[0]
            name = head1_prices_list[1]
            highest_bookmaker = head1_prices_list[2]

            for iteration, price in enumerate(head1_prices_list):
                if iteration % 3 == 0:
                    if head1_prices_list[iteration + 2] == 'betfair_ex_au':
                        betfair_list.append(price)
                    elif price > highest_price:
                        highest_price = price
                        highest_bookmaker = head1_prices_list[iteration + 2]

            if len(betfair_list) > 0:
                lay_price = betfair_list[0]
                for price in betfair_list:
                    if price > lay_price:
                        lay_price = price

                # Calculations
                strategy = ((highest_price - 1) / lay_price) * bonus_bet_amount
                liability = (lay_price * strategy) - strategy

                if strategy > 0.6 * bonus_bet_amount:
                    print('Sport:', sport, '\n', 'Days:', days, '\n', 'Team:', name, '\n', 'Bookmaker 1:',
                          highest_bookmaker, '\n', 'Price:', highest_price, '\n', 'Bookmaker 2: Betfair', '\n', 'Price:',
                          lay_price, '\n', highest_bookmaker, 'Strategy:', bonus_bet_amount, '\n', 'Betfair Strategy:', strategy,
                          '\n', 'Liability:', liability, '\n', 'Profit:', strategy, '\n')

            betfair_list = []
            highest_price = head2_prices_list[0]
            name = head2_prices_list[1]
            highest_bookmaker = head2_prices_list[2]

            for iteration, price in enumerate(head2_prices_list):
                if iteration % 3 == 0:
                    if head2_prices_list[iteration + 2] == 'betfair_ex_au':
                        betfair_list.append(price)
                    elif price > highest_price:
                        highest_price = price
                        highest_bookmaker = head2_prices_list[iteration + 2]

            if len(betfair_list) > 0:
                lay_price = betfair_list[0]
                for price in betfair_list:
                    if price > lay_price:
                        lay_price = price

                strategy = ((highest_price - 1) / lay_price) * bonus_bet_amount
                liability = (lay_price * strategy) - strategy

                if strategy > 0.6 * bonus_bet_amount:
                    print('Sport:', sport, '\n', 'Days:', days, '\n', 'Team:', name, '\n', 'Bookmaker 1:',
                          highest_bookmaker, '\n', 'Price:', highest_price, '\n', 'Bookmaker 2: Betfair', '\n', 'Price:',
                          lay_price, '\n', highest_bookmaker, 'Strategy:', bonus_bet_amount, '\n', 'Betfair Strategy:', strategy,
                          '\n', 'Liability:', liability, '\n', 'Profit:', strategy, '\n')
