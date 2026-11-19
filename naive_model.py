#Naive Model: The simplest possible baseline for predicting a football match outcome 
#Every match gets the same home / draw / away probabilities 
#Training season = 2023/24 (the share of home wins, draws and away wins)
#Test season = 2024/25 
#Test only in premier league matches 
#We compare our probabilities with Pinnacle's closing odds (margin removed)
#to see how close our model is to a professional bookmaker
#closeness per outcome = 1 - |our probability - Pinnacle's probability|
#Pass line: average closeness (home , draw, away,  all 380 matches) >= 0.85
#Result: 0.8812 PASS
#Brier score (380 matches): 0.6572

import pandas as pd 
from pathlib import Path
from functions import (naive_model_table , add_outcomes , brier_score_in_a_Dateframe)

#Set the paths to the data files
HERE = Path(__file__).parent
DATA_DIR = HERE / "datas"

def main():

    #Load the data for the test
    tuning_data = pd.read_csv(DATA_DIR / "prem_data_23_24.csv")
    testing_period_data = pd.read_csv(DATA_DIR / "prem_data_24_25.csv")
    naive_model = naive_model_table(tuning_data)

    #Section 2: Use the model on the test season

    #Calculate Pinnacle's fair probabilities from the odds
    naive_model_data = testing_period_data[["Date" , "Time" , "HomeTeam" , "AwayTeam" , "PSCH", "PSCD" , "PSCA" , "FTAG" , "FTHG"]].copy()
    naive_model_data['Home_probability'] = 1/naive_model_data["PSCH"]
    naive_model_data['Draw_probability'] = 1/naive_model_data["PSCD"]
    naive_model_data['Away_probability'] = 1/naive_model_data["PSCA"]
    naive_model_data['sum_probability'] = naive_model_data["Home_probability"] + naive_model_data["Draw_probability"] + naive_model_data["Away_probability"]
    naive_model_data["Real_home_probability"] = naive_model_data["Home_probability"]/naive_model_data["sum_probability"]
    naive_model_data["Real_draw_probability"] = naive_model_data["Draw_probability"]/naive_model_data["sum_probability"]
    naive_model_data["Real_away_probability"] = naive_model_data["Away_probability"]/naive_model_data["sum_probability"]

    #Create a table with Pinnacle's probabilities and ours 
    our_model_result = naive_model_data[["Date" , "Time" , "HomeTeam" , "AwayTeam", "Real_home_probability" , "Real_draw_probability" , "Real_away_probability" , "FTAG" , "FTHG" ]].copy()
    our_model_result["naive_model_home_prob"] = (naive_model["average_%_of_home_win"].iloc[0])/100
    our_model_result["naive_model_draw_prob"] = (naive_model["average_%_of_draw"].iloc[0])/100
    our_model_result["naive_model_away_prob"] = (naive_model["average_%_of_away_win"].iloc[0])/100
    our_model_result["Home_accuracy"] = 1 - (abs(our_model_result["Real_home_probability"] - our_model_result["naive_model_home_prob"]))
    our_model_result["Draw_accuracy"] = 1 - (abs(our_model_result["Real_draw_probability"] - our_model_result["naive_model_draw_prob"]))
    our_model_result["Away_accuracy"] = 1 - (abs(our_model_result["Real_away_probability"] - our_model_result["naive_model_away_prob"]))

    #Calculate the average accuracy for each column
    home_accuracy_mean = our_model_result["Home_accuracy"].mean()
    draw_accuracy_mean = our_model_result["Draw_accuracy"].mean()
    away_accuracy_mean = our_model_result["Away_accuracy"].mean()

    #Calculate the brier score
    naive_brier = our_model_result.copy()
    naive_brier = naive_brier.rename(columns={"naive_model_home_prob": "H" , "naive_model_draw_prob": "D" , "naive_model_away_prob": "A"})
    naive_brier = add_outcomes(naive_brier)
    naive_brier = brier_score_in_a_Dateframe(naive_brier)


    #The final avrage accuracy
    average_accuracy = (home_accuracy_mean + draw_accuracy_mean + away_accuracy_mean)/3
    print(f"Naive model average accuracy to pinnacle's probability: {average_accuracy}")
    print(f"Naive model brier_score on 380 match: {naive_brier}")
    return [average_accuracy , naive_brier]

if __name__ == "__main__":
    main()