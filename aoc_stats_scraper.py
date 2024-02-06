import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

def collect_yearly_stats(years):
    """
    Outer loop gets day stats and day names, inner loop leaderboard stats
    """
    stats = pd.DataFrame({'date': [], 'both': [], 'one': [], 'name': []})
    leaderboard_stats = pd.DataFrame({'date': [], 'stars': [], 'time': [], 'scored_place': []})

    for year in years:
        print('collecting data for year ' + str(year))
        stats_url = "https://adventofcode.com/" + str(year) + "/stats"
        stats_data = requests.get(stats_url)
        soup = BeautifulSoup(stats_data.text, 'html.parser')
        table = soup.find_all(attrs={'class' : 'stats'})
        for entry in table:
            i = 25
            for line in entry:
                if line == '\n':
                    continue
                info = line.find_all(string=True)

                # dayname 
                dayname_url = "https://adventofcode.com/" + str(year) + "/day/" + str(i)
                dayname_data = requests.get(dayname_url)
                day_soup = BeautifulSoup(dayname_data.text, 'html.parser')
                day_name_list = day_soup.find_all('h2')
                day_name = day_name_list[0].next.replace('--- ', '').replace(' ---', '').split(':')[1]

                temp_df = pd.DataFrame({'date': info[0].strip()+".12."+str(year), 
                                        'both': int(info[1].strip()), 
                                        'one': int(info[3].strip()), 
                                        'name': day_name}, index=[0])
                stats = pd.concat([stats,temp_df],ignore_index=True)
                print(temp_df)

                # leaderboard stats
                lb_url = "https://adventofcode.com/" + str(year) + "/leaderboard/day/" + str(i)
                lb_data = requests.get(lb_url)
                lb_soup = BeautifulSoup(lb_data.text, 'html.parser')
                lb_list = lb_soup.find_all(attrs={'class' : 'leaderboard-entry'})

                for count, scored_time_str in enumerate(lb_list, 1):
                    stars = 2 if count <= 100 else 1
                    scored_place = count if count <= 100 else count - 100
                    scored_time_str = scored_time_str.text
                    pattern = r'\b\d{2}:\d{2}:\d{2}\b'
                    scored_time =  re.search(pattern, scored_time_str)
                    temp_lb_df = pd.DataFrame({'date': info[0].strip()+".12."+str(year), 
                                            'stars': stars, 
                                            'time': scored_time.group(0),
                                            'scored_place': scored_place}, index=[0])
                    leaderboard_stats = pd.concat([leaderboard_stats,temp_lb_df], ignore_index=True)
                    print(temp_lb_df)


                i -= 1
                time.sleep(3)
        
        # no spamming :) 
        time.sleep(2)
    stats.to_excel("stats.xlsx", index=False)
    leaderboard_stats.to_excel("leaderboard_stats.xlsx", index=False)

if __name__ == "__main__":
    collect_yearly_stats(years=[2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023])
