import pikepdf

INPUT = "n.pdf"          # Your source PDF
OUTPUT = "app_bookmarked.pdf"

# List of documents: (Title, first page)
DOCUMENTS = [
    ("Cover (1/01/2026)", 0),
    ("Civil Case Information Statement (12/9/2025)", 2),
    ("Notice (10/30/2025)", 9),
    ("Register of Actions (1/1/2026)", 10),
    ("Election (10/31/2025)", 15),
]

pdf = pikepdf.open(INPUT)

with pdf.open_outline() as outline:
    vol = outline.root.add_child("Appendix Volume 1", page=0)
    for title, page in DOCUMENTS:
        vol.add_child(title, page=page)

pdf.save(OUTPUT)
print("✓ 2nd DCA civil appendix bookmarks added")