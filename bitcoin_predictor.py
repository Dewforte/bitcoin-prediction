# -*- coding: utf-8 -*-

import requests
import pandas as pd
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.models import Sequential

api_key = "e021ee2e32bf487dadde337e5e8328ed"
symbol = "BTC/USD"
interval = "5min"  # Kept the original interval for fetching data
order = "asc"
start_date = "2024-01-01 00:00:00"
end_date = "2024-07-01 00:00:00"
api_url = f"https://api.twelvedata.com/time_series?symbol={symbol}&start_date={start_date}&end_date={end_date}&interval={interval}&order={order}&apikey={api_key}"

data = requests.get(api_url).json()
data

data.keys()

data_final = pd.DataFrame(data["values"])
data_final

data.keys()

data_final["close"].values.reshape(-1, 1).shape

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data_final["close"].values.reshape(-1, 1))

scaled_data.shape

time_interval_train = 24
prediction_interval = 2  # Changed from 12 (for 1 hour) to 2 (for 10 minutes)

x_train = []
y_train = []

for i in range(time_interval_train, len(scaled_data) - prediction_interval):
    x_train.append(scaled_data[i - time_interval_train: i, 0])
    y_train.append(scaled_data[i + prediction_interval, 0])

x_train = np.array(x_train)
y_train = np.array(y_train)

x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
x_train.shape

model = Sequential()

model.add(LSTM(128, return_sequences=True, input_shape=(x_train.shape[1], 1), activation="relu"))
model.add(Dropout(0.4))
model.add(LSTM(64, return_sequences=True, activation="relu"))
model.add(Dropout(0.3))
model.add(LSTM(32, activation="relu"))
model.add(Dropout(0.2))
model.add(Dense(1, activation="sigmoid"))

model.compile(loss="mean_squared_error", optimizer="adam", metrics=["accuracy"])

model.fit(x_train, y_train, epochs=10, batch_size=64)

test_start = "2024-1-1"
test_end = "2024-7-31"
test_api_url = f"https://api.twelvedata.com/time_series?symbol={symbol}&start_date={test_start}&end_date={test_end}&interval={interval}&order={order}&apikey={api_key}"
test_data = requests.get(test_api_url).json()
test_data_final = pd.DataFrame(test_data["values"])
test_data_final

bitcoin_prices = pd.to_numeric(test_data_final["close"], errors="coerce").values
test_inputs = test_data_final["close"].values
test_inputs = test_inputs.reshape(-1, 1)
model_inputs = scaler.fit_transform(test_inputs)

model_inputs

model_inputs.shape

x_test = []

for x in range(time_interval_train, len(model_inputs)):
    x_test.append(model_inputs[x - time_interval_train:x, 0])
x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

x_test.shape

prediction_prices = model.predict(x_test)
prediction_prices = scaler.inverse_transform(prediction_prices)

prediction_prices

last_data = model_inputs[len(model_inputs) + 1 - time_interval_train: len(model_inputs) + 1, 0]
last_data = np.array(last_data)

last_data.shape

last_data = np.reshape(last_data, (1, last_data.shape[0], 1))

prediction = model.predict(last_data)

prediction

prediction = scaler.inverse_transform(prediction)
prediction

