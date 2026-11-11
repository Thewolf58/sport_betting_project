# Premier League match Probability Model

## Goal
To improve my Python and statistics skills 
Learn the basics of machine learning
Develop a model that precisely calculates outcome probabilities close to the bookmakers 


## Definition of Done 
Deadline: 2026-11-20
- [x] Create a naive model which calculate the probability of H/D/A by home advantage 
- [x] Create a team strength model which calculate the probability of each outcome (H/D/A) from a strength model and home advantage formula 
- [x] Test how precise the naive model compared against professional bookmakers probability 
- [x] Test how precise the team strength model against professional bookmakers probability 
- [x] Compare the accuracy of the naive model and the team strength model in the same 272 data 
- [ ] Compare which model is better on Brier score include the Pinnacle's probability too on the same 272 data 
- [ ] Test the better model (which is have the better Brier score) in 2025-2026 Premier League data 
- [ ] Write down the model accuracy in the 2025-2026 data against the Pinnacle probability 
- [ ] Clean your code: No absolute path , no unused code , correct spelling , one command runs everything
- [ ] Create a professional README , gitignore , requirements document: README have a clear goal , how to run , results table , and a review at the end of it 
- [ ] Commit the final file to GitHub 


## Question
Can I good enough to develop a probability estimating model which is close to professional bookmakers
Can I produce good quality documentation and code to be able to publish it 
Can I finally finish a project before I move to an other 


## Rules
In this project the primary goal is to learn as much as we can 
So we only develop these models for education only 
A model only use data before an event happen to avoid overlook bias 
Before every test we need a why and when the test is going to fail and when it going to pass the test
We will only use the 2025-2026 Premier League season data to test our best strategy
Because we use only training season to train our models we can't train our model for the promoted teams so we only test the models in 272 match/season

## Data
 Data comes from: football-data.co.uk for each test we need to write down what data we use 
 1. Naive model: from football-data.co.uk: Premier league data from 2023-2025 include 2 season: 23-24 , 24-25
 2. Team strength model: from football-data.co.uk: Premier league data from 2023-2025 include 2 season: 23-24 , 24-25


## Benchmarks
For each test we write it down what we compare our model against our model(other bookmakers etc .):
1. Naive model: we compared against the official Pinnacle probability number from the odds
2. We will compare against the Naive model accuracy and the Pinnacle odds 
    

## Roadmap
1. Naive model that measure in 24/25 session the home advantage only and use that numbers to see that in the following season which match have a lower probability that we expected and we bet that lower probability 
2. Team strength model: it watches the average scored and average conceded goals for all team in 23/24 and it will test it in 24/25 (we will exclude the promoted teams from the 24/25 teams because we don't have data from they)
3. Write each model Brier score put every model's result into an overall xlsx table and compare the Naive model the Team strength model and the Pinnacle's Brier score against each other and look at it which have the best 

## Result
1. Naive model = 0.881 vs Pinnacle (24/25) Pass (line >= 0.85)
2. Team strength model: Pass line: Better accuracy to the Pinnacle probability than the Naive model , Pass: True , Team strength: 0.935 , Naive model: 0.897
3. 2025/26 season data model Pass line: If the Pinnacle Brier score > Our model Brier score

## How to run
1. Python 3.9+
2. pip install -r requirements.txt 
3. to download the needed data run the download_data.py file 
4. if you want to see the accuracy of the naive model run the naive_model.py
5. if you want to see the accuracy of the team strength model run the team_strength.py
