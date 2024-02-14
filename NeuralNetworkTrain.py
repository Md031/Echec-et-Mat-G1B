import torch
import torch.nn as nn
# import torch.nn.functional as F

# from chessNet import ChessNet
# from chessDataSet import ChessDataset
# from torch.utils.data import DataLoader

torch.manual_seed(41)
#model = ChessNet()


# import pandas as pd
# import matplotlib.pyplot as plt
# import gc

# import data from data set

# chess_data_raw = pd.read_csv('chess_games.csv', usecols = ['AN','WhiteElo'])
# chess_data = chess_data_raw[chess_data_raw['WhiteElo'] > 2000]


# del chess_data_raw
# gc.collect()

# chess_data = chess_data[['AN']]
# chess_data = chess_data[~chess_data['AN'].str.contains('{')]
# chess_data = chess_data[chess_data['AN'].str.len()>20]

# print("Shape chess_date =", chess_data.shape()) # Ce print vérifie combien de games contient l'array chess_data

# data_train = ChessDataset(chess_data['AN'])
# data_train_loader = DataLoader(data_train, batch_size=32, shuffle=True, drop_last=True) # Shuffle not necessary because games are selected randomly

#from sklearn.model_selection import train_test_split

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=41)

# Train

from chessNet import model

metric_from = nn.CrossEntropyLoss()
metric_to = nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(model.parameters(), lr=0.01) # Pas sur de cette ligne 


# Train our model!
# Epochs? (one run thru all the training data in our network)
epochs = 10000
losses = []
epoch_count = 0

from chessDataSet import data_train_loader
from NeuralNetwork import board_2_rep

for X_input, y in data_train_loader: # X_input = 32 dispositions de board
    if epoch_count >= epochs: 
        break
    
    #X_input, y = X_input.cuda(), y.cuda() # Sends the Data to the GPU

    batch_size = X_input.size(0)
    #print(batch_size)
    batch_output = []
    for i in range(batch_size):
        single_board = X_input[i]  # Extract one board disposition at a time

        #single_board = torch.Tensor(single_board).float().to('cuda') # Uses GPU
        single_board = torch.Tensor(single_board).float() # Uses CPU

        #print("Singleboard: ", single_board, type(single_board))

        single_board = single_board.unsqueeze(0) # Turns single_board from 3D to 4D
        output = model.forward(single_board) # Get predicted results
        # print("output: ", output)
        # print("type output: ", type(output))
        batch_output.append(output)

    batch_output = torch.cat(batch_output, dim=0)

    loss_from = metric_from(batch_output[:,0,:], y[:,0,:])
    loss_to = metric_to(batch_output[:,1,:], y[:,1,:])
    loss = loss_from + loss_to

    # Keep Track of our losses
    losses.append(loss.detach().numpy())

    # print every 10 epoch
    if epoch_count % 10 == 0:
        print(f'Epoch: {epoch_count} and loss: {loss}')

    # Do some back propagation: take the error rate of forward propagation and feed it back
    # thru the network to fine tune the weights
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    epoch_count += 1