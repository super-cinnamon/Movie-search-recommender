import os

import pandas as pd
import dotenv

dotenv.load_dotenv('./src/setup/.env')
data_path = os.getenv('RAW_DATA_PATH')
df = pd.read_csv(data_path)

# we need plot, genre, release year, and title
df.drop(columns=['Origin/Ethnicity', 'Director', 'Cast', 'Wiki Page'], inplace=True)

# Save into new file
df.to_csv('data/processed_data.csv', index=False)
