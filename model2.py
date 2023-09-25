import torch
import pandas as pd
import sqlite3
import numpy as np
import functions

import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# -------- get and organize data------------------------------------------------------------

conn = sqlite3.connect('db.db')
data = pd.read_sql_query("SELECT * from main", conn)
# data = functions.cleanData(data)

# use_date = data[data['buoy_id'] == '46221'].iloc[0]['datetime']

# all_buoys = data[data['buoy_id'] != '46221']
# output_buoy = data[data['buoy_id'] == '46221']

data = functions.buildnparray(functions.cleanData(data))

# ---- train -------------------------------------------------------------

sequence_length = 24 * 10  # length of sequence, 24 hours * 10 days
batch_size = 32      # Batch size for training
num_epochs = 50      # Number of training epochs

data_tensor = torch.Tensor(data) # convert to pytorch tensor
print("data tensor", data_tensor.shape)

# Create input sequences and corresponding target values
input_sequences = []
target_values = []

for i in range(len(data) - sequence_length):
    input_seq = data_tensor[i:i+sequence_length]  
    target_val = data_tensor[i+sequence_length] 
    input_sequences.append(input_seq)
    target_values.append(target_val)

input_sequences = torch.stack(input_sequences)
target_values = torch.stack(target_values)
print("input sequences", input_sequences.shape)

# Create a DataLoader for batching
# dataloader allows efficient use of memory
dataset = TensorDataset(input_sequences, target_values)
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

class WaveForecastingRNN(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(WaveForecastingRNN, self).__init__()
        # self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True) # recurrent neural network
        self.rnn = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True) # long short term memory model
        self.fc = nn.Linear(hidden_size, output_size) # fully connected layer

    def forward(self, x):
        out, _ = self.rnn(x)
        out = self.fc(out[:, -1, :])  # Use the last time step's output for prediction
        return out

# Initialize the model
num_features = 3
input_size = num_features
hidden_size = 64
num_layers = 1 
output_size = num_features

model = WaveForecastingRNN(input_size, hidden_size, num_layers, output_size)

# Define the loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
for epoch in range(num_epochs):
    for inputs, targets in dataloader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
    print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')
