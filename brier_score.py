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
from functions import (add_outcomes , brier_score_in_a_Dateframe)

def brier_score(data):
    test_data = data.copy()
    test_data = add_outcomes(test_data) 
    brier_score = brier_score_in_a_Dateframe(test_data)
    return brier_score





