import re
import pandas as pd
from html import unescape

# ----------------------------
# Input/Output files
# ----------------------------
mht_file = "f.mht"
csv_file = "tt.csv"

# ----------------------------
# Read .mht file
# ----------------------------
with open(mht_file, "r", encoding="utf-8", errors="ignore") as f:
    raw_text = f.read()

# Unescape HTML entities
raw_text = unescape(raw_text)

# ----------------------------
# Extract YouTube video IDs
# ----------------------------
# Match /watch?v=VIDEOID (partial URLs in search pages)
video_ids_watch = re.findall(r"/watch\?v=([A-Za-z0-9_-]{11})", raw_text)

# Match shortened youtu.be URLs
video_ids_short = re.findall(r"youtu\.be/([A-Za-z0-9_-]{11})", raw_text)

# Combine and deduplicate
all_ids = video_ids_watch + video_ids_short
seen = set()
unique_ids = []
for vid in all_ids:
    if vid not in seen:
        unique_ids.append(vid)
        seen.add(vid)

print(f"[INFO] Extracted {len(unique_ids)} unique video IDs")

# ----------------------------
# Reconstruct full URLs
# ----------------------------
urls = [f"https://www.youtube.com/watch?v={vid}" for vid in unique_ids]

# ----------------------------
# Build dataframe
# ----------------------------
df = pd.DataFrame({
    "line_number": range(1, len(urls)+1),
    "url": urls
})

# ----------------------------
# Save to CSV
# ----------------------------
df.to_csv(csv_file, index=False)
print(f"[INFO] CSV saved as {csv_file}")