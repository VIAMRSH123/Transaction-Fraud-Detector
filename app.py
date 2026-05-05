from flask import Flask, render_template, request
import pandas as pd
import joblib
import numpy as np
import random

app = Flask(__name__)

model = joblib.load("fraud_model.pkl")
scaler = joblib.load("scaler.pkl")

payment_modes = ["UPI", "VISA Card", "MasterCard", "NetBanking", "Debit Card"]
upi_handles = ["@oksbi", "@okhdfc", "@okicici", "@ybl", "@paytm"]

@app.route('/', methods=['GET', 'POST'])
def home():
    data = pd.read_csv("transactions.csv")

    total = len(data)
    fraud = len(data[data['Class'] == 1])
    legit = len(data[data['Class'] == 0])

    sample_transactions = data[['Time', 'Amount', 'Class']].tail(8).values.tolist()

    alerts = []
    txn_no = 1041

    for row in sample_transactions:
        txn_id = "TXN" + str(txn_no)
        mode = random.choice(payment_modes)
        user = "user" + str(random.randint(10,99)) + random.choice(upi_handles)
        amount = round(row[1],2)
        status = "FRAUD ALERT" if row[2] == 1 else "SAFE"

        alerts.append([txn_id, mode, user, amount, status])
        txn_no += 1

    result = ""

    if request.method == 'POST':
        time = float(request.form['time'])
        amount = float(request.form['amount'])

        dummy = np.zeros((1,30))
        dummy[0][0] = time
        dummy[0][-1] = amount

        dummy[:, [0,29]] = scaler.transform(dummy[:, [0,29]])
        pred = model.predict(dummy)

        fraud_score = 0

        if pred[0] == 1:
            fraud_score += 1

        if amount > 180:
            fraud_score += 1

        if time > 45:
            fraud_score += 1

        if fraud_score >= 2:
            result = "🚨 FRAUD ALERT DETECTED"
        else:
            result = "✅ LEGITIMATE TRANSACTION"

    return render_template("index.html",
                           total=total,
                           fraud=fraud,
                           legit=legit,
                           alerts=alerts,
                           result=result)

if __name__ == '__main__':
    app.run(debug=True, port=5050)