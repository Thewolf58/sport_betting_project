#Naive Modell: In this modell we are only going to test the method of testing a football match
#testing period session = x
#tuning session = x - 1 session
#We want to tune our modell on the tuning session
#And with the tuned modell we test the modell in testing period session
#We will test the modell only in premier leauge and only in one session
#And we only tune this model one session too 
#For the compare we will create for every match new odds in the testing period session and we will compare againts the pinnacle close odds to see how far is our model compare to a professional bookmaker
#testing period session = 2024/2025
#Tuning session = 2023/2024
#Mesure our modell accuraccy = how far from our modell decimals(in absolute value) (like 0.65 wich means 65%) is pinnacle decimals (like 0.35) = 0.65-0.35 = 0.3
#The modell pass if the avrage (home , away and draw all over the 380 matches) accuraccy compared to pinnacle is bigger or equal than 85%
#Because this is just one output and if it is that accurate than it is a good starting point 
#Result: 0,881 , PASS: True

import pandas as pd 
from pathlib import Path

#Set the paths to the data files
HERE = Path(__file__).parent
DATA_DIR = HERE / "datas"

#Load the data for the test
tuning_data = pd.read_csv(DATA_DIR / "prem_data_23_24.csv")
testing_period_data = pd.read_csv(DATA_DIR / "prem_data_24_25.csv")

#Section 1: Build the model
def naiv_model_table(data):
    total_match = len(data)
    pitch_where = data["FTR"].value_counts()
    naiv_model = pd.DataFrame({
        "avrage_%_of_home_win": [(pitch_where["H"]/total_match)*100],
        "avrage_%_of_draw": [(pitch_where["D"]/total_match)*100],
        "avrage_%_of_away_win": [(pitch_where["A"]/total_match)*100]
    })
    return naiv_model

naiv_model = naiv_model_table(tuning_data)

#The naiv_modell_odds will be our fair odds for all match in testing period data
naiv_modell_odds = pd.DataFrame({
    "ODDS_of_home_win": [1/(naiv_model["avrage_%_of_home_win"][0]/100)],
    "ODDS_of_draw": [1/(naiv_model["avrage_%_of_draw"][0]/100)],
    "ODDS_of_away_win": [1/(naiv_model["avrage_%_of_away_win"][0]/100)],
})

#2. part of the model is use the model on the testing_period_data

#Rules if the odds is bigger than our odds for home win then we place a bet

#First calculate the fair value of an odds 
naiv_modell_data = testing_period_data[["Date" , "Time" , "HomeTeam" , "AwayTeam" , "FTR", "PSCH", "PSCD" , "PSCA"]].copy()
naiv_modell_data['Home_probability'] = 1/naiv_modell_data["PSCH"]
naiv_modell_data['Draw_probability'] = 1/naiv_modell_data["PSCD"]
naiv_modell_data['Away_probability'] = 1/naiv_modell_data["PSCA"]
naiv_modell_data['sum_probability'] = naiv_modell_data["Home_probability"] + naiv_modell_data["Draw_probability"] + naiv_modell_data["Away_probability"]
naiv_modell_data["Brokerage_edge"] = naiv_modell_data["sum_probability"] - 1
naiv_modell_data["Real_home_probability"] = naiv_modell_data["Home_probability"]/naiv_modell_data["sum_probability"]
naiv_modell_data["Real_draw_probability"] = naiv_modell_data["Draw_probability"]/naiv_modell_data["sum_probability"]
naiv_modell_data["Real_away_probability"] = naiv_modell_data["Away_probability"]/naiv_modell_data["sum_probability"]

#Create a final table wich include all important data to our calculation
our_modell_result = naiv_modell_data[["Date" , "Time" , "HomeTeam" , "AwayTeam", "Real_home_probability" , "Real_draw_probability" , "Real_away_probability" , ]].copy()
our_modell_result["naiv_model_home_prob"] = 1/(naiv_modell_odds["ODDS_of_home_win"].iloc[0])
our_modell_result["naiv_model_draw_prob"] = 1/(naiv_modell_odds["ODDS_of_draw"].iloc[0])
our_modell_result["naiv_model_away_prob"] = 1/(naiv_modell_odds["ODDS_of_away_win"].iloc[0])
our_modell_result["Home_accuracy"] = 1 - (abs(our_modell_result["Real_home_probability"] - our_modell_result["naiv_model_home_prob"]))
our_modell_result["Draw_accuracy"] = 1 - (abs(our_modell_result["Real_draw_probability"] - our_modell_result["naiv_model_draw_prob"]))
our_modell_result["Away_accuracy"] = 1 - (abs(our_modell_result["Real_away_probability"] - our_modell_result["naiv_model_away_prob"]))

#Calculate the avrage accuracy for each collum
home_accuracy_mean = our_modell_result["Home_accuracy"].mean()
draw_accuracy_mean = our_modell_result["Draw_accuracy"].mean()
away_accuracy_mean = our_modell_result["Away_accuracy"].mean()

#The final avrage accuracy num:
avrage_accuracy = (home_accuracy_mean + draw_accuracy_mean + away_accuracy_mean)/3

if avrage_accuracy >= 0.85:
    naiv_model_pass = "True"
else:
    naiv_model_pass = "False"

print(avrage_accuracy)
