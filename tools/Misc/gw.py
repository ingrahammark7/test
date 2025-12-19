import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Embedding, TimeDistributed, Dense
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# ----------------------------
# Load CSV
# ----------------------------
df = pd.read_csv("tt.csv")  # columns: line_number,url

# Extract video IDs from URLs
df['id'] = df['url'].str.extract(r"v=([A-Za-z0-9_-]{11})")
df = df.dropna(subset=['id'])
ids = df['id'].tolist()
print(f"[INFO] Extracted {len(ids)} valid video IDs")

# ----------------------------
# Build character mapping
# ----------------------------
vocab = sorted(list(set(''.join(ids))))
char_to_idx = {c: i for i, c in enumerate(vocab)}
idx_to_char = {i: c for c, i in char_to_idx.items()}
vocab_size = len(vocab)
print(f"[INFO] Vocabulary size: {vocab_size}")

# ----------------------------
# Prepare sequences
# ----------------------------
seq_length = 10  # predict next character
X_data = []
y_data = []

for vid in ids:
    for i in range(len(vid) - seq_length):
        seq_in = vid[i:i + seq_length]
        seq_out = vid[i + seq_length]
        X_data.append([char_to_idx[c] for c in seq_in])
        y_data.append(char_to_idx[seq_out])

X_data = np.array(X_data)
y_data = to_categorical(y_data, num_classes=vocab_size)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2, random_state=42)

# ----------------------------
# Build model
# ----------------------------
model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=32),
    LSTM(128, return_sequences=False),
    Dense(vocab_size, activation='softmax')
])
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

# ----------------------------
# Train with progress info
# ----------------------------
class ProgressCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        print(f"[Epoch {epoch+1}] loss={logs['loss']:.4f}, acc={logs['accuracy']:.4f}, val_loss={logs['val_loss']:.4f}, val_acc={logs['val_accuracy']:.4f}")

model.fit(X_train, y_train, validation_data=(X_test, y_test),
          epochs=20, batch_size=32, callbacks=[ProgressCallback()])