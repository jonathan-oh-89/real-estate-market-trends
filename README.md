# Real Estate Market Trends

This repo pulls together important market trends real estate investors look for. The data is aggregated for the top 50
metropolitan statistical areas.


# Motivation
This project was created to generate data for this dashboard:
https://public.tableau.com/profile/jonathan.oh2482#!/vizhome/Top50Metros-MacroTrendsforRealEstateInvestors/Dashboard1?publish=yes

# Directions
- Clone repo to your computer.
- Download the most recent data for Metros from https://www.redfin.com/news/data-center. Make sure you download using
all columns. Update the med_sale_price_Full_Data_data.csv file.
- Run redfin.py
- Run unemployment.py (will take a couple minutes)
- Run import_esri.py
- Run monthlytrends.py
- The result will be stored in metrostats.csv and monthlytrends.csv

# What's in the csv files
- monthlytrends.csv
  - Months of supply by month (Redfin)
  - Median sale price by month (Redfin)
  - Unemployment by month (Bureau of Labor Statistics)

- metrostats.csv
  - 2010-2020 Population (ESRI)
  - 2020 Property Types (ESRI)
  - 2020 Employment Industries (ESRI)




