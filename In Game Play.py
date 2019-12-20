from bs4 import BeautifulSoup
### CODE FOR SCRAPING DATA FROM BOVADA
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import pandas as pd
import time 

SOURCE_URL = 'https://www.bovada.lv/sports/basketball/nba/memphis-grizzlies-cleveland-cavaliers-201912201900'


#This example requires Selenium WebDriver 3.13 or newer
with webdriver.Chrome() as driver:
    row_counter = 0
    end_counter = 5000
    while row_counter < end_counter:
        start_time = time.time()
        wait = WebDriverWait(driver, 10) 
        # navigates to a link
        driver.get(SOURCE_URL)
        # gets the html for the webpage
            
        html = driver.execute_script('return document.documentElement.outerHTML')

        soup_html = BeautifulSoup(html)
        
        # Extracts values from source tags and returns them in a new list
        def extractor(attr_list):
            new_list = []
            for item in attr_list:
                item = item.contents
                item = item[0]
                new_list.append(item)
            return new_list

        # Both team names
        team_names = soup_html.findAll('span','name')
        team_names = extractor(team_names)

        # All spread market lines
        spread_market_line = soup_html.findAll('span','market-line bet-handicap')
        spread_market_line = extractor(spread_market_line)

        # Bet prices
        bet_prices = soup_html.findAll('span','bet-price')
        bet_prices = extractor(bet_prices)

        # over unders
        over_unders = soup_html.findAll('span','market-line bet-handicap both-handicaps') 
        over_unders = extractor(over_unders)

        print('Team names:')
        print(team_names)

        print('Spread market lines:')
        print(spread_market_line)
        
        print('Bet Prices:')
        print(bet_prices)

        print('Over unders:')
        print(over_unders)
        
        main_df_cols = ['team_one',
            'team_two',
            'team_one_spread_line',
            'team_two_spread_line',
            'team_one_spread_price',
            'team_two_spread_price',
            'team_one_bet_price',
            'team_two_bet_price',
            'team_one_ou',
            'team_one_ou_val',
            'team_two_ou',
            'team_two_ou_val'
            ]

        # Creates dataframe from the webpage data
        main_df = pd.DataFrame(columns=main_df_cols)

        main_df.at[row_counter, main_df_cols[0] ] = team_names[0]
        main_df.at[row_counter, main_df_cols[1]] = team_names[1]
        main_df.at[row_counter, main_df_cols[2] ] = spread_market_line[0]
        main_df.at[row_counter, main_df_cols[3] ] = spread_market_line[1]
        # spread prices and money-line prices are both in bet_prices
        main_df.at[row_counter, main_df_cols[4] ] = bet_prices[0]
        main_df.at[row_counter, main_df_cols[5] ] = bet_prices[1]
        main_df.at[row_counter, main_df_cols[4] ] = bet_prices[2]
        main_df.at[row_counter, main_df_cols[5] ] = bet_prices[3]
        main_df.at[row_counter, main_df_cols[6] ] = over_unders[0]
        main_df.at[row_counter, main_df_cols[7] ] = over_unders[1]
        main_df.at[row_counter, main_df_cols[8] ] = over_unders[2]
        main_df.at[row_counter, main_df_cols[9] ] = over_unders[3]
        
        new_time = time.time() - start_time
        delay_time = 5 - new_time
        time.sleep(delay_time) # times the program to run exactly every 5 seconds
        row_counter += 1


main_df.write_csv('in game data.csv')
    

