import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Embedding, Dense
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import tensorflow as tf
import os

# ----------------------------
# Load CSV and extract video IDs
# ----------------------------
df = pd.read_csv("tt.csv")  # columns: line_number,url
df['id'] = df['url'].str.extract(r"v=([A-Za-z0-9_-]{11})")
df = df.dropna(subset=['id'])
ids = df['id'].tolist()
print(f"[INFO] Extracted {len(ids)} valid video IDs")

# ----------------------------
# Parameters
# ----------------------------
window_size = 200       # sliding window size
seq_length = 10         # predict next character
embedding_dim = 32
lstm_units = 128
epochs_per_update = 5
batch_size = 32
top_k = 3
variants = 3
pred_len = 11
url_prefix = "https://www.youtube.com/watch?v="

# ----------------------------
# Build character mapping
# ----------------------------
vocab = sorted(list(set(''.join(ids))))
char_to_idx = {c: i for i, c in enumerate(vocab)}
idx_to_char = {i: c for c, i in char_to_idx.items()}
vocab_size = len(vocab)
print(f"[INFO] Vocabulary size: {vocab_size}")

# ----------------------------
# Build model
# ----------------------------
model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=embedding_dim),
    LSTM(lstm_units, return_sequences=False),
    Dense(vocab_size, activation='softmax')
])
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# ----------------------------
# Sliding window training function
# ----------------------------
def train_on_window(ids_window):
    X_data = []
    y_data = []
    for vid in ids_window:
        for i in range(len(vid) - seq_length):
            seq_in = vid[i:i + seq_length]
            seq_out = vid[i + seq_length]
            X_data.append([char_to_idx[c] for c in seq_in])
            y_data.append(char_to_idx[seq_out])
    if len(X_data) == 0:
        return  # skip empty window

    X_data = np.array(X_data)
    y_data = to_categorical(y_data, num_classes=vocab_size)
    X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2, random_state=42)

    model.fit(X_train, y_train, validation_data=(X_test, y_test),
              epochs=epochs_per_update, batch_size=batch_size, verbose=1)

# ----------------------------
# Sliding window training
# ----------------------------
for start_idx in range(0, len(ids), window_size):
    end_idx = min(start_idx + window_size, len(ids))
    ids_window = ids[start_idx:end_idx]
    print(f"[INFO] Training on window {start_idx}-{end_idx}")
    train_on_window(ids_window)

# ----------------------------
# Generate predicted URLs
# ----------------------------
N = 20  # number of seeds
weights = np.linspace(1, 2, len(ids))
weights /= weights.sum()  # recency weighting

with open("fin.txt", "w") as f:
    for i in range(N):
        seed_vid = np.random.choice(ids, p=weights)
        seed_pattern = [char_to_idx[c] for c in seed_vid[:seq_length]]

        for v in range(variants):
            pattern = seed_pattern.copy()
            result = seed_vid[:seq_length]

            for _ in range(pred_len - seq_length):
                x = np.array([pattern])
                pred = model.predict(x, verbose=0)[0]
                top_indices = pred.argsort()[-top_k:][::-1]
                next_idx = np.random.choice(top_indices)
                next_char = idx_to_char[next_idx]
                result += next_char
                pattern = pattern[1:] + [next_idx]

            f.write(url_prefix + result + "\n")

print(f"[INFO] {N*variants} predicted YouTube URLs written to fin.txt")