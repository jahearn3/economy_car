import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
from matplotlib.ticker import FuncFormatter
from utils import dollar_formatter


def model(t, C0, k):
    return C0 * np.exp(k * t)


printing = False
plotting = False
saving = True
results = []
df = pd.read_csv('three_row_suvs.csv')
years = np.array([5, 10])
for index, row in df.iterrows():
    costs = np.array([float(row['5-Yr_Maintenance_Cost']),
                      float(row['10-Yr_Maintenance_Cost'])])
    params, covariance = curve_fit(model, years, costs)
    C0, k = params

    # Calculate costs for each year from 1 to 10
    future_years = np.arange(1, 11)
    future_costs = np.round(model(future_years, C0, k), 2)
    label = str(row['Year']) + ' ' + row['Make'] + ' ' + row['Model']
    results.append([label] + list(future_costs))

    # Print the results
    if printing:
        for year, cost in zip(future_years, future_costs):
            print(f"Year {year}: Cost {cost:,.2f}")

    # Plot the results
    if plotting:
        filename = str(row['Year']) + '_' + row['Make'] + '_' + row['Model']
        plt.scatter(years, costs, color='red', label='Data Points')
        plt.plot(
            future_years, future_costs, label='Exponential Fit', color='blue'
        )
        plt.xlabel('Year')
        plt.ylabel('Maintenance Cost')
        plt.gca().yaxis.set_major_formatter(FuncFormatter(dollar_formatter))
        plt.title(label + ' Maintenance')
        plt.legend()
        plt.savefig(filename + '_Maintenance.png')
        plt.clf()

# Save the results to csv
if saving:
    # Convert results to a DataFrame for better visualization
    columns = ['Label'] + [f'Year_{i}' for i in range(1, 11)]
    results_df = pd.DataFrame(results, columns=columns)

    # Save the results to a CSV file
    results_df.to_csv('maintenance_costs_extrapolated.csv', index=False)

# TODO: Consider using a linear model for the first 5 years
# TODO: and then the exponential model for the following 5
