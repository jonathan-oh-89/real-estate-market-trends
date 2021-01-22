import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


path = os.getcwd()

with open(os.path.join(path + '/files/redfin.csv')) as f:
    redfin = pd.read_csv(f)

with open(os.path.join(path + '/files/unemployment.csv')) as f:
    unemployment = pd.read_csv(f)

df = pd.merge(unemployment, redfin,  how='inner', left_on=['geographyid','date'], right_on=['geographyid','date'])

df[['monthsofsupply','mediansaleprice','unemploymentrate']] = df[['monthsofsupply','mediansaleprice','unemploymentrate']].astype(float)

df = df.to_csv('files/monthlytrends.csv', index=False)









