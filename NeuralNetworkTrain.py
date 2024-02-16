import torch
import torch.nn as nn

torch.manual_seed(41)

# Train
from chessNet import ChessNet

model = ChessNet()
model.load_state_dict(torch.load('ChessModel.pt'))

model.eval()

metric_from = nn.CrossEntropyLoss()
metric_to = nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(model.parameters(), lr=0.001) # Learning rate can be modified here

# Checks if the a GPU is available
if torch.cuda.is_available():
    print("Cuda is available")
    device = "cuda"
else:
    print("Cuda is unavailable")
    device = "cpu"

model = model.to(device) # Moves model to the GPU, if available

epochs = 1000
losses = []

from chessDataSet import data_train_loader


for epoch_count, (X_input, y) in enumerate(data_train_loader): # X_input = 32 dispositions de board
    if epoch_count >= epochs: 
        break
    
    X_input, y = X_input.to(device), y.to(device) # Sends the Data to the GPU

    batch_size = X_input.size(0)
    batch_output = []
    for i in range(batch_size):
        single_board = X_input[i]  # Extract one board disposition at a time

        single_board = torch.Tensor(single_board).float().to(device) # Uses GPU
        #single_board = torch.Tensor(single_board).float() # Uses CPU

        single_board = single_board.unsqueeze(0) # Turns single_board from 3D to 4D
        output = model.forward(single_board) # Get predicted results

        batch_output.append(output)

    batch_output = torch.cat(batch_output, dim=0)

    loss_from = metric_from(batch_output[:,0,:], y[:,0,:])
    loss_to = metric_to(batch_output[:,1,:], y[:,1,:])
    loss = loss_from + loss_to

    # Keep Track of our losses
    losses.append(loss.detach().cpu().numpy()) # Sends data to the cpu so that it can be turned to a numpy array

    # print every 10 epoch
    if epoch_count % 10 == 0:
        print(f'Epoch: {epoch_count} and loss: {loss}')

    # Do some back propagation: take the error rate of forward propagation and feed it back
    # thru the network to fine tune the weights
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    torch.save(model.state_dict(), 'ChessModel.pt') # Saves the model at each epoch