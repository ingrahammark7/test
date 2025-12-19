import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense, Embedding, TimeDistributed, Bidirectional, Concatenate, Flatten
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# ----------------------------
# Load CSV
# ----------------------------
df = pd.read_csv("tt.csv")  # columns: line_number,url
# Extract video IDs (11 chars)
df['id'] = df['url'].str.extract(r"v=([A-Za-z0-9_-]{11})")
df = df.dropna(subset=['id'])
ids = df['id'].tolist()
print(f"[INFO] Extracted {len(ids)} valid video IDs")

# Optional: infer eras from row index (approximate time)
df['era'] = (df.index // 100).astype(int)  # adjust bin size
num_eras = df['era'].nunique()
eras = df['era'].tolist()

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
seq_length = 10  # sequence length
X_chars, X_eras, y_data = [], [], []

for vid, era in zip(ids, eras):
    for i in range(len(vid) - seq_length):
        seq_in = vid[i:i + seq_length]
        seq_out = vid[i + seq_length]
        X_chars.append([char_to_idx[c] for c in seq_in])
        X_eras.append(era)
        y_data.append(char_to_idx[seq_out])

X_chars = np.array(X_chars)
X_eras = np.array(X_eras)
y_data = to_categorical(y_data, num_classes=vocab_size)

# Train/test split
Xc_train, Xc_test, Xe_train, Xe_test, y_train, y_test = train_test_split(
    X_chars, X_eras, y_data, test_size=0.2, random_state=42
)

# ----------------------------
# Build model
# ----------------------------
# Character input
char_input = Input(shape=(seq_length,), name='char_input')
x = Embedding(input_dim=vocab_size, output_dim=64)(char_input)

# Bidirectional LSTM layers with dropout
x = Bidirectional(LSTM(128, return_sequences=True, dropout=0.2, recurrent_dropout=0.2))(x)
x = Bidirectional(LSTM(128, dropout=0.2, recurrent_dropout=0.2))(x)

# Era input + embedding
era_input = Input(shape=(1,), name='era_input')
era_emb = Embedding(input_dim=num_eras, output_dim=8)(era_input)
era_emb = Flatten()(era_emb)

# Concatenate
x = Concatenate()([x, era_emb])

# Output layer
output = Dense(vocab_size, activation='softmax')(x)

model = Model(inputs=[char_input, era_input], outputs=output)
model.compile(loss='categorical_crossentropy', optimizer=tf.keras.optimizers.Adam(1e-3), metrics=['accuracy'])
model.summary()

# ----------------------------
# Training callback
# ----------------------------
class ProgressCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        print(f"[Epoch {epoch+1}] loss={logs['loss']:.4f}, acc={logs['accuracy']:.4f}, "
              f"val_loss={logs['val_loss']:.4f}, val_acc={logs['val_accuracy']:.4f}")

# Early stopping
early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# ----------------------------
# Train
# ----------------------------
model.fit(
    {'char_input': Xc_train, 'era_input': Xe_train},
    y_train,
    validation_data=({'char_input': Xc_test, 'era_input': Xe_test}, y_test),
    epochs=50,
    batch_size=32,
    callbacks=[ProgressCallback(), early_stop]
)