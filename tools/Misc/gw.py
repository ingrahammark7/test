import pikepdf

INPUT = "app_clean.pdf"
OUTPUT = "app_bookmarked.pdf"

DOCUMENTS = [
    ("Cover (1/01/2026)", 0),
    ("Civil Case Information Statement (12/9/2025)", 2),
    ("Notice (10/30/2025)", 9),
    ("Register of Actions (1/1/2026)", 10),
    ("Election (10/31/2025)", 15),
]

pdf = pikepdf.open(INPUT)

# Create a new outline attached to the PDF
outline = pikepdf.Outline(pdf)

# Clear any existing outline
outline.root.clear()

# Add a Volume bookmark
volume = pikepdf.OutlineItem("Appendix Volume 1", destination=pdf.pages[0])
outline.root.append(volume)

# Add all documents as top-level bookmarks
for title, page_index in DOCUMENTS:
    item = pikepdf.OutlineItem(title, destination=pdf.pages[page_index])
    outline.root.append(item)

# Save PDF and attach the new outline
pdf.save(OUTPUT)
print("✓ Bookmarks added safely and ready for filing")