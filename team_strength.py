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
from scipy.stats import poisson
from naive_model import naive_model_table
from pathlib import Path

#File paths 
HERE = Path(__file__).parent
DATA_DIR = HERE / "datas"

#Functions block 
#Function for scored , conceded goal per team
def goals_per_team(data):
    home_score_per_team = data.groupby(["HomeTeam"])["FTHG"].sum().reset_index()
    away_score_per_team = data.groupby(["AwayTeam"])["FTAG"].sum().reset_index()
    scored_goal_team = pd.merge(home_score_per_team , away_score_per_team , left_on="HomeTeam" , right_on="AwayTeam")
    scored_goal_team["Goals"] = scored_goal_team["FTHG"] + scored_goal_team["FTAG"]
    scored_goal_team = scored_goal_team.drop(columns=["FTHG" , "FTAG", "AwayTeam"])
    scored_goal_team = scored_goal_team.rename(columns={"HomeTeam": "Team"})

    home_conceded_per_team = data.groupby(["HomeTeam"])["FTAG"].sum().reset_index()
    away_conceded_per_team = data.groupby(["AwayTeam"])["FTHG"].sum().reset_index()
    all_conceded_team = pd.merge(home_conceded_per_team , away_conceded_per_team , left_on="HomeTeam" , right_on="AwayTeam")
    all_conceded_team["Conceded_goals"] = all_conceded_team["FTAG"] + all_conceded_team["FTHG"]
    all_conceded_team = all_conceded_team.drop(columns=["FTAG" , "AwayTeam" , "FTHG"])
    all_conceded_team = all_conceded_team.rename(columns={"HomeTeam": "Team"})

    all_goal_team = pd.merge(scored_goal_team, all_conceded_team , on="Team")
    #Assumes a full Premier League season: every team plays 38 matches
    all_goal_team["Avg_scored_match"] = all_goal_team["Goals"]/38
    all_goal_team["Avg_conceded_match"] = all_goal_team["Conceded_goals"]/38
    return all_goal_team

#Create a function that calculates the average league goals per season 
def average_league_goal(data):
    average_goal_per_team = data["Avg_scored_match"].mean()
    return average_goal_per_team

#Create a function that writes attack score and defend score columns to the original data 
def attack_defend_score(avg_league_goal , team_strength):
    attack_defend_table = team_strength.copy()
    attack_defend_table["Attack"] = attack_defend_table["Avg_scored_match"]/avg_league_goal
    attack_defend_table["Defend"] = attack_defend_table["Avg_conceded_match"]/avg_league_goal
    attack_defend_table = attack_defend_table.drop(columns={"Goals" , "Conceded_goals" , "Avg_conceded_match" , "Avg_scored_match"})
    return attack_defend_table

#Add the team's attack and defense score into the match table 
def add_scores_to_match_data(score , data):
    final_data = pd.merge(data , score , left_on="HomeTeam" , right_on="Team")
    final_data = final_data.rename(columns={"Attack" : "Home_attack" , "Defend": "Home_defend"})
    final_data = pd.merge(final_data , score , left_on="AwayTeam" , right_on="Team")
    final_data = final_data.rename(columns={"Attack": "Away_attack" , "Defend": "Away_defend"})
    final_data = final_data.drop(columns=["Team_x" , "Team_y"])
    return final_data

#Create a function that calculates the average home and away goal 
def average_home_away_goal(data):
    home = data["FTHG"].mean()
    away = data["FTAG"].mean()
    avr_pitch_goal = [home , away]
    return avr_pitch_goal 

#Poisson model function 
def chance(home_exp , away_exp):
    home_c = 0
    away_c = 0
    draw_c = 0
    for h in range(11):
        for a in range(11):
            if h > a:
                home_c += (poisson.pmf(h , home_exp) * poisson.pmf(a , away_exp))
            if a > h: 
                away_c += (poisson.pmf(h , home_exp) * poisson.pmf(a , away_exp))
            if a == h: 
                draw_c += (poisson.pmf(h , home_exp) * poisson.pmf(a , away_exp))
    return([home_c , away_c , draw_c])


#Create a function which gives the raw probabilities from odds 
def raw_probability_from_odds(data):
    data = data.copy()
    data["bookmaker_home_raw_prob"] = 1/data["PSCH"]
    data["bookmaker_draw_raw_prob"] = 1/data["PSCD"]
    data["bookmaker_away_raw_prob"] = 1/data["PSCA"]  
    return data

#Create a function that calculates the real probability from raw probability 
def real_probability_from_raw_prob(data):
    data = data.copy()
    data["sum_prob"] = (data["bookmaker_home_raw_prob"] + data["bookmaker_draw_raw_prob"] + data["bookmaker_away_raw_prob"])
    data["Real_home_prob"] = data["bookmaker_home_raw_prob"]/data["sum_prob"]
    data["Real_draw_prob"] = data["bookmaker_draw_raw_prob"]/data["sum_prob"]
    data["Real_away_prob"] = data["bookmaker_away_raw_prob"]/data["sum_prob"]
    return data

#Calculate the model accuracy compared to the Pinnacle's probability 
def accuracy_to_bookmaker_prob(data):
    accuracy_table = data[["Date" , "HomeTeam" , "AwayTeam" , "FTHG" , "FTAG" , "FTR" , "Real_home_prob" , 'Real_draw_prob' , "Real_away_prob" , "H" , "A" , "D"]].copy()
    accuracy_table["avg_diff_from_pinnacle"] = (abs(accuracy_table["H"] - accuracy_table["Real_home_prob"]) + abs(accuracy_table["D"] - accuracy_table["Real_draw_prob"]) + abs(accuracy_table["A"] - accuracy_table["Real_away_prob"]))/3
    test_accuracy = 1- (accuracy_table["avg_diff_from_pinnacle"].mean())
    return test_accuracy
#Function block end
##################

#The test itself 
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

    print(test_accuracy)
    print(naive_model_accuracy)

    #Print which model was better 
    if test_accuracy > naive_model_accuracy:
        print("Team_strength_model_better")
    elif test_accuracy < naive_model_accuracy:
        print("naive_model_was_better")
    else: 
        print("Equal")

    return(test_accuracy , naive_model_accuracy)

if __name__ == "__main__":
    main()




