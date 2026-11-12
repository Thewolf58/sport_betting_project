#Out of sample test
#In this test we are going to test our team_strenght_model because it got the greater result in the brier score test
#The learning period the 2024-2025 season only
#Test: 2025/26, promoted teams excluded, same matches for all models 
#Pass: if the brier score will lower than the Pinnacle's brier score
#Look at once, no retest watever the result

import pandas as pd 
from scipy.stats import poisson

#Import the original raw data
raw_training_data = pd.read_csv("datas/prem_data_24_25.csv")
raw_testing_data = pd.read_csv("datas/prem_data_25_26.csv")

#Select the only needed columns from the datas
training_data = raw_training_data[["Date" , "Time" , "HomeTeam" , "AwayTeam" , "FTHG" , "FTAG" , "FTR" , "PSCH" , "PSCD" , "PSCA"]]
testing_data = raw_testing_data[["Date" , "Time" , "HomeTeam" , "AwayTeam" , "FTHG" , "FTAG" , "FTR" , "PSCH" , "PSCD" , "PSCA"]]

#Calculate the raw pinnacle probabilites from the odds
def raw_probability_from_odds(data):
    data = data.copy()
    data["bookmaker_home_raw_prob"] = 1/data["PSCH"]
    data["bookmaker_draw_raw_prob"] = 1/data["PSCD"]
    data["bookmaker_away_raw_prob"] = 1/data["PSCA"]  
    return data

#Used raw_probability_from_odds function to get our raw probabilities from oods
train_raw_prob = raw_probability_from_odds(training_data)
test_raw_prob = raw_probability_from_odds(testing_data)

#Calculate the real probabilities from the raw probability
def real_probability_from_raw_prob(data):
    data = data.copy()
    data["sum_prob"] = (data["bookmaker_home_raw_prob"] + data["bookmaker_draw_raw_prob"] + data["bookmaker_away_raw_prob"])
    data["Real_home_prob"] = data["bookmaker_home_raw_prob"]/data["sum_prob"]
    data["Real_draw_prob"] = data["bookmaker_draw_raw_prob"]/data["sum_prob"]
    data["Real_away_prob"] = data["bookmaker_away_raw_prob"]/data["sum_prob"]
    return data

#Used real_probability function to gather the real probability from the side / side + bookmaker edge
train_real_prob = real_probability_from_raw_prob(train_raw_prob)
test_real_prob = real_probability_from_raw_prob(test_raw_prob)

#Calculate the home advantage:
avg_away_goal = train_real_prob["FTAG"].mean()
avg_home_goal = train_real_prob["FTHG"].mean()

