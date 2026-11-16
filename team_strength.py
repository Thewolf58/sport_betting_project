#This file want to mesure how strong was each team from the traning data wich is the premier leauge 2023-2024 season
#The  basic of the mesurement is the concered and the scored goal
#With that for each team we can create a separete avrage concered goals and avrage scored goals collum 
#We just give rating to the teams wich is in the traning data so the promoted team dont get rating from the training data 
#From the testing data we will cut down the promoted teams because for the teams we dont have good data 
# ---- PASS LINE (written BEFORE any 24/25 test) ----
# Metric: the same closeness score as the naive model, 1 - |our prob - Pinnacle prob|
# Matches: 24/25 without promoted-team matches (~270), and both models are scored on these
# Pass: team-strength score > naive score on the same matches
# Fail: team-strength score <= naive score
# Measured on: overall average
# Note: a win smaller than 0.01 = weak result (could be luck)
#Result: team strenght modell: 0.935 , naive modell: 0.897 PASS: True

import pandas as pd 
from scipy.stats import poisson
from naive_model import naive_model_table
from pathlib import Path

#File paths 
HERE = Path(__file__).parent
DATA_DIR = HERE / "datas"

#Import data
traning_data = pd.read_csv(DATA_DIR/"prem_data_23_24.csv")
testing_data = pd.read_csv(DATA_DIR/"prem_data_24_25.csv")
naive_table = naive_model_table(traning_data)

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
    all_goal_team["Avg_scored_match"] = all_goal_team["Goals"]/38
    all_goal_team["Avg_concered_match"] = all_goal_team["Conceded_goals"]/38

    return all_goal_team

#Create a table that contain the scored and conceded goals for all team
training_data_team_strength = goals_per_team(traning_data)

#Create a function that is calculate the avrage league goals per season 
def average_league_goal(data):
    all_league_goal = data["Goals"].sum()
    average_goal_per_game = all_league_goal/(len(data)*38)
    return average_goal_per_game

train_average_goal_per_match = average_league_goal(training_data_team_strength)

#Create a function that write attack score and defend score collums to the original data 

#I'm curently at here with cleaning

training_data_with_power_rate = power_rating(traning_data , training_data_team_strength)
 

team_strenght_testing_data = testing_data[["Date" , "HomeTeam" , "AwayTeam" , "FTHG" , "FTAG" , "PSCH" , "PSCD" , "PSCA"]]

match_with_goals_data = pd.merge(team_strenght_testing_data , overall_table , left_on="HomeTeam" , right_on="Team")
match_with_goals_data = match_with_goals_data[["Date" , "HomeTeam", "AwayTeam" , "FTHG" , "FTAG" , "Team" , "avg_scored_goal/legauge_avg" , "avg_concered_goal/legauge_avg" , "PSCH" , "PSCD" , "PSCA"]]
match_with_goals_data = match_with_goals_data.rename(columns={"avg_scored_goal/legauge_avg": "Home_attack" , "avg_concered_goal/legauge_avg": "Home_defend"})
match_with_goals_data = pd.merge(match_with_goals_data , overall_table , left_on="AwayTeam" , right_on="Team")
match_with_goals_data = match_with_goals_data.rename(columns={"avg_scored_goal/legauge_avg": "Away_attack" , "avg_concered_goal/legauge_avg": "Away_defend"})
match_with_goals_data = match_with_goals_data[["Date" , "HomeTeam" , "AwayTeam" , "FTHG" , "FTAG" , "Home_attack" , "Home_defend" , "Away_attack" , "Away_defend" , "PSCH" , "PSCD" , "PSCA"]]
final_data = match_with_goals_data

avrage_home_goal = team_strenght_training_data["FTHG"].mean()
avrage_away_goal = team_strenght_training_data["FTAG"].mean()

home_advangages = avrage_home_goal/avrage_away_goal #We use this to multiply exp_home goals

final_data["exp_home_goals"] = avrage_home_goal * final_data["Home_attack"] * final_data["Away_defend"]
final_data["exp_away_goals"] = avrage_away_goal * final_data["Away_attack"] * final_data["Home_defend"]

#Poission modell calculation 

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

final_data["H"] = chance(final_data["exp_home_goals"] , final_data["exp_away_goals"])[0]
final_data["D"] = chance(final_data["exp_home_goals"] , final_data["exp_away_goals"])[2]
final_data["A"] = chance(final_data["exp_home_goals"] , final_data["exp_away_goals"])[1]

final_data["SUM_probability"] = (1/final_data["PSCH"] + 1/final_data["PSCD"] + 1/final_data["PSCA"])
final_data["Pinnacle_margin"] = final_data["SUM_probability"]-1
final_data["Home_prob_odds"] = 1/final_data["PSCH"]
final_data["Draw_prob_odds"] = 1/final_data["PSCD"]
final_data["Away_prob_odds"] = 1/final_data["PSCA"]
final_data["Fair_home"] = final_data["Home_prob_odds"]/final_data["SUM_probability"]
final_data["Fair_draw"] = final_data["Draw_prob_odds"]/final_data["SUM_probability"]
final_data["Fair_away"] = final_data["Away_prob_odds"]/final_data["SUM_probability"]

accuracy_table = final_data[["Date" , "HomeTeam" , "AwayTeam" , "FTHG" , "FTAG" , "PSCH" , "PSCA" , "H" , "D" , "A" , "Fair_home" , "Fair_draw" , "Fair_away" , "Home_prob_odds" , "Draw_prob_odds" , "Away_prob_odds"]]
accuracy_table["closness_H"] = 1-(abs(accuracy_table["H"] - accuracy_table["Fair_home"]))
accuracy_table["closness_D"] = 1-(abs(accuracy_table["D"] - accuracy_table["Fair_draw"]))
accuracy_table["closness_A"] = 1-(abs(accuracy_table["A"] - accuracy_table["Fair_away"]))

avrage_accuracy = (accuracy_table["closness_H"].mean() + accuracy_table["closness_D"].mean() + accuracy_table["closness_A"].mean())/3

probability_for_matches_with_our_model = accuracy_table[["Date" , "HomeTeam" , "AwayTeam" , "FTHG" , "FTAG" , "H" , "D" , "A"]].copy()
probability_for_matches_with_our_model["H"] = probability_for_matches_with_our_model["H"]*100 
probability_for_matches_with_our_model["D"] = probability_for_matches_with_our_model["D"]*100 
probability_for_matches_with_our_model["A"] = probability_for_matches_with_our_model["A"]*100 
probability_for_matches_with_our_model = probability_for_matches_with_our_model.rename(columns={"H": "H_%" , "D": "D_%" , "A": "A_%"})

#Run the naive modell
avrage_home_goal_odds = avrage_home_goal
avrage_away_goal_odds = avrage_away_goal

naive_modell_run_on_the_same_sample = final_data[["PSCH" , "PSCD" , "PSCA" , "Fair_home" , "Fair_draw" , "Fair_away" , "FTHG" , "FTAG"]].copy()
naive_modell_run_on_the_same_sample["naive_model_home_win_%"] = naive_table["average_%_of_home_win"].iloc[0]/100
naive_modell_run_on_the_same_sample["naive_model_draw_%"] = naive_table["average_%_of_draw"].iloc[0]/100
naive_modell_run_on_the_same_sample["naive_model_away_win_%"] = naive_table["average_%_of_away_win"].iloc[0]/100
naive_modell_run_on_the_same_sample["Diff_from_Pinnacle"] = (naive_modell_run_on_the_same_sample["naive_model_home_win_%"] - naive_modell_run_on_the_same_sample["Fair_home"]).abs()
naive_modell_run_on_the_same_sample["Diff_from_Pinnacle"] = naive_modell_run_on_the_same_sample["Diff_from_Pinnacle"] + (naive_modell_run_on_the_same_sample["naive_model_away_win_%"] - naive_modell_run_on_the_same_sample["Fair_away"]).abs()
naive_modell_run_on_the_same_sample["Diff_from_Pinnacle"]= naive_modell_run_on_the_same_sample["Diff_from_Pinnacle"] + (naive_modell_run_on_the_same_sample["naive_model_draw_%"] - naive_modell_run_on_the_same_sample["Fair_draw"]).abs()
naive_modell_run_on_the_same_sample["Diff_from_Pinnacle"] = naive_modell_run_on_the_same_sample["Diff_from_Pinnacle"]/3

avrage_diff_from_pinnacle = (naive_modell_run_on_the_same_sample["Diff_from_Pinnacle"]).mean()
avrage_accuracy_naive_model = 1 - avrage_diff_from_pinnacle
naive_model_accuracy = avrage_accuracy_naive_model

if avrage_accuracy > naive_model_accuracy:
    print(avrage_accuracy)
    print("Team_strenght_model_better")
elif avrage_accuracy < naive_model_accuracy:
    print(avrage_accuracy)
    print("naive_modell_was_better")

print(naive_model_accuracy)
print(strength_calculation(testing_data))