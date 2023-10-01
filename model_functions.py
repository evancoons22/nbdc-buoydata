import torch
import pandas as pd
import sqlite3
import numpy as np
import functions

import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from matplotlib import pyplot as plt
from datetime import datetime

class WaveForecastingRNN(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(WaveForecastingRNN, self).__init__()
        # self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True) # recurrent neural network
        self.rnn = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True) # long short term memory model
        self.fc = nn.Linear(hidden_size, output_size) # fully connected layer
        # self.fc = nn.Linear(hidden_size, output_size) # fully connected layer


    def forward(self, x):
        out, _ = self.rnn(x)
        out = self.fc(out[:, -1, :])  # Use the last time step's output for prediction
        return out


def querySqliteData():
    conn = sqlite3.connect('db.db')
    data = pd.read_sql_query("SELECT * from main", conn)
    data = functions.cleanData(data)

    target = functions.buildnparray(data[data["buoy_id"] == "46221"])
    data = functions.buildnparray(data[data["buoy_id"] != "46221"])
    data = data[1:]

    return (data, target)


def intoTensor(data):
    data_tensor = torch.Tensor(data) # convert to pytorch tensor

    data_tensor = torch.reshape(data_tensor, (data.shape[0], -1))
    nan_mask = torch.isnan(data_tensor)
    data_tensor[nan_mask] = 0
    return data_tensor


def buildTrainTensor(data_tensor, target_tensor, batch_size):
    input_sequences = []
    target_values = []

    for i in range(len(data_tensor) - sequence_length - 24):
        input_seq = data_tensor[i:i+sequence_length]
        target_val = target_tensor[i + sequence_length + 24]
        # input_seq = data_tensor[i:i+sequence_length]  
        # target_val = data_tensor[i+sequence_length] 
        input_sequences.append(input_seq)
        target_values.append(target_val)
    # print("input sequences", input_sequences.shape)

    input_sequences = torch.stack(input_sequences)
    target_values = torch.stack(target_values)

    dataset = TensorDataset(input_sequences, target_values)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    return (dataset, dataloader)



def trainModel(dataloader, num_features, hidden_size, num_layers, output_size, num_epochs):
    # num_features = 225
    # input_size = num_features
    # hidden_size = 64
    # num_layers = 1 
    # output_size = 3

    loss_errors = []

    model = WaveForecastingRNN(input_size, hidden_size, num_layers, output_size)

    # Define the loss function and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    start = datetime.now() # timing

    # Training loop
    print(f'beginning training')
    for epoch in range(num_epochs):
        for inputs, targets in dataloader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss_errors.append(loss.item())
            loss.backward()
            optimizer.step()
        if epoch % 10 == 0:
            print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')
    end = datetime.now() # timing end

    print(f"training finished in {end - start}, saving model")
    torch.save(model.state_dict(), 'model_weights.pth')


def testModel(model, data_test, target_test):
    datasettest, dataloadertest = buildTensor(data_test, target_test, batch_size = 1)
    test_loss = 0.0
    for inputs, targets in dataloadertest:
        # Forward pass
        outputs = model(inputs)
        # print("outputs: ", outputs, "\n", "targets: ", targets, "\n")
        
        # Compute loss
        loss = criterion(outputs, targets)
        # print("loss:  ", loss)
        test_loss += loss.item()  # Accumulate the test loss

    # Calculate and print average test loss
    avg_test_loss = test_loss / len(dataloadertest)
    print(f'Average Test Loss: {avg_test_loss:.4f}')
