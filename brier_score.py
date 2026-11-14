#This file contain a function and with this function the calculation of Brier score for each model:
    #Pinnacle probability model
    #Our naive model
    #Our Team strenght model
#We mesure wich model is better the naive model or the team_strenght model
#That model pass wich have the lower brier_score because brier score can be from 0 to 2 and if the score is lower that mean the calculation is more accurate
#Result:
    #Pinnacle_brier_score: 0.6187
    #Team_strenght_brier_score: 0.6459
    #Naive_model_brier_score: 0.6595
#So the Team strenght model won.
import pandas as pd
from team_strength import accuracy_table #the team strenght data 
from team_strength import naive_modell_run_on_the_same_sample
from out_of_sample_test import probability_with_strenght_test

def add_outcomes(df):
    df["Home_output"] = (df["FTHG"] > df["FTAG"]).astype(int)
    df["Draw_output"] = (df["FTHG"] == df["FTAG"]).astype(int)
    df["Away_output"] = (df["FTHG"] < df["FTAG"]).astype(int)
    return df

brier_score_out_of_sample_test = probability_with_strenght_test.copy()
brier_score_data_team_strenght_model = accuracy_table[["H" , "D" , "A" , "FTHG" , "FTAG"]].copy()
brier_score_data_team_strenght_model = add_outcomes(brier_score_data_team_strenght_model)
brier_score_out_of_sample_test = add_outcomes(brier_score_out_of_sample_test)

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

brier_score_pinnacle = accuracy_table.copy()
brier_score_pinnacle = add_outcomes(brier_score_pinnacle)
brier_score_pinnacle = brier_score_pinnacle.drop(columns=["H" , "D" , "A"])
brier_score_pinnacle = brier_score_pinnacle.rename(columns={"Fair_home": "H" , "Fair_draw": "D" , "Fair_away": "A"})

naive_modell_data = naive_modell_run_on_the_same_sample.copy()

naive_modell_data = naive_modell_data.rename(columns={"naive_model_home_win_%": "H" , "naive_model_draw_%": "D" , "naive_model_away_win_%": "A"})
naive_modell_data = add_outcomes(naive_modell_data)

brier_score_overall_table = pd.DataFrame({
    "Pinnacle_brier_score": [brier_score_in_a_Dateframe(brier_score_pinnacle)],
    "Team_strenght_brier_score": [brier_score_in_a_Dateframe(brier_score_data_team_strenght_model)],
    "Naive_modell_brier_score": [brier_score_in_a_Dateframe(naive_modell_data)],
    "OOS_test_brier_score": [brier_score_in_a_Dateframe(brier_score_out_of_sample_test)]
}) 

brier_score_overall_table.to_excel("Overall_brier_score_table.xlsx" , index=False)

