#Functions
#This file contains all functions that I used in my tests 
#Functions: 
    #1. naive_model_table(data) – share (%) of home wins, draws and away wins in the training data
    #2. goals_per_team(data) - goals scored and conceded by each team
    #3. average_league_goal(data) - average goals per team per match in the training period 
    #4. attack_defend_score(avg_league_goal, team_strength) - returns a new table with each team's attack and defend score 
    #5. add_scores_to_match_data(score , data) - adds the team's attack and defense score into the match table 
    #6. average_home_away_goal(data) - calculates the average home and away goals
    #7. chance(home_exp , away_exp) - home / away / draw probabilities from expected goals
    #8. raw_probability_from_odds(data) - gives the raw probabilities from odds 
    #9. real_probability_from_raw_prob(data) - fair probability (margin removed)
    #10. accuracy_to_bookmaker_prob(data) - calculates the model accuracy compared to Pinnacle's probability 
    #11. add_outcomes(df): add a value for each outcome in each match (the value can be 0 or 1)
    #12. brier_score_in_a_Dateframe(dataframe): calculates the average of the matches brier scores 

import pandas as pd 
from scipy.stats import poisson

#Naive model functions 
#1: share (%) of home wins, draws and away wins in the training data
def naive_model_table(data):
    total_match = len(data)
    pitch_where = data["FTR"].value_counts()
    naive_model = pd.DataFrame({
        "average_%_of_home_win": [(pitch_where["H"]/total_match)*100],
        "average_%_of_draw": [(pitch_where["D"]/total_match)*100],
        "average_%_of_away_win": [(pitch_where["A"]/total_match)*100]
    })
    return naive_model

#Team strength functions 
#2. goals_per_team(data) - goals scored and conceded by each team
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

#3. average_league_goal(data) - average goals per team per match in the training period 
def average_league_goal(data):
    average_goal_per_team = data["Avg_scored_match"].mean()
    return average_goal_per_team

#4. attack_defend_score(avg_league_goal, team_strength) - returns a new table with each team's attack and defend score 
def attack_defend_score(avg_league_goal , team_strength):
    attack_defend_table = team_strength.copy()
    attack_defend_table["Attack"] = attack_defend_table["Avg_scored_match"]/avg_league_goal
    attack_defend_table["Defend"] = attack_defend_table["Avg_conceded_match"]/avg_league_goal
    attack_defend_table = attack_defend_table.drop(columns={"Goals" , "Conceded_goals" , "Avg_conceded_match" , "Avg_scored_match"})
    return attack_defend_table

#5. add_scores_to_match_data(score , data) - adds the team's attack and defense score into the match table 
def add_scores_to_match_data(score , data):
    final_data = pd.merge(data , score , left_on="HomeTeam" , right_on="Team")
    final_data = final_data.rename(columns={"Attack" : "Home_attack" , "Defend": "Home_defend"})
    final_data = pd.merge(final_data , score , left_on="AwayTeam" , right_on="Team")
    final_data = final_data.rename(columns={"Attack": "Away_attack" , "Defend": "Away_defend"})
    final_data = final_data.drop(columns=["Team_x" , "Team_y"])
    return final_data

#6. average_home_away_goal(data) - calculates the average home and away goals
def average_home_away_goal(data):
    home = data["FTHG"].mean()
    away = data["FTAG"].mean()
    avr_pitch_goal = [home , away]
    return avr_pitch_goal 

#7. chance(home_exp , away_exp) - home / away / draw probabilities from expected goals
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


#8. raw_probability_from_odds(data) - gives the raw probabilities from odds 
def raw_probability_from_odds(data):
    data = data.copy()
    data["bookmaker_home_raw_prob"] = 1/data["PSCH"]
    data["bookmaker_draw_raw_prob"] = 1/data["PSCD"]
    data["bookmaker_away_raw_prob"] = 1/data["PSCA"]  
    return data

#9. real_probability_from_raw_prob(data) - fair probability (margin removed)
def real_probability_from_raw_prob(data):
    data = data.copy()
    data["sum_prob"] = (data["bookmaker_home_raw_prob"] + data["bookmaker_draw_raw_prob"] + data["bookmaker_away_raw_prob"])
    data["Real_home_prob"] = data["bookmaker_home_raw_prob"]/data["sum_prob"]
    data["Real_draw_prob"] = data["bookmaker_draw_raw_prob"]/data["sum_prob"]
    data["Real_away_prob"] = data["bookmaker_away_raw_prob"]/data["sum_prob"]
    return data

#10. accuracy_to_bookmaker_prob(data) - calculates the model accuracy compared to Pinnacle's probability 
def accuracy_to_bookmaker_prob(data):
    accuracy_table = data[["Date" , "HomeTeam" , "AwayTeam" , "FTHG" , "FTAG" , "FTR" , "Real_home_prob" , 'Real_draw_prob' , "Real_away_prob" , "H" , "A" , "D"]].copy()
    accuracy_table["avg_diff_from_pinnacle"] = (abs(accuracy_table["H"] - accuracy_table["Real_home_prob"]) + abs(accuracy_table["D"] - accuracy_table["Real_draw_prob"]) + abs(accuracy_table["A"] - accuracy_table["Real_away_prob"]))/3
    test_accuracy = 1- (accuracy_table["avg_diff_from_pinnacle"].mean())
    return test_accuracy

#Brier_score functions:
#11. add_outcomes(df): it is add a value for each outcome in each match (the value can be 0 or 1)
def add_outcomes(df):
    df["Home_output"] = (df["FTHG"] > df["FTAG"]).astype(int)
    df["Draw_output"] = (df["FTHG"] == df["FTAG"]).astype(int)
    df["Away_output"] = (df["FTHG"] < df["FTAG"]).astype(int)
    return df

#12. calculates the brier score for each match and gives back the average of the brier scores 
def brier_score_in_a_Dateframe(dataframe):
    model_home = dataframe["H"]
    model_draw = dataframe["D"]
    model_away = dataframe["A"]
    home_output = dataframe["Home_output"]
    draw_output = dataframe["Draw_output"]
    away_output = dataframe["Away_output"]
    overall_home_brier_score = 0
    home_brier_scores = (model_home - home_output)**2
    draw_brier_scores = (model_draw - draw_output)**2
    away_brier_scores = (model_away - away_output)**2
    overall_brier_scores = home_brier_scores + draw_brier_scores + away_brier_scores
    avrage_brier_scores = overall_brier_scores.mean()
    return avrage_brier_scores
