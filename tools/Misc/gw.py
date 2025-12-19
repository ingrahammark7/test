import re
import pandas as pd
from html import unescape

# ----------------------------
# Input/Output files
# ----------------------------
mht_file = "raw.mht"   # your input .mht file
csv_file = "tt.csv"    # output CSV

# ----------------------------
# Read .mht file
# ----------------------------
with open(mht_file, "r", encoding="utf-8", errors="ignore") as f:
    raw_text = f.read()

# Unescape HTML entities (e.g., &amp;)
raw_text = unescape(raw_text)

# ----------------------------
# Extract YouTube URLs
# ----------------------------
# Match standard watch URLs
urls_watch = re.findall(r"https?://(?:www\.)?youtube\.com/watch\?v=[A-Za-z0-9_-]{11}", raw_text)

# Also match shortened youtu.be links
urls_short = re.findall(r"https?://youtu\.be/[A-Za-z0-9_-]{11}", raw_text)

# Combine and deduplicate while preserving order
all_urls = urls_watch + urls_short
seen = set()
urls = []
for url in all_urls:
    if url not in seen:
        urls.append(url)
        seen.add(url)

print(f"[INFO] Extracted {len(urls)} unique YouTube URLs")

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