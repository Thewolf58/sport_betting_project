#Out of sample test
#In this test we are going to test our team_strenght_model because it got the greater result in the brier score test
#The learning period the 2024-2025 season only
#Test: 2025/26, promoted teams excluded, same matches for all models 
#Pass: if the brier score will lower than the Pinnacle's brier score
#Look at once, no retest watever the result

import pandas as pd 
from scipy.stats import poisson
import numpy as np
from team_strength import chance #This function output will be (home_chance , away_chance , draw_chance)

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

#Drop the raws probability from the real_prob datas
train_real_prob = train_real_prob.drop(columns=["bookmaker_home_raw_prob" ,"bookmaker_draw_raw_prob" , "bookmaker_away_raw_prob"])
test_real_prob = test_real_prob.drop(columns=["bookmaker_home_raw_prob" ,"bookmaker_draw_raw_prob" , "bookmaker_away_raw_prob"])

#Calculate the home advantage:
avg_away_goal = train_real_prob["FTAG"].mean()
avg_home_goal = train_real_prob["FTHG"].mean()

#This function calculate from the training season avrage scored and concered goal for each team how strong their defend and how strong their attack 
def training_strengh_data(data_real):
    data = data_real.copy()
    home_team_score = data.groupby("HomeTeam")["FTHG"].sum()
    away_team_score = data.groupby("AwayTeam")["FTAG"].sum()
    home_team_concered = data.groupby("HomeTeam")["FTAG"].sum()
    away_team_concered = data.groupby("AwayTeam")["FTHG"].sum()
    avg_scored_goal_match = (home_team_score + away_team_score)/38
    avg_concered_goal_match = (home_team_concered + away_team_concered)/38
    goal_per_match = len(data)/(data["FTHG"].sum() + data["FTAG"].sum())
    reset_avg_scored_goal_match = avg_scored_goal_match.reset_index()
    reset_avg_concered_goal_match = avg_concered_goal_match.reset_index()
    reset_avg_concered_goal_match = reset_avg_concered_goal_match.rename(columns={"0" : "1"})
    team_avg_table = pd.merge(reset_avg_concered_goal_match , reset_avg_scored_goal_match , on="HomeTeam")
    team_avg_table = team_avg_table.rename(columns={"0_x": "avg_concered_goal" , "0_y": "avg_scored_goal"})
    team_avg_table["attack_score"] = team_avg_table["avg_scored_goal"]/team_avg_table["avg_scored_goal"].mean()
    team_avg_table["deffend_score"] = team_avg_table["avg_concered_goal"]/team_avg_table["avg_concered_goal"].mean()
    team_avg_table = team_avg_table.set_index("HomeTeam")
    team_avg_table = team_avg_table.rename(columns={"HomeTeam" : "Team"})
    team_avg_table = team_avg_table.drop(columns=["avg_concered_goal" , "avg_scored_goal"])
    return team_avg_table

#run the training_strenght_data function to get a test and a training data too
rating_strenght = training_strengh_data(train_real_prob)

#Create a function that is add for the match datas the strongth 
def add_match_data_w_strenght(match , rating):
    merged_Home_data = pd.merge(match , rating , left_on="HomeTeam" , right_index=True)
    merged_Home_data = merged_Home_data.rename(columns={"attack_score": "home_attack_score" , "deffend_score": "home_defend_score"})
    merged_all_data = pd.merge(merged_Home_data , rating , left_on="AwayTeam" , right_index=True)
    merged_all_data = merged_all_data.rename(columns={"attack_score": "away_attack_score" , "deffend_score": "away_defend_score"})
    return merged_all_data

#Create the merged tables with our merge function 
training_data_strenght_calc = add_match_data_w_strenght(train_real_prob , rating_strenght)
test_data_strenght_calc = add_match_data_w_strenght(test_real_prob , rating_strenght)


#Calculate the expected goals for both to the training and the test data too
training_data_strenght_calc["home_expected_goal"] = avg_home_goal * training_data_strenght_calc["home_attack_score"] * training_data_strenght_calc["away_defend_score"]
training_data_strenght_calc["away_expected_goal"] = avg_away_goal * training_data_strenght_calc["away_attack_score"] * training_data_strenght_calc["home_defend_score"]
test_data_strenght_calc["home_expected_goal"] = avg_home_goal * test_data_strenght_calc["home_attack_score"] * test_data_strenght_calc["away_defend_score"]
test_data_strenght_calc["away_expected_goal"] = avg_away_goal * test_data_strenght_calc["away_attack_score"] * test_data_strenght_calc["home_defend_score"]

#Create a function that calculate our probabilities
def add_probability_to_strenght(data): 
    data["H"] = chance(data["home_expected_goal"] , data["away_expected_goal"])[0]
    data["A"] = chance(data["home_expected_goal"] , data["away_expected_goal"])[1]
    data["D"] = chance(data["home_expected_goal"] , data["away_expected_goal"])[2]
    return data

#Create datas that include our probabilities
probability_with_strenght_training = add_probability_to_strenght(training_data_strenght_calc)
probability_with_strenght_test = add_probability_to_strenght(test_data_strenght_calc)

#Create function that is create a new table that include only just needed data nad avg_diff_from_pinnacle 
def accuracy_to_bookmaker_prob(data):
    accuracy_table = data[["Date" , "HomeTeam" , "AwayTeam" , "FTHG" , "FTAG" , "FTR" , "Real_home_prob" , 'Real_draw_prob' , "Real_away_prob" , "H" , "A" , "D"]].copy()
    accuracy_table["avg_diff_from_pinnacle"] = (abs(accuracy_table["H"] - accuracy_table["Real_home_prob"]) + abs(accuracy_table["D"] - accuracy_table["Real_draw_prob"]) + abs(accuracy_table["A"] - accuracy_table["Real_away_prob"]))/3
    return accuracy_table

diff_from_pinnacle_training = accuracy_to_bookmaker_prob(probability_with_strenght_training)
avg_diff_from_pinnacle_training = diff_from_pinnacle_training["avg_diff_from_pinnacle"].mean()
probability_sameless_training = 1 - avg_diff_from_pinnacle_training

diff_from_pinnacle_test = accuracy_to_bookmaker_prob(probability_with_strenght_test)
avg_diff_from_pinnacle_test = diff_from_pinnacle_test["avg_diff_from_pinnacle"].mean()
probability_sameless_test = 1 - avg_diff_from_pinnacle_test

print(test_data_strenght_calc["Date"].head())
print(len(test_data_strenght_calc))

