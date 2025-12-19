import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Embedding, Dense
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import tensorflow as tf

# ----------------------------
# Load CSV and extract video IDs
# ----------------------------
df = pd.read_csv("tt.csv")  # columns: line_number,url
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
# Train with console progress
# ----------------------------
class ProgressCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        print(f"[Epoch {epoch+1}] loss={logs['loss']:.4f}, acc={logs['accuracy']:.4f}, val_loss={logs['val_loss']:.4f}, val_acc={logs['val_accuracy']:.4f}")

model.fit(X_train, y_train, validation_data=(X_test, y_test),
          epochs=20, batch_size=32, callbacks=[ProgressCallback()])

# ----------------------------
# Generate predicted URLs with multiple variants
# ----------------------------
N = 20        # number of seeds
variants = 3  # number of variants per seed
pred_len = 11 # full YouTube ID length
top_k = 3     # top-k for diversity
url_prefix = "https://www.youtube.com/watch?v="

with open("fin.txt", "w") as f:
    for i in range(N):
        seed_vid = np.random.choice(ids)
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