import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from utils import dollar_formatter_wrapper

df = pd.read_csv('three_row_suvs.csv')

resale_cols = ['3-Yr_Resale_Value', '5-Yr_Resale_Value', '7-Yr_Resale_Value']

for col in resale_cols:
    df[col] = df[col].str.replace('%', '').astype(float) / 100
    df[col + '_USD_min'] = df['Min_Retail_Price'] * df[col]
    df[col + '_USD_max'] = df['Max_Retail_Price'] * df[col]

# Assume 5 years of ownership
ownership_years = 5
annual_miles = 15000
avg_gas_price = 4.00

# Calculate the total cost of ownership
df['Total_Cost_min'] = (
    df['Min_Retail_Price'] +
    avg_gas_price * annual_miles * ownership_years / df['MPG'] +
    df['Annual_Insurance_Cost'] * ownership_years +
    df['5-Yr_Maintenance_Cost'] -
    df['5-Yr_Resale_Value_USD_min']
)
df['Total_Cost_max'] = (
    df['Max_Retail_Price'] +
    avg_gas_price * annual_miles * ownership_years / df['MPG'] +
    df['Annual_Insurance_Cost'] * ownership_years +
    df['5-Yr_Maintenance_Cost'] -
    df['5-Yr_Resale_Value_USD_max']
)

# See top 3 by Total_Cost_min
df_sorted_min = df.sort_values(by='Total_Cost_min', ascending=True)
print("Sorted by Total Cost (Min):")
print(df_sorted_min[['Year', 'Make', 'Model', 'Total_Cost_min']].head(3))

# See top 3 by Total_Cost_max
df_sorted_max = df.sort_values(by='Total_Cost_max', ascending=True)
print("\nSorted by Total Cost (Max):")
print(df_sorted_max[['Year', 'Make', 'Model', 'Total_Cost_max']].head(3))

df['Average_Cost'] = (df['Total_Cost_min'] + df['Total_Cost_max']) / 2
df_sorted_avg = df.sort_values(by='Average_Cost', ascending=False)
df_sorted_avg['Year_Make_Model'] = (df_sorted_avg['Year'].astype(str) + ' ' +
                                    df_sorted_avg['Make'] + ' ' +
                                    df_sorted_avg['Model'])

# Visualize total cost ranges sorted by average total cost
plt.figure(figsize=(10, 6))
for index, row in df_sorted_avg.iterrows():
    plt.hlines(y=row['Year_Make_Model'],
               xmin=row['Total_Cost_min'],
               xmax=row['Total_Cost_max'],
               color='blue',
               linewidth=2
               )
plt.title('Cost Ranges')
plt.xlabel('5-Year Total Cost')
plt.gca().xaxis.set_major_formatter(FuncFormatter(dollar_formatter_wrapper))
plt.tight_layout()
plt.savefig('5-yr_total_cost.png')
