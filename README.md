# Real Estate Market Trends

This repo pulls together important market trends real estate investors look for. The data is aggregated for the top 50
metropolitan statistal areas.

The following data can be retrieved:

- Months of supply by month (Redfin)
- Median sale price by month (Redfin)
- Unemployment by month (Bureau of Labor Statistics)
- 2010-2020 Population (ESRI)
- 2020 Property Types (ESRI)
- 2020 Employment Industries (ESRI)

# Motivation
This project was created to generate data for this dashboard:
https://public.tableau.com/profile/jonathan.oh2482#!/vizhome/Top50Metros-MacroTrendsforRealEstateInvestors/Dashboard1?publish=yes

# Directions
- Clone repo to your computer.
- Download the most recent data for Metros from https://www.redfin.com/news/data-center. Make sure you download using
all columns. Update the med_sale_price_Full_Data_data.csv file.
- Run redfin.py
- Run unemploment.py (will take a couple minutes)
- Run import_esri.py
- Run monthlytrends.py




