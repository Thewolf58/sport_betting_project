#Out of sample test (train: 2024/25 , test: 2025/26 , 272 matches, promoted teams exluded):
#In this test we are going to test our team_strenght_model because it got the greater result in the brier score test
#The learning period the 2024-2025 season only
#Test: 2025/26, promoted teams excluded, same matches for all models 
#Pass: if the brier score will lower than the Pinnacle's brier score
#Look at once, no retest watever the result
#Pass line: our Brier score < Pinnacle's Brier score 
#Brier score: Our model: 0.63184 , The 25-26 pinnacle: 0.59495
#Result: Fail

import pandas as pd 
import numpy as np
from brier_score import brier_score
from functions import (chance , raw_probability_from_odds , real_probability_from_raw_prob , goals_per_team , average_league_goal, attack_defend_score , add_scores_to_match_data , average_home_away_goal ,accuracy_to_bookmaker_prob , add_outcomes , brier_score_in_a_Dateframe)

#Import the original raw data
raw_training_data = pd.read_csv("datas/prem_data_24_25.csv")
raw_testing_data = pd.read_csv("datas/prem_data_25_26.csv")

def main():
    #Select the only needed columns from the datas
    training_data = raw_training_data[["Date" , "Time" , "HomeTeam" , "AwayTeam" , "FTHG" , "FTAG" , "FTR" , "PSCH" , "PSCD" , "PSCA"]]
    testing_data = raw_testing_data[["Date" , "Time" , "HomeTeam" , "AwayTeam" , "FTHG" , "FTAG" , "FTR" , "PSCH" , "PSCD" , "PSCA"]]

    #Used raw_probability_from_odds function to get our raw probabilities from oods
    training_data = raw_probability_from_odds(training_data)
    testing_data = raw_probability_from_odds(testing_data)

    #Use real_probability function to gather the real probability from the side / side + bookmaker edge
    training_data = real_probability_from_raw_prob(training_data)
    testing_data = real_probability_from_raw_prob(testing_data)

    #Drop the raws probability from the real_prob datas
    training_data = training_data.drop(columns=["bookmaker_home_raw_prob" ,"bookmaker_draw_raw_prob" , "bookmaker_away_raw_prob"])
    testing_data = testing_data.drop(columns=["bookmaker_home_raw_prob" ,"bookmaker_draw_raw_prob" , "bookmaker_away_raw_prob"])

    #Calculate the strength of each team
    training_data_strength = goals_per_team(training_data)

    #Call average leauge goal function on training data's strength data 
    training_average_goal = average_league_goal(training_data_strength)

    #Call the attack defend score in training data
    training_teams_scores = attack_defend_score(training_average_goal , training_data_strength)

    #Call the function wich is put the scores of each team and the match data together on the testing data
    testing_data = add_scores_to_match_data(training_teams_scores , testing_data)

    #Calculate the average goals for home and away
    average_home_goal , average_away_goal = average_home_away_goal(training_data)

    #Calculate the expected goals
    testing_data["exp_home_goals"] = average_home_goal * testing_data["Home_attack"] * testing_data["Away_defend"]
    testing_data["exp_away_goals"] = average_away_goal * testing_data["Away_attack"] * testing_data["Home_defend"]

    #Calculate the probablility of each outcome
    testing_data["H"] , testing_data["A"] , testing_data["D"] = chance(testing_data["exp_home_goals"] , testing_data["exp_away_goals"])

    #Calculate the Pinnacle's brier score 
    pinnacle_brier_score = testing_data.copy()
    pinnacle_brier_score = pinnacle_brier_score.drop(columns=["H" , "A" , "D"])
    pinnacle_brier_score = pinnacle_brier_score.rename(columns={"Real_home_prob": "H" , "Real_draw_prob": "D" , "Real_away_prob": "A"})
    pinnacle_brier_score = add_outcomes(pinnacle_brier_score)
    
    #Test accuracy
    accuracy = accuracy_to_bookmaker_prob(testing_data)
    avg_brier_score = brier_score(testing_data)
    pinnacle_brier_score = brier_score_in_a_Dateframe(pinnacle_brier_score)
    print(f"{accuracy} The model accuracy")
    print(f"{avg_brier_score} The model brier score ")
    print(f"{pinnacle_brier_score} Pinnacle brier score")
    return [avg_brier_score , pinnacle_brier_score , accuracy]
    

if __name__ == "__main__":
    main()

