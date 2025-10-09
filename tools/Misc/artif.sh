#!/data/data/com.termux/files/usr/bin/bash
# Adds visual artifacts (noise + blur) to each page of combined.pdf

# Requirements: ghostscript, poppler-utils, imagemagick

INPUT="combined.pdf"
OUTPDF="combined_artifact.pdf"

# 1. Convert PDF pages to PNG images
echo "[1/3] Converting PDF to images..."
pdftoppm -png "$INPUT" page

# 2. Add artifacts to each image
echo "[2/3] Adding visual artifacts..."
for f in page-*.png; do
  convert "$f" \
    -attenuate 0.25 +noise Gaussian \
    -blur 0x1.2 \
    -contrast \
    -modulate 95,110,100 \
    "art-$f"
done

# 3. Reassemble images back to PDF
echo "[3/3] Reassembling artifact PDF..."
convert art-page-*.png "$OUTPDF"

# 4. (Optional) Compress final PDF
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen \
   -dNOPAUSE -dBATCH -sOutputFile=combined_artifact_small.pdf "$OUTPDF"

echo "✅ Done! Files created:"
echo " - $OUTPDF"
echo " - combined_artifact_small.pdf (compressed version)"
