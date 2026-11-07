import pandas as pd

prem_data_23_24 = pd.read_csv("https://football-data.co.uk/mmz4281/2324/E0.csv")
prem_data_24_25 = pd.read_csv("https://football-data.co.uk/mmz4281/2425/E0.csv")

prem_data_23_24.to_csv("/Users/lukacsadam/python/sport_betting_project/datas/prem_data_23_24.csv")
prem_data_24_25.to_csv("/Users/lukacsadam/python/sport_betting_project/datas/prem_data_24_25.csv")

