#Result table creator file 
#This file collect all the results of different tests and create an overall table from them that is include all important data

import pandas as pd 
from pathlib import Path
from naive_model import main as naive_result
from team_strength import main as team_strenght_result 
from out_of_sample_test import main as out_of_sample

HERE = Path(__file__).parent

def main():
    strenghth_score ,naive_272_score , strength_brier , naive_272_brier , pinnacle_272_brier = team_strenght_result()
    naive_score , naive_brier = naive_result()
    oos_brier , pinnacle_oos_brier , oos_accuracy = out_of_sample()

    results = pd.DataFrame({
        "Model": ["Naive" , "Team strength" ,"Naive_on_team_strength_sample" , "OOS_strength_model" , "Pinnacle_24-25" , "Pinnacle_25-26"],
        "Matches": [380 , 272 , 272 , 272 , 272 , 272],
        "Metric": ["closeness" , "closeness" , "closeness" , "brier_score" , "brier_score" , "brier_score"],
        "Score": [naive_score , strenghth_score , naive_272_score , oos_brier , pinnacle_272_brier , pinnacle_oos_brier],
        "Pass_line": [">= 0.85" , "> naive on 272" , "- (baseline)" , "Pinnacle_brier > OOS_strength_model" , None , None],
        "Pass": [naive_score >= 0.85 , strenghth_score > naive_272_score , None , pinnacle_oos_brier > oos_brier , None , None], 
        "Brier_score": [naive_brier ,strength_brier , naive_272_brier , oos_brier , pinnacle_272_brier , pinnacle_oos_brier],
        
    })

    print(results.to_string())
    results.to_csv(HERE / "results.csv" , index=False)


if __name__ == "__main__":
    main()