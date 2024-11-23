from flask import Flask, render_template, request, redirect, url_for
from engeto import DataDownloads
from datetime import datetime
from funkce_cal import investment

from datetime import datetime

downloader = DataDownloads()

app = Flask(__name__)

"""
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/comparison', methods=['GET', 'POST'])
def comparison():
    cryptocurrencies = downloader.get_top_10_cryptos_denca()
    #cryptocurrencies = ['Bitcoin', 'Ethereum', 'Litecoin']
    comparisons = downloader.get_top_10_cryptos_denca() + ['S&P 500']

    selected_date = None

    if request.method == "POST":
        selected_crypto = request.form.get('cryptocurrency')
        selected_comparison = request.form.get('comparison')
        selected_date = request.form.get('date')
        error_messages = []

        # Check if cryptocurrency and comparison are valid
        if selected_crypto not in cryptocurrencies or selected_comparison not in comparisons:
            error_messages.append("Neplatná volba! Prosím zvolte platnou kryptoměnu a srovnávací bázi.")

        # Check if the selected cryptocurrency and comparison are the same
        if selected_crypto == selected_comparison:
            error_messages.append(
                "Kryptoměna a srovnávací báze nemohou být stejné. Prosím vyberte jiné hodnoty.")

        # Check if a date is selected
        if not selected_date:
            error_messages.append("Prosím zvolte platné datum.")

        # Validate date format
        try:
            valid_date = datetime.strptime(selected_date, '%Y-%m-%d')
        except (ValueError, TypeError) as e:
            if not "Please select a valid date." in error_messages:
                error_messages.append("Neplatný formát data. Prosím zvolte platné datum a čas.")

        # If there are error messages, return the template with them
        if error_messages:
            return render_template("Comparison.html", cryptocurrencies=cryptocurrencies, comparisons=comparisons,
                                   error_message="\n".join(
                                       error_messages))  # Join the error messages with <br> for new lines

        # here enter values for the template to show!

        return render_template("comparison.html", cryptocurrencies=cryptocurrencies, comparisons=comparisons, posted=1)

    else:
        return render_template('Comparison.html', cryptocurrencies=cryptocurrencies, comparisons=comparisons)
"""
@app.route('/', methods=['GET', 'POST'])
def calculator():
    cryptocurrencies = downloader.get_top_10_cryptos_denca()
    comparisons = downloader.get_top_10_cryptos_denca() + ['S&P 500']
    
    if request.method == "POST":
        coin = request.form.get('coin')
        selected_comparison = request.form.get('comparison')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        amount = request.form.get('amount')
        error_messages = []

        # Validate coin
        # Check if cryptocurrency and comparison are valid
        if coin not in cryptocurrencies or selected_comparison not in comparisons:
            error_messages.append("Neplatná volba! Prosím zvolte platnou kryptoměnu a srovnávací bázi.")

        # Check if the selected cryptocurrency and comparison are the same
        if coin == selected_comparison:
            error_messages.append(
                "Kryptoměna a srovnávací báze nemohou být stejné. Prosím vyberte jiné hodnoty.")
        # Validate dates
        if not start_date or not end_date:
            error_messages.append("Je vyžadováno datum začátku a datum konce.")
        else:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

                if start_date_obj >= end_date_obj:
                    error_messages.append("Datum začátku musí být dřívější než konečné datum.")
            except ValueError:
                error_messages.append("Neplatný formát data. Prosím zvolte platné datum začátku a konce.")

        # Validate amount
        try:
            amount = int(amount)
            if amount < 0:
                error_messages.append("Množství musí být kladné číslo.")
        except ValueError:
            error_messages.append("Neplatné množství. Prosím zvolte platné číslo.")

        # If there are any error messages, return the template with errors
        if error_messages:
            return render_template("calculator.html", cryptocurrencies=cryptocurrencies,
                                   error_message="\n".join(
                                       error_messages))  # Join the error messages with <br> for new lines
        # here enter the function calling
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        date_difference = end_date_obj - start_date_obj
        investment_length = date_difference.days

#        if investment_length == 1:
 #           year_word = "rok"
  #      elif 1 < investment_length < 2:
   #         year_word = "roku"
    #    else:
     #       year_word = "let"
            
        data = downloader.main(start_date=start_date, end_date=end_date)
        plot = Plotting()
        plot.run_plot(start_date, end_date, data, initial_investment, first=coin,
                      second=seleted_comparison)  #### creates media/crypto.png

        cagr, cagr2, final_value, final_value2, years, investment_return, investment_return2 = plot.investment(
            initial_investment, start_date, end_date, data, first=coin, second=selected_comparison)

        result_message = f"Složená roční míra růstu u {coin} je {cagr:.2%} za dobu {investment_length:.2f} dni. Výnos je {investment_return} Kč. Složená roční míra růstu u {selected_comparison} je {cagr2:.2%} za dobu {investment_length:.2f} dni. Výnos je {investment_return2} Kč."
        # If no errors, process the valid data (example: display the result or perform calculations)
        return render_template("calculator.html", coin=coin, start_date=start_date, end_date=end_date,
                               amount=amount, result_message=result_message, posted=1)

    return render_template("calculator.html", cryptocurrencies=cryptocurrencies, comparisons=comparisons)


if __name__ == "__main__":
    app.run(debug=True)
