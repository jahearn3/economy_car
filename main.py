import pandas as pd


def estimate_vehicle_cost(
        df,
        ownership_years,
        annual_miles,
        fuel_price,
        highway_fraction=0.5):
    """
    Estimate the total cost of owning vehicles based on a DataFrame containing
    vehicle data.

    Parameters:
    - df: DataFrame containing vehicle data including purchase price, fuel
            efficiency, annual maintenance costs, annual repair costs, and
            depreciation rates.
    - ownership_years: Number of years the vehicles will be owned.
    - annual_miles: Number of miles per year.
    - fuel_price: Price of fuel per gallon.
    - highway_fraction: Fraction of highway miles (default is 0.5, meaning 50%
            highway miles).

    Returns:
    - DataFrame with total cost and estimated resale value for each vehicle.
    """
    # Calculate average fuel economy based on city and highway MPG
    df['Average_MPG'] = (
        (df['MPG_City'] * (1 - highway_fraction)) +
        (df['MPG_Highway'] * highway_fraction)
    )

    # Calculate total cost for each vehicle
    df['Total_Fuel_Cost'] = (
        (annual_miles * ownership_years / df['Average_MPG']) * fuel_price
    )
    df['Total_Maintenance_Cost'] = (
        df['Annual_Maintenance_Cost'] * ownership_years
    )
    df['Total_Repair_Cost'] = df['Annual_Repair_Cost'] * ownership_years

    # Calculate depreciation and resale value
    df['Resale_Value'] = round(
        df['Purchase_Price'] *
        (1 - df['Depreciation_Rate']) ** ownership_years,
        2
    )
    df['Total_Cost'] = round(
        (
            df['Purchase_Price'] +
            df['Total_Fuel_Cost'] +
            df['Total_Maintenance_Cost'] +
            df['Total_Repair_Cost'] -
            df['Resale_Value']
        ),
        2
    )

    return df[['Year', 'Make', 'Model', 'Total_Cost', 'Resale_Value']]


df = pd.read_csv("car_comparison_data.csv")
ownership_years = 8
annual_miles = 15000
fuel_price = 4.00
highway_fraction = 0.7
min_seating = 6

filtered_df = df[df['Seating'] >= min_seating]

# Estimate vehicle costs
result_df = estimate_vehicle_cost(
    filtered_df,
    ownership_years,
    annual_miles,
    fuel_price,
    highway_fraction
    )

# Sort the results by Total Cost in ascending order
result_df_sorted = result_df.sort_values(by='Total_Cost', ascending=True)

# Display the sorted results
print(result_df_sorted.head())
