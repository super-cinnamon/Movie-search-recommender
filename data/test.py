import os

import pandas as pd
import dotenv


df = pd.read_csv('data\processed_data.csv')

df = df[(df['Release Year']==2009) & (df['Genre'].str.contains('comedy'))]

print(df.shape)

