from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import os
import pandas as pd
import numpy as np
from IPython.display import clear_output
from zipfile import ZipFile
from ScraperFC.shared_functions import check_season

class FiveThirtyEight:
    
    ############################################################################
    def __init__(self):
        options = Options()
        options.headless = True
        prefs = {"download.default_directory" : os.getcwd()}
        options.add_experimental_option("prefs",prefs)
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        clear_output()
        
    ############################################################################    
    def close(self):
        """ Closes and quits the Selenium WebDriver instance.
        """
        self.driver.close()
        self.driver.quit()
        
    ############################################################################    
    def up_season(self, string):
        """ Increments a string of the season year
        
        Args
        ----
        string : str
            String of a calendar year (e.g. "2022")
        Returns
        -------
        : str
            Incremented calendar year
        """
        return str(int(string) + 1)
        
    ############################################################################  
    def scrape_matches(self, year, league, save=False):
        """ Scrapes matches for the given league season

        Args
        ----
        year : int
            Calendar year that the season ends in (e.g. 2023 for the 2022/23 season)
        league : str
            League. Look in shared_functions.py for the available leagues for each\
            module.
        save : bool
            OPTIONAL, default is False. If True, output will be saved to a CSV file.
        Returns
        -------
        : Pandas DataFrame
            If save=False, FiveThirtyEight stats for all matches of the given\
            league season
        filename : str
            If save=True, filename of the CSV that the stats were saved to 
        """
        if not check_season(year,'EPL','FiveThirtyEight'):
            return -1
        
        url = 'https://data.fivethirtyeight.com/#soccer-spi'
        self.driver.get(url)
        
        # find and click download button
        for element in self.driver.find_elements(By.CLASS_NAME, "download-link"):
            if element.get_attribute("dataset-name") == "soccer-spi":
                element.click()
                
        # wait for download to complete
        while not os.path.exists('soccer-spi.zip'):
            pass
        
        # get data table
        with ZipFile('soccer-spi.zip') as zf:
            with zf.open('soccer-spi/spi_matches.csv') as f:
                df = pd.read_csv(f)
        os.remove('soccer-spi.zip') # delete downloaded folder
        
        # pick the chosen league
        if league == "EPL":
            df = df[df['league'] == 'Barclays Premier League']
        elif league == "La Liga":
            df = df[df['league'] == 'Spanish Primera Division']
        elif league == "Bundesliga":
            df = df[df['league'] == 'German Bundesliga']
        elif league == "Serie A":
            df = df[df['league'] == 'Italy Serie A']
        elif league == "Ligue 1":
            df = df[df['league'] == 'French Ligue 1']
        
        # add one to season column
        df['season'] = df['season'].apply(self.up_season)
        
        # only keep the season requested
        df = df[df['season']==str(year)]
        
        # only keep some cols
        keep = ['date','team1','team2','score1','score2','xg1','xg2',
                'nsxg1','nsxg2','adj_score1','adj_score2']
        df = df[keep]
        
        # rename cols
        cols = ['Date','Home Team','Away Team','Home Goals','Away Goals',
                'FTE Home xG','FTE Away xG','FTE Home nsxG','FTE Away nsxG',
                'Home Adj Score','Away Adj Score']
        df.columns = cols
        
        df = df.reset_index(drop=True)
        
        # save to CSV if requested by user
        if save:
            filename = f'{year}_{league}_FiveThirtyEight_matches.csv'
            df.to_csv(path_or_buf=filename, index=False)
            print('Matches dataframe saved to ' + filename)
            return filename
        else:
            return df
        