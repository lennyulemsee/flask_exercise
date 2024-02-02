# Import libraries
from flask import Flask, url_for, redirect, render_template, request

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]
total_bal = 0


# Read operation
@app.route("/")
def get_transactions():
    return render_template("transactions.html", transactions=transactions)


# Create operation
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    """ adds a new transaction """

    # provider a the form to the user if requested.
    if request.method == "GET":
        return render_template("form.html")
    # take the data enter to the form by the user and add it to the list.
    if request.method == "POST":
        transaction = {
                'id': len(transactions)+1,
                'date': request.form['date'],
                'amount': float(request.form['amount'])
                }
        transactions.append(transaction)
        return redirect(url_for("get_transactions"))


# Update operation
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    if request.method == "GET":
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                return render_template("edit.html", transaction=transaction)

    if request.method == "POST":
        date = request.form['date']
        amount = float(request.form['amount'])

        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
        return redirect(url_for("get_transactions"))

    return render_template("transactions.html",
                           transaction=transactions[transaction_id - 1])


# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    del (transactions[transaction_id - 1])
    return redirect(url_for("get_transactions"))


# search operation
@app.route("/search", methods=["GET", "POST"])
def search_transactions():
    if request.method == "POST":
        mini = float(request.form["min_amount"])
        maxi = float(request.form["max_amount"])

        filtered_transactions = [trans for trans in transactions
                                 if trans['amount'] <= maxi and
                                 trans['amount'] >= mini]

        return render_template("transactions.html",
                               transactions=filtered_transactions)
    return render_template("search.html")


# total balance
@app.route('/balance')
def total_balance():
    bal = 0
    for tran in transactions:
        bal += float(tran['amount'])
    total_bal = f"total balance: {bal}"
    return render_template("transactions.html",
                           transactions=transactions, total_bal=total_bal)


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
