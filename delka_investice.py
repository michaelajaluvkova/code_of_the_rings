from datetime import datetime


def investment_duration(start_date: str, end_date: str, date_format: str = "%Y-%m-%d"):
    """
    Calculate the duration of an investment in years, months, or days,
    and return the result without unnecessary units (e.g., if duration is less than a year, exclude years).

    Parameters:
        start_date (str): The start date of the investment (format: YYYY-MM-DD).
        end_date (str): The end date of the investment (format: YYYY-MM-DD).
        date_format (str): The format of the date (default is "%Y-%m-%d").

    Returns:
        str: A string representation of the duration, excluding unnecessary units.
    """

    # Convert string dates to datetime objects
    start_date_obj = datetime.strptime(start_date, date_format)
    end_date_obj = datetime.strptime(end_date, date_format)

    # Calculate the difference in years, months, and days
    delta_years = end_date_obj.year - start_date_obj.year
    delta_months = end_date_obj.month - start_date_obj.month
    delta_days = end_date_obj.day - start_date_obj.day

    # Adjust for negative months and days
    if delta_days < 0:
        delta_months -= 1
        delta_days += (
            end_date_obj.replace(year=end_date_obj.year, month=end_date_obj.month - 1)
            - start_date_obj
        ).days

    if delta_months < 0:
        delta_years -= 1
        delta_months += 12

    # Build the result string without unnecessary units
    result = []
    if delta_years > 0:
        result.append(f"{delta_years} years")
    if (
        delta_months > 0 or delta_years > 0
    ):  # Show months only if there is a year or months exist
        result.append(f"{delta_months} months")
    if delta_days > 0:
        result.append(f"{delta_days} days")

    # Return the result as a string
    return ", ".join(result) if result else "0 days"
