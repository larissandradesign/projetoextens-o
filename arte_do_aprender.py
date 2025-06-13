import pandas as pd
import streamlit as st
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# --- Dados simulados para treinar o modelo ---
data = {
    "Matemática": [450, 600, 300, 700, 400, 650, 480, 520],
    "Linguagens": [550, 400, 350, 600, 300, 700, 500, 450],
    "Ciências Humanas": [400, 620, 310, 680, 420, 630, 470, 510],
    "Ciências da Natureza": [430, 610, 290, 670, 410, 640, 460, 520],
    "Redação": [480, 590, 300, 690, 420, 600, 490, 530],
    "Dificuldade": [1, 0, 1, 0, 1, 0, 1, 0]
}

df = pd.DataFrame(data)
X = df.drop("Dificuldade", axis=1)
y = df["Dificuldade"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = DecisionTreeClassif
