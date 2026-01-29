import numpy as np
import pandas as pd

# Example data (replace with your real measurements)
data = pd.DataFrame({
    'CPU': np.random.normal(0, 0.5, 100),
    'MEM': np.random.normal(62.7, 0.5, 100),
    'PROC': np.random.normal(5, 0.2, 100)
})

window_sizes = [5, 10, 20, 40]
anomaly_threshold = 2.0  # std deviations

# Global stats
global_mean = data.mean()
global_std = data.std().replace(0, 1e-6)

for size in window_sizes:
    total_windows = len(data) - size + 1
    for i in range(total_windows):
        window = data.iloc[i:i+size]
        w_mean = window.mean()
        w_min = window.min()
        w_max = window.max()

        # Realistic "Accuracy" metric: proportion of features within 1 std of global mean
        deviations = np.abs(window - global_mean) <= global_std
        accuracy = deviations.mean().mean()

        # Confidence: average z-score across features
        z_scores = np.abs((window - global_mean) / global_std)
        confidence = z_scores.mean().mean()

        # Flag if window is anomalous
        flag = "⚠️ EDGE" if confidence > anomaly_threshold else ""

        print(f"[Window {i+1}/{total_windows}, Size={size}] Accuracy={accuracy:.4f} Confidence={confidence:.3f} {flag}")
        print(f" Feature means: CPU={w_mean['CPU']:.2f}, MEM={w_mean['MEM']:.2f}, PROC={w_mean['PROC']:.1f}")
        print(f" Feature min  : CPU={w_min['CPU']:.2f}, MEM={w_min['MEM']:.2f}, PROC={w_min['PROC']:.1f}")
        print(f" Feature max  : CPU={w_max['CPU']:.2f}, MEM={w_max['MEM']:.2f}, PROC={w_max['PROC']:.1f}")