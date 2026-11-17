#Team strength model test (Premier League)
#This model rates each team's attack and defense strength and, from that, predicts the probability of each match outcome 
#Model training period: 2023/2024 Premier League season
#Model testing period: 2024/2025 Premier League season , promoted teams removed because we had no data on them 
#Method: 
    #1. Rate each team's defense and attack from goals data
    #2. Calculate the expected goals for each match 
    #3. Use the Poisson distribution to calculate the probabilities for outcomes 

# ---- PASS LINE (written BEFORE any 24/25 test) ----
# Metric: the same closeness score as the naive model, 1 - |our prob - Pinnacle prob|
# Matches: 24/25 without promoted-team matches (~270), and both models are scored on these
# Pass: team-strength score > naive score on the same matches
# Fail: team-strength score <= naive score
# Measured on: overall average
# Note: a win smaller than 0.01 = weak result (could be luck)
#Result: team strength model: 0.9351 , naive model: 0.8967 , PASS: True

import pandas as pd 
from pathlib import Path
from functions import (naive_model_table , goals_per_team , average_league_goal , attack_defend_score , add_scores_to_match_data , average_home_away_goal , chance , raw_probability_from_odds , real_probability_from_raw_prob, accuracy_to_bookmaker_prob)

#File paths 
HERE = Path(__file__).parent
DATA_DIR = HERE / "datas"

def main():
    #Import data
    training_data = pd.read_csv(DATA_DIR/"prem_data_23_24.csv")
    testing_data = pd.read_csv(DATA_DIR/"prem_data_24_25.csv")
    naive_table = naive_model_table(training_data)
    
    #Create a table that contains the scored and conceded goals for all teams 
    training_data_team_strength = goals_per_team(training_data)

    #Call the average_league_goal function on training data  and saved it
    train_average_goal_per_match = average_league_goal(training_data_team_strength)

    #Call the attack_defend_score on training data 
    training_scores = attack_defend_score(train_average_goal_per_match , training_data_team_strength)

    #Create the data that contains the attack and defend scores too
    final_test_data = add_scores_to_match_data(training_scores , testing_data)

    #Calculate the average home and away goal
    avr_home_goal , avr_away_goal = average_home_away_goal(training_data)

    #Calculate the expected goals
    final_test_data["exp_home_goals"] = avr_home_goal * final_test_data["Home_attack"] * final_test_data["Away_defend"]
    final_test_data["exp_away_goals"] = avr_away_goal * final_test_data["Away_attack"] * final_test_data["Home_defend"]

    #Calculate the probabilities for each match outcome 
    final_test_data["H"] , final_test_data["A"] , final_test_data["D"] = chance(final_test_data["exp_home_goals"] , final_test_data["exp_away_goals"])

    #Calculate the raw probabilities from Pinnacle's odds 
    final_test_data = raw_probability_from_odds(final_test_data)

    #Calculate the real probabilities from raw probabilities
    final_test_data = real_probability_from_raw_prob(final_test_data)

    #Calculate the test accuracy compared into Pinnacle's probabilities 
    test_accuracy = accuracy_to_bookmaker_prob(final_test_data)

    #Run the naive model to compare the accuracy against the team_strength model
    naive_model_run_on_the_same_sample = final_test_data[["Date", "HomeTeam", "AwayTeam" , "FTR" , "Real_home_prob" , "Real_draw_prob" , "Real_away_prob" , "FTHG" , "FTAG"]].copy()
    naive_model_run_on_the_same_sample["H"] = naive_table["average_%_of_home_win"].iloc[0]/100
    naive_model_run_on_the_same_sample["D"] = naive_table["average_%_of_draw"].iloc[0]/100
    naive_model_run_on_the_same_sample["A"] = naive_table["average_%_of_away_win"].iloc[0]/100

    #Calculate the naive_model_accuracy
    naive_model_accuracy = accuracy_to_bookmaker_prob(naive_model_run_on_the_same_sample)

    return([test_accuracy , naive_model_accuracy])

if __name__ == "__main__":
    main()




