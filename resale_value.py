import pandas as pd

df_makes = pd.read_csv('resale_value_make.csv')
df_models = pd.read_csv('resale_value_model.csv')

print(df_makes.head())
print(df_models.head())
