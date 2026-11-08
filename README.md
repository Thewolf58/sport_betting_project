Premier League match Probabililty Model

Goal: 
    For me personally to improve my python statistics skills and learn Machine learning 
    And develop a model that is close to the probability that the bookmakers see 
    And if possibe create a Modell that can gain profitr 

Question: 
    I want to know that whether I'm good enoght or not to develop a modell close to the bookmakers
    And can i learn machine learning and what is that, how difficult it is 

Rules:
    In this project the primary goal is to learn as much as we can 
    So we only "trade" with paper money until we see result 
    A modell only use data before an event happen to avoid overlook bias 
    Before every test we need a why and when the test is going to fail and when it going to pass the test
    We will only use the 2025-2026 premier league season data to test our best strategy

Data:
    Data comes from: football-data.co.uk for each test we need to write down what data we use 
    1. Naiv modell: from football-data.co.uk: Premier leauge data from 2023-2025 include 2 season: 23-24 , 24-25
    2. Team strenght modell: from football-data.co.uk: Premier leauge data from 2023-2025 include 2 season: 23-24 , 24-25


Benchmarks:
    For each test we write it down what we compare our model againts our modell(other bookmakers etc .):
        1. Naiv modell: we compared againts the offical pinnacle probability number from the odds
        2. We will compare againts the Naiv modell accuracy and the pinnacle odds 
    

Roadmap: 
    1. Naiv modell that mesure in 24/25 session the home advantage only and use that numbers to see that in the following season wich match have a lower probability that we expected and we bet that lower probability 
    2. Team strenght modell: it watches the avrage scored and avrage concered goals for all team in 23/24 and it will test it in 24/25 (we will execute the promoted teams from the 24/25 teams because we dont have data from they)

Result: 
    1. Naive model = 0.881 vs Pinnacle (24/25) Pass (line >= 0.85)
    2. Team strenght modell: Pass line: Better accuracy to the Pinnacle probability than the Naiv modell , Pass: 

What we learned:
    2. How to use groupby function 