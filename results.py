#Result table creator file 
#This file collect all the results of different tests and create an overall table from them that is include all important data

import pandas as pd 
from pathlib import Path
from naive_model import main as naive_result
from team_strength import main as team_strenght_result 

HERE = Path(__file__).parent

def main():
    strenghth_score ,naive_272_score = team_strenght_result()
    naive_score = naive_result()

    results = pd.DataFrame({
        "Model": ["Naive" , "Team strength" ,"Naive_on_team_strength_sample"],
        "Matches": [380 , 272 , 272],
        "Metric": ["closeness" , "closeness" , "closeness"],
        "Score": [naive_score , strenghth_score , naive_272_score],
        "Pass_line": [">= 0.85" , "> naive on 272" , "- (baseline)"],
        "Pass": [naive_score >= 0.85 , strenghth_score > naive_272_score , None]
    })

    print(results.to_string())
    results.to_csv(HERE / "results.csv" , index=False)

if __name__ == "__main__":
    main()