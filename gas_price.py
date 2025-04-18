import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from utils import dollar_formatter


# Import gas_prices.csv
df = pd.read_csv("gas_prices.csv")

# Discard incomplete rows
df.dropna(inplace=True)

# Calculate the average price for each year
# Exclude the 'Year' column when calculating the mean
df['Average'] = df.loc[:, 'Jan':'Dec'].mean(axis=1)

# Plotting the average gas prices
plt.figure(figsize=(10, 5))
plt.plot(df['Year'], df['Average'], marker='o')
plt.xlabel('Year')
plt.ylabel('Average Gas Price')
plt.gca().yaxis.set_major_formatter(FuncFormatter(dollar_formatter))
plt.xticks(df['Year'], rotation=45)  # Show all years on the x-axis
plt.tight_layout()
plt.savefig('avg_gas_price_by_year.png')
