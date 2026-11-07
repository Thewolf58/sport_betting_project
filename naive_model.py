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

#The following function will watch if we have the same match data as the official premier leauge data
def data_lenght_test(data):
    if total_prem_match == len(data):
        return "We have all match data"
    else: 
        return "we dont have the same number of data that we needed"



total_data_match = len(tuning_data)


pitch_where = tuning_data["FTR"].value_counts()

#1. part is to build the model

naiv_modell = pd.DataFrame({
    "avrage_%_of_home_win": [(pitch_where["H"]/total_data_match)*100],
    "avrage_%_of_draw": [(pitch_where["D"]/total_data_match)*100],
    "avrage_%_of_away_win": [(pitch_where["A"]/total_data_match)*100]
})

#The naiv_modell_odds will be our fair odds for all match in testing period data
naiv_modell_odds = pd.DataFrame({
    "ODDS_of_home_win": [1/(naiv_modell["avrage_%_of_home_win"][0]/100)],
    "ODDS_of_draw": [1/(naiv_modell["avrage_%_of_draw"][0]/100)],
    "ODDS_of_away_win": [1/(naiv_modell["avrage_%_of_away_win"][0]/100)],
})

#2. part of the model is use the model on the testing_period_data

#Rules if the odds is bigger than our odds for home win then we place a bet
#First calculate the fair value of an odds 

naiv_modell_data = testing_period_data[["Date" , "Time" , "HomeTeam" , "AwayTeam" , "FTR", "PSCH", "PSCD" , "PSCA"]].copy()
naiv_modell_data['Home_probability'] = 1/naiv_modell_data["PSCH"]
naiv_modell_data['Draw_probability'] = 1/naiv_modell_data["PSCD"]
naiv_modell_data['Away_probability'] = 1/naiv_modell_data["PSCA"]
naiv_modell_data['sum_probability'] = naiv_modell_data["Home_probability"] + naiv_modell_data["Draw_probability"] + naiv_modell_data["Away_probability"]
naiv_modell_data["Brokerage_edge"] = naiv_modell_data["sum_probability"] - 1
naiv_modell_data["Real_home_probability"] = naiv_modell_data["Home_probability"]/naiv_modell_data["sum_probability"]
naiv_modell_data["Real_draw_probability"] = naiv_modell_data["Draw_probability"]/naiv_modell_data["sum_probability"]
naiv_modell_data["Real_away_probability"] = naiv_modell_data["Away_probability"]/naiv_modell_data["sum_probability"]

Missing_psch = 0
Missing_pscd = 0
Missing_psca = 0

print((naiv_modell_data[naiv_modell_data["PSCH"].isna() == True]))
print((naiv_modell_data[naiv_modell_data["PSCD"].isna() == True]))
print((naiv_modell_data[naiv_modell_data["PSCA"].isna() == True]))
