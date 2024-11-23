from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/comparison', methods=['GET', 'POST'])
def comparison():
    if request.method == "POST":
        selected_crypto = request.form.get('cryptocurrency')
        selected_comparison = request.form.get('comparison')

        return render_template("result_comparison.html",
                               selected_crypto=selected_crypto,
                               selected_comparison=selected_comparison)

    else:
        cryptocurrencies = ['Bitcoin', 'Ethereum', 'Litecoin']
        comparisons = ['Stock', 'USD']
        return render_template('Comparison.html', cryptocurrencies=cryptocurrencies, comparisons=comparisons)

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    return render_template('calculator.html')

@app.route('/result_comparison')
def result_comparison():
    return render_template('result_comparison.html')

if __name__ == "__main__":
    app.run(debug=True)