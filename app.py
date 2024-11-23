from flask import Flask, render_template, request, redirect, url_for
from engeto import DataDownloads
from datetime import datetime


downloader = DataDownloads()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/comparison', methods=['GET', 'POST'])
def comparison():
    cryptocurrencies = downloader.get_top_10_cryptos()
    #cryptocurrencies = ['Bitcoin', 'Ethereum', 'Litecoin']
    comparisons = ['Stock', 'USD']
    selected_date = None

    if request.method == "POST":
        selected_crypto = request.form.get('cryptocurrency')
        selected_comparison = request.form.get('comparison')
        selected_date = request.form.get('date')
        error_messages = []

        # Check if cryptocurrency and comparison are valid
        if selected_crypto not in cryptocurrencies or selected_comparison not in comparisons:
            error_messages.append("Invalid selection! Please choose a valid cryptocurrency and comparison to it.")

        # Check if the selected cryptocurrency and comparison are the same
        if selected_crypto == selected_comparison:
            error_messages.append(
                "The cryptocurrency and comparison cannot be the same. Please select different values.")

        # Check if a date is selected
        if not selected_date:
            error_messages.append("Please select a valid date.")

        # Validate date format
        try:
            valid_date = datetime.strptime(selected_date, '%Y-%m-%dT%H:%M')
        except (ValueError, TypeError) as e:
            if not "Please select a valid date." in error_messages:
                error_messages.append("Invalid date format. Please select a valid date and time.")

        # If there are error messages, return the template with them
        if error_messages:
            return render_template("Comparison.html", cryptocurrencies=cryptocurrencies, comparisons=comparisons,
                                   error_message="\n".join(
                                       error_messages))  # Join the error messages with <br> for new lines

        # here enter values for the template to show!

        return render_template("result_comparison.html", selected_crypto=selected_crypto,
                               selected_comparison=selected_comparison)

    else:
        return render_template('Comparison.html', cryptocurrencies=cryptocurrencies, comparisons=comparisons)

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    cryptocurrencies = downloader.get_top_10_cryptos()
    if request.method == "POST":
        coin = request.form.get('coin')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        amount = request.form.get('amount')
        error_messages = []

        # Validate coin
        if coin not in cryptocurrencies:
            error_messages.append("Invalid coin selected. Please select a valid cryptocurrency.")

        # Validate dates
        if not start_date or not end_date:
            error_messages.append("Both start date and end date are required.")
        else:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%dT%H:%M')

                if start_date_obj >= end_date_obj:
                    error_messages.append("Start date must be earlier than end date.")
            except ValueError:
                error_messages.append("Invalid date format. Please select valid start and end dates.")

        # Validate amount
        try:
            amount = float(amount)
            if amount < 0:
                error_messages.append("Amount must be a positive number.")
        except ValueError:
            error_messages.append("Invalid amount. Please enter a valid number.")

        # If there are any error messages, return the template with errors
        if error_messages:
            return render_template("calculator.html", cryptocurrencies=cryptocurrencies, error_messages=error_messages)

        # If no errors, process the valid data (example: display the result or perform calculations)
        return render_template("result_calculator.html", coin=coin, start_date=start_date, end_date=end_date,
                               amount=amount)

    return render_template("calculator.html", cryptocurrencies=cryptocurrencies)


if __name__ == "__main__":
    app.run(debug=True)
