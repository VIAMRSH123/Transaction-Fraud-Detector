import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest, RandomForestClassifier

sns.set_style("darkgrid")
plt.style.use("ggplot")

data = pd.read_csv("transactions.csv")

# ------------------ VISUAL CHART 1 ------------------
sizes = data['Class'].value_counts()
plt.figure(figsize=(6,6))
plt.pie(sizes, labels=['Legitimate','Fraud'],
        colors=['#2ecc71','#e74c3c'],
        autopct='%1.1f%%')
plt.title("Transaction Class Distribution")
plt.savefig("static/chart1.png")
plt.close()

# ------------------ VISUAL CHART 2 ------------------
plt.figure(figsize=(8,4))
plt.hist(data['Amount'], bins=15, color='#9b59b6', edgecolor='black')
plt.title("Transaction Amount Distribution")
plt.xlabel("Amount")
plt.ylabel("Frequency")
plt.savefig("static/chart2.png")
plt.close()

# ------------------ VISUAL CHART 3 ------------------
plt.figure(figsize=(10,6))
sns.heatmap(data.corr(), cmap='magma')
plt.title("Correlation Heatmap")
plt.savefig("static/chart3.png")
plt.close()

# ------------------ MODEL TRAINING ------------------
X = data.drop("Class", axis=1)
y = data["Class"]

scaler = StandardScaler()
X[['Time','Amount']] = scaler.fit_transform(X[['Time','Amount']])

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)

iso_model = IsolationForest(contamination=0.15, random_state=42)
iso_model.fit(X_train)

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

joblib.dump(rf_model, "fraud_model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("Charts generated and ML models saved successfully.")