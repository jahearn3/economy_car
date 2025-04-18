import pandas as pd

df_makes = pd.read_csv('resale_value_make.csv')
df_models = pd.read_csv('resale_value_model.csv')
df_msrp = pd.read_csv('msrp.csv')

resale_cols = ['3-Yr_Resale_Value', '5-Yr_Resale_Value', '7-Yr_Resale_Value']

# Convert from percentage to float
for col in resale_cols:
    df_makes[col] = df_makes[col].str.replace('%', '').astype(float) / 100
    df_models[col] = df_models[col].str.replace('%', '').astype(float) / 100

# Merge the dataframes df_msrp and df_makes on 'Make'
df = pd.merge(df_msrp, df_makes, left_on='Make', right_on='Brand', how='left')

# Delete column Brand
df.drop(columns=['Brand'], inplace=True)

df['Make_and_Model'] = df['Make'] + ' ' + df['Model']

df = df.merge(
    df_models,
    left_on='Make_and_Model',
    right_on='Model',
    suffixes=('', '_new'),
    how='left'
    )

for col in resale_cols:
    df[col] = df[col + '_new'].combine_first(df[col])

df.drop(columns=[col + '_new' for col in resale_cols], inplace=True)

for col in resale_cols:
    df[col + '_USD'] = df['MSRP'] * df[col]

df['10-Yr_Resale_Value_USD'] = 0

for n in [0, 3, 5, 7]:  # year of purchase
    for m in [3, 5, 7, 10]:  # year of sale
        if n < m:
            if n == 0:
                purchase_val = 'MSRP'
            else:
                purchase_val = f'{n}-Yr_Resale_Value_USD'
            sale_val = f'{m}-Yr_Resale_Value_USD'
            df[f'diff_{n}_{m}'] = df[purchase_val] - df[sale_val]

for col in df.columns:
    if 'diff' in col:
        print(col)
        result_df_sorted = df.sort_values(by=col, ascending=True)
        print(result_df_sorted[['Make_and_Model', 'MSRP', col]].head())
        print()
