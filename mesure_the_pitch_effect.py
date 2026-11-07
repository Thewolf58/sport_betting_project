import pandas as pd 
import datetime
import numpy as np

total_prem_match = 380 #From official premier league site

season_24_25 = pd.read_csv("Premier_league_data_2024-2025.csv")
season_24_25 = pd.DataFrame(season_24_25).reset_index()
season_24_25["Date"] =  pd.to_datetime(season_24_25["Date"])

if total_prem_match == len(season_24_25):
    print("We have all match data")

total_data_match = len(season_24_25)

pitch_where = season_24_25["FTR"].value_counts()

avrage_percentages_pitch = pd.DataFrame({
    "avrage_%_of_home_win": [(pitch_where["H"]/total_data_match)*100],
    "avrage_%_of_draw": [(pitch_where["D"]/total_data_match)*100],
    "avrage_%_of_away_win": [(pitch_where["A"]/total_data_match)*100]
})

print(avrage_percentages_pitch)

if (round(avrage_percentages_pitch["avrage_%_of_home_win"][0] + avrage_percentages_pitch["avrage_%_of_draw"][0] + avrage_percentages_pitch["avrage_%_of_away_win"][0])) == 100:
    print("Percent is good")

