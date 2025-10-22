import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import os

# --- Parameters ---
N = 60          # number of bytes
lag = 20          # sliding window length
batch_size = 64
epochs = 20
hidden_size = 128
lr = 0.001

# --- Load data ---
data = np.frombuffer(os.getrandom(N), dtype=np.uint8) / 255.0  # normalize to [0,1]

# --- Prepare sliding window dataset ---
def prepare_lstm_data(data, lag):
    X = np.array([data[i:i+lag] for i in range(len(data)-lag)])
    y = np.array([data[i+lag] for i in range(len(data)-lag)])
    return torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.float32)

X, y = prepare_lstm_data(data, lag)
dataset = TensorDataset(X, y)
split = int(0.8 * len(dataset))
train_dataset, test_dataset = torch.utils.data.random_split(dataset, [split, len(dataset)-split])

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size)

# --- Define LSTM Model ---
class LSTMRegressor(nn.Module):
    def __init__(self, input_size, hidden_size):
        super().__init__()
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)
    
    def forward(self, x):
        out, _ = self.lstm(x)
        out = out[:, -1, :]      # take output at last timestep
        out = self.fc(out)
        return out.squeeze()

model = LSTMRegressor(input_size=1, hidden_size=hidden_size)

# --- Optimizer and loss ---
optimizer = torch.optim.Adam(model.parameters(), lr=lr)
criterion = nn.MSELoss()

# --- Training loop ---
for epoch in range(epochs):
    model.train()
    total_loss = 0
    for batch_X, batch_y in train_loader:
        batch_X = batch_X.unsqueeze(-1)  # shape: [batch, lag, 1]
        optimizer.zero_grad()
        pred = model(batch_X)
        loss = criterion(pred, batch_y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * batch_X.size(0)
    print(f"Epoch {epoch+1}/{epochs}, Train MSE: {total_loss/len(train_loader.dataset):.6f}")

# --- Evaluation ---
model.eval()
mse_total = 0
with torch.no_grad():
    for batch_X, batch_y in test_loader:
        batch_X = batch_X.unsqueeze(-1)
        pred = model(batch_X)
        mse_total += criterion(pred, batch_y).item() * batch_X.size(0)
mse_test = mse_total / len(test_loader.dataset)
print("Test MSE:", mse_test)