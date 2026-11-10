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
#Result: 0.935 , PASS

import pandas as pd 
from scipy.stats import poisson

traning_data = pd.read_csv("/Users/lukacsadam/python/sport_betting_project/datas/prem_data_23_24.csv" ,).reset_index()
testing_data = pd.read_csv("/Users/lukacsadam/python/sport_betting_project/datas/prem_data_24_25.csv" ,).reset_index()

team_strenght_training_data = traning_data[["Date" , "HomeTeam" , "AwayTeam" , "FTHG" , "FTAG"]]

Home_team_scored_goals = team_strenght_training_data.groupby(["HomeTeam"])["FTHG"].sum().reset_index()
Away_team_scored_goals = team_strenght_training_data.groupby(["AwayTeam"])["FTAG"].sum().reset_index()
Home_team_concered_goals = team_strenght_training_data.groupby(["HomeTeam"])["FTAG"].sum().reset_index()
Away_team_concered_goals = team_strenght_training_data.groupby(["AwayTeam"])["FTHG"].sum().reset_index()
Home_team_scored_goals = Home_team_scored_goals.rename(columns={"HomeTeam" : "Team"})
Away_team_scored_goals = Away_team_scored_goals.rename(columns={"AwayTeam": "Team"})
Home_team_concered_goals = Home_team_concered_goals.rename(columns={"HomeTeam": "Team"})
Away_team_concered_goals = Away_team_concered_goals.rename(columns={"AwayTeam": "Team"})

overall_table = pd.merge(Home_team_scored_goals , Away_team_scored_goals , on="Team" , how="left")
overall_table = pd.merge(overall_table , Home_team_concered_goals , on="Team" , how="left")
overall_table = pd.merge(overall_table , Away_team_concered_goals , on="Team" , how="left")
overall_table = overall_table.rename(columns={"FTHG_x": "scored_goal_home" , "FTAG_x": "scored_goal_away" , "FTAG_y": "concered_goal_home" , "FTHG_y": "concered_goal_away"})
overall_table["scored_goals"] = overall_table["scored_goal_home"] + overall_table["scored_goal_away"]
overall_table["concered_goals"] = overall_table["concered_goal_home"] + overall_table["concered_goal_away"]
overall_table["avg_scored_goal_per_match"] = overall_table["scored_goals"]/38
overall_table["avg_concered_goal_per_match"] = overall_table["concered_goals"]/38

all_league_goal = overall_table["scored_goals"].sum()
avrage_goal_per_game = all_league_goal/(len(overall_table)*38)

overall_table["avg_scored_goal/legauge_avg"] = overall_table["avg_scored_goal_per_match"]/avrage_goal_per_game
overall_table["avg_concered_goal/legauge_avg"] = overall_table["avg_concered_goal_per_match"]/avrage_goal_per_game

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
naive_model_accuracy = 0.881

if avrage_accuracy > 0.881:
    print(avrage_accuracy)
    print("Team_strenght_model_better")
elif avrage_accuracy < 0.881:
    print(avrage_accuracy)
    print("naive_modell_was_better")

