#This file want to mesure how strong was each team from the traning data wich is the premier leauge 2023-2024 season
#The  basic of the mesurement is the concered and the scored goal
#With that for each team we can create a separete avrage concered goals and avrage scored goals collum 
#We just give rating to the teams wich is in the traning data so the promoted team dont get rating from the training data 

import pandas as pd 
import numpy as np

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

all_league_goal = overall_table["scored_goals"].sum()
avrage_goal_per_game = all_league_goal/(len(overall_table)*38)

print(avrage_goal_per_game)