# Imports
import requests
from datetime import date, datetime

key = 'API-KEY'

today_date = str(date.today())

bonus_bet_amount = float(input('Please set your bonus bet amount: '))
max_days = int(input('Please select the max amount of days to search: '))
min_profit = int(input('Please enter the minimum percentage of profit: '))
bookie_filter = input('Please enter the bookie: ')
max_liability = int(input('Please enter the maximum liability: '))


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
        draw_prices_list = []
        betfair_head1_prices_list = []
        betfair_head2_prices_list = []
        betfair_draw_prices_list = []

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
                        # If there are draw prices
                        if len(betfair_prices_temp_list) == 3:
                            betfair_draw_prices_list.extend((betfair_prices_temp_list[2], bookie))
                        betfair_head1_prices_list.extend((betfair_prices_temp_list[1], bookie))
                        betfair_head2_prices_list.extend((betfair_prices_temp_list[0], bookie))

                    else:
                        if len(prices_temp_list) == 3:
                            draw_prices_list.extend((prices_temp_list[2], bookie))
                        head1_prices_list.extend((prices_temp_list[1], bookie))
                        head2_prices_list.extend((prices_temp_list[0], bookie))

            # Head 1
            # Finding lay price
            if len(betfair_head1_prices_list) != 0:
                lay_price = betfair_head1_prices_list[2]
                name = head1_name + ' vs ' + head2_name

                # Finding Arbitrage
                for iteration in range(2, len(head1_prices_list), 2):
                    # Calculations
                    price = head1_prices_list[iteration - 2]
                    bookmaker = head1_prices_list[iteration - 1]

                    if bookie_filter == '' or bookmaker == bookie_filter:
                        strategy = ((price - 1) / lay_price) * bonus_bet_amount
                        liability = (lay_price * strategy) - strategy

                        if liability < max_liability:
                            if strategy > (min_profit / 100) * bonus_bet_amount:
                                print('Sport:', sport, '\n', 'Days:', days, '\n', 'Game:', name, '\n', 'Bookmaker 1:',
                                      bookmaker, '\n', 'Price:', price, '\n', 'Betfair:', '\n',
                                      'Price:',
                                      lay_price, '\n', bookmaker, 'Strategy:', bonus_bet_amount, '\n',
                                      'Backers Stake:', strategy,
                                      '\n', 'Liability:', liability, '\n', 'Profit:', strategy, '\n')

            # Head 2
            if len(betfair_head2_prices_list) != 0:
                lay_price = betfair_head2_prices_list[2]
                name = head1_name + ' vs ' + head2_name

                for iteration in range(2, len(head2_prices_list), 2):
                    price = head2_prices_list[iteration - 2]
                    bookmaker = head2_prices_list[iteration - 1]

                    if bookie_filter == '' or bookmaker == bookie_filter:
                        strategy = ((price - 1) / lay_price) * bonus_bet_amount
                        liability = (lay_price * strategy) - strategy

                        if liability < max_liability:
                            if strategy > (min_profit / 100) * bonus_bet_amount:
                                print('Sport:', sport, '\n', 'Days:', days, '\n', 'Game:', name, '\n',
                                      'Bookmaker 1:',
                                      bookmaker, '\n', 'Price:', price, '\n', 'Betfair:', '\n',
                                      'Price:',
                                      lay_price, '\n', bookmaker, 'Strategy:', bonus_bet_amount, '\n',
                                      'Backers Stake:', strategy,
                                      '\n', 'Liability:', liability, '\n', 'Profit:', strategy, '\n')

            # Draw
            if len(betfair_draw_prices_list) != 0:
                lay_price = betfair_draw_prices_list[2]
                name = head1_name + ' vs ' + head2_name + ' Draw'

                for iteration in range(2, len(draw_prices_list), 2):
                    price = draw_prices_list[iteration - 2]
                    bookmaker = draw_prices_list[iteration - 1]

                    if bookie_filter == '' or bookmaker == bookie_filter:
                        strategy = ((price - 1) / lay_price) * bonus_bet_amount
                        liability = (lay_price * strategy) - strategy

                        if liability < max_liability:
                            if strategy > (min_profit / 100) * bonus_bet_amount:
                                print('Sport:', sport, '\n', 'Days:', days, '\n', 'Game:', name, '\n',
                                      'Bookmaker 1:',
                                      bookmaker, '\n', 'Price:', price, '\n', 'Betfair:', '\n',
                                      'Price:',
                                      lay_price, '\n', bookmaker, 'Strategy:', bonus_bet_amount, '\n',
                                      'Backers Stake:', strategy,
                                      '\n', 'Liability:', liability, '\n', 'Profit:', strategy, '\n')
