import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from utils import dollar_formatter_wrapper

# df = pd.read_csv('three_row_suvs.csv')
# df = pd.read_csv('commuter_cars.csv')
df = pd.read_csv('cheapest_commuter_cars.csv')

# resale_cols = ['3-Yr_Resale_Value', '5-Yr_Resale_Value', '7-Yr_Resale_Value']

# for col in resale_cols:
#     df[col] = df[col].str.replace('%', '').astype(float) / 100
#     df[col + '_USD_min'] = df['Min_Retail_Price'] * df[col]
#     df[col + '_USD_max'] = df['Max_Retail_Price'] * df[col]

df['Age'] = df['Year'].apply(lambda x: 2025 - x)
# df['Age_Enhancement'] = (df['Age'] / 10)**2
# df['Annual_Maintenance'] = (
#     df['5-Yr_Maintenance_Cost'] +
#     (df['Age_Enhancement'] * (
#         (df['10-Yr_Maintenance_Cost'] - df['5-Yr_Maintenance_Cost']) / 5
#     ))
# )
k = 0.05
df['Age_Enhancement'] = 1 + (k * (df['Age'] - 12))
df['Annual_Maintenance'] = (
    df['Year_12_Estimated_Annual_Maintenance'] * df['Age_Enhancement']
)

df['Difficult_Replacement_Part_Cost'] = np.where(
    df['Last_Year_Produced'] > 0,
    (2025 - df['Last_Year_Produced']) *
    (df['Annual_Maintenance'] / 10),
    0
)
df['Difficult_Replacement_Part_Cost'] = np.where(
    df['Model'] == 'Prius',
    df['Difficult_Replacement_Part_Cost'] + 3250,
    df['Difficult_Replacement_Part_Cost']
)

# Drop rows with the following makes
makes_to_drop = ['Dodge', 'Chevrolet', 'Kia', 'Ford']
df = df[~df['Make'].isin(makes_to_drop)]

# Assume N years of ownership
ownership_years = 3
annual_miles = 15000
avg_gas_price = 4.00

# Calculate the total cost of ownership
if ownership_years == 5:
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
else:  # Using the car until it breaks down (not selling it afterward)
    df['Total_Cost_min'] = (
        df['Min_Retail_Price'] +
        avg_gas_price * annual_miles * ownership_years / df['MPG'] +
        df['Annual_Insurance_Cost'] * ownership_years +
        df['Annual_Maintenance'] * ownership_years +
        df['Difficult_Replacement_Part_Cost']
    )
    df['Total_Cost_max'] = (
        df['Max_Retail_Price'] +
        avg_gas_price * annual_miles * ownership_years / df['MPG'] +
        df['Annual_Insurance_Cost'] * ownership_years +
        df['Annual_Insurance_Cost'] * ownership_years +
        df['Annual_Maintenance'] * ownership_years +
        df['Difficult_Replacement_Part_Cost']
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

# Keep only the top N rows for visualization
df_sorted_avg = df_sorted_avg.tail(20)

# Visualize total cost ranges sorted by average total cost
plt.figure(figsize=(10, 6))
for index, row in df_sorted_avg.iterrows():
    plt.hlines(y=row['Year_Make_Model'],
               xmin=row['Total_Cost_min'],
               xmax=row['Total_Cost_max'],
               color='blue',
               linewidth=3
               )
plt.title('Cost Ranges')
plt.xlabel(f'{ownership_years}-Year Total Cost')
plt.gca().xaxis.set_major_formatter(FuncFormatter(dollar_formatter_wrapper))
plt.tight_layout()
plt.savefig(f'{ownership_years}-yr_total_cost.png')


# Pie chart snapshots by year
# for ownership_years in range(10):
    # Used vehicle purchase

    # Insurance

    # Gas

    # Maintenance
