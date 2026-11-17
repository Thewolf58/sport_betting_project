#Functions
#This file contains all function that I used in my tests 
#Functions: 
    #1. naive_model_table(data) – share (%) of home wins, draws and away wins in the training data

import pandas as pd 
import pathlib as Path

#Naive model functions 
#1: Build the model
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
#2: 