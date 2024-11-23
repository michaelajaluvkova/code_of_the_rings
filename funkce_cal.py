from datetime import datetime


def investment(initial_value, final_value, start_date: str, end_date: str) -> tuple:
    # Convert input strings to datetime objects
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

    # Calculate the difference in days
    delta = end_date_obj - start_date_obj

    # Convert the difference in days to years (accounting for leap years)
    years = delta.days / 365

    # Calculate the Compound Annual Growth Rate (CAGR)
    cagr = (final_value / initial_value) ** (1 / years) - 1

    investment_return = final_value - initial_value

    # Return both CAGR, the length of the investment in years, and the investment return
    return cagr, years, investment_return


initial_value = 1000
final_value = 1100
start_date = '2020-01-01'
end_date = '2023-01-01'

# Unpack the return values from the function
cagr, investment_length, investment_return = investment(initial_value, final_value, start_date, end_date)

# Print the results
print(f"The CAGR is {cagr:.2%} over {investment_length:.2f} years. Total return is {investment_return}")
