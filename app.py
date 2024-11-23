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
    # doplnit funkce na listy!
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
    return render_template('calculator.html')

if __name__ == "__main__":
    app.run(debug=True)
