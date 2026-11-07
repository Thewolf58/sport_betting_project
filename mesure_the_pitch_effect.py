#Naive Modell: In this modell we are only going to test the method of testing a football match
#testing period session = x
#tuning session = x - 1 session
#We want to tune our modell on the tuning session
#And with the tuned modell we test the modell in testing period session
#We will test the modell only in premier leauge and only in one session
#And we only tune this model one session too 
#For the compare we will create for every match new odds in the testing period session and we will compare againts the pinnacle close odds to see how far is our model compare to a professional bookmaker
#testing period session = 2024/2025
#Tuning session = 2023/2024
#Mesure our modell accuraccy = how far from our modell decimals (like 0.65 wich means 65%) is pinnacle decimals (like 0.35) = 0.65-0.35 = 0.3 

import pandas as pd 
import datetime
import numpy as np

tuning_data = pd.read_csv("/Users/lukacsadam/python/sport_betting_project/datas/prem_data_23_24.csv")
testing_period_data = pd.read_csv("/Users/lukacsadam/python/sport_betting_project/datas/prem_data_24_25.csv")

total_prem_match = 380 #From official premier league site

tuning_data = pd.DataFrame(tuning_data).reset_index()
tuning_data["Date"] =  pd.to_datetime(tuning_data["Date"] , dayfirst=True)

if total_prem_match == len(tuning_data):
    print("We have all match data")

total_data_match = len(tuning_data)

pitch_where = tuning_data["FTR"].value_counts()

avrage_percentages_pitch = pd.DataFrame({
    "avrage_%_of_home_win": [(pitch_where["H"]/total_data_match)*100],
    "avrage_%_of_draw": [(pitch_where["D"]/total_data_match)*100],
    "avrage_%_of_away_win": [(pitch_where["A"]/total_data_match)*100]
})

print(avrage_percentages_pitch)

if (round(avrage_percentages_pitch["avrage_%_of_home_win"][0] + avrage_percentages_pitch["avrage_%_of_draw"][0] + avrage_percentages_pitch["avrage_%_of_away_win"][0])) == 100:
    print("Percent is good")

