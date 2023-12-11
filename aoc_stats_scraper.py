import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def collect_yearly_stats(years):
    stats = pd.DataFrame({'date': [], 'both': [], 'one': []})
    for year in years:
        url = "https://adventofcode.com/" + str(year) + "/stats"
        data = requests.get(url)
        soup = BeautifulSoup(data.text, 'html.parser')
        table = soup.find_all(attrs={'class' : 'stats'})
        for entry in table:
            for line in entry:
                if line == '\n':
                    continue
                info = line.find_all(string=True)
                temp_df = pd.DataFrame({'date': info[0].strip()+".12."+str(year), 'both': int(info[1].strip()), 'one': int(info[3].strip())}, index=[0])
                stats = pd.concat([stats,temp_df],ignore_index=True)
        
        # no spamming :) 
        time.sleep(2)
    stats.to_excel("stats.xlsx", index=False)

if __name__ == "__main__":
    collect_yearly_stats(years=[2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023])
 