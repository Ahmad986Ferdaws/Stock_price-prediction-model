# so first we are going to import the necesary librtaries to make sure you have all the libraries please check the terminal on macos or command promt,powershell on windows
# first we import the numpy 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# this part of the code we import a function thats classified in pandas library 
# as pandas data reader that will help us to read the data thar are necessary for 
# stock prediction 
import pandas_datareader as web
# and over here we are importing the date time as pd since we will have the option to ask predictions from certian date time
import datetime as dt

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tenserflow.keras.layers import Dense, Dropout, LSTM

# Loading the data
#over here for loading the data and also the company names for example like the amazon and the FB
company = 'FB'
company = 'Amazon'
#and also over here we define the start date and also end date
start = dt.datetime(2012,1,1)
end = dt.datetime(2020,1,1)
# in this part the we read the data from yahoo
data = web.DataReader(company,'yahoo',start,end)

# Prepare Data

scaler  = MinMaxScaler(feature_range=(0,1))

scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1,1))

prediction_days = 90

x_train = []
y_train = []

for x in range(prediction_days, len(scaled_data)):
    x_train.append(scaled_data[x-prediction_days:x,0])
    y_train.append(scaled_data[x,0])

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train,(x_train.shape[0],x_train.shape[1],1))

# Build The model

model = Sequential()
model.add(LSTM(units=40,return_sequences = True, input_shape =(x_train.shape[1],1)))
model.add(Dropout(0.2))
model.add(LSTM(units=40,return_sequences = True))
model.add(Dropout(0.2))
model.add(LSTM(units=40,return_sequences = True))
model.add(Dropout(0.2))
model.add(Dense(units =1)) # prediction of the next price


model,compile(optimize='adam', loss='mean_squared_errors')
model.fit(x_train,y_train, epochs= 25, batch_size= 32)

''' Test the model accuracy on existing data'''

# Load 
test_start = dt.datetime(2024,1,1)
test_end = dt.datetime.now()

test_data = web.DataReader(company,'yahoo',test_start,test_end)
atcual_prices = test_data['Close'].values

total_dataset = pd.concat((data['Close'],test_data['Close']), axis=0)

model_inputs = total_dataset[len(total_dataset) - len(test_data) - prediction_days:].values
model_inputs = model_inputs.reshape(-1,1)
model_inputs = scaler.transform(model_inputs)


# Make predictions on test data

x_test =[0]

for x in range(prediction_days,len(model_inputs)):
    x_test.append(model_inputs[x-prediction_days:x,0])

x_test = np.array(x_test)
x_test = np.reshape(x_test,(x_test.shape[0], x_test.shape[1],1))

predicted_prices = model.predict(x_test)
predicted_prices = scaler.inverse_transform(predicted_prices)

# Plot the test predictions 
plt.plot(atcual_prices, color = "Blue", label = f"actual{company}price")
plt.plot(predicted_prices, color = 'red', label = f"Prediction{company}Price" )

plt.title(f'{company}Share Price')
plt.xlabel('Time')
plt.ylabel(f'{company} Share Price')
plt.legend()
plt.show()

