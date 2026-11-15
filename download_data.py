#This file downloads the data used by the following tests: 
    #Naive model
    #Team strength model
    #Out of sample test
#All data is downloaded from www.football-data.co.uk
#Run this script to download the data

import pandas as pd
from pathlib import Path

#Set where the data is saved
HERE = Path(__file__).parent
DATA_DIR = HERE / "datas"

def main(): 
    #Create the data folder if it doesn't exist
    DATA_DIR.mkdir(exist_ok=True)

    #download the data into Dataframe
    prem_data_23_24 = pd.read_csv("https://football-data.co.uk/mmz4281/2324/E0.csv")
    prem_data_24_25 = pd.read_csv("https://football-data.co.uk/mmz4281/2425/E0.csv")
    prem_data_25_26 = pd.read_csv("https://football-data.co.uk/mmz4281/2526/E0.csv")

    #Save the Dataframes as CSV files
    prem_data_23_24.to_csv(DATA_DIR / "prem_data_23_24.csv" , index=False)
    prem_data_24_25.to_csv( DATA_DIR / "prem_data_24_25.csv" , index=False)
    prem_data_25_26.to_csv(DATA_DIR /"prem_data_25_26.csv" , index=False)

if __name__ == "__main__":
    main()


