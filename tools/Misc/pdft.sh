#!/data/data/com.termux/files/usr/bin/bash

# Ensure input.pdf exists
INPUT="input.pdf"
OUTPUT_PREFIX="page"

if [ ! -f "$INPUT" ]; then
    echo "Error: $INPUT not found in $(pwd)"
    exit 1
fi

# Convert all pages to PNG at 150 DPI
pdftoppm -png -r 150 "$INPUT" "$OUTPUT_PREFIX"

echo "Conversion complete. Pages saved as ${OUTPUT_PREFIX}-1.png, ${OUTPUT_PREFIX}-2.png, ..."

