from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject
from reportlab.pdfgen import canvas

# Step 1: Create a base PDF with dummy pages
# In practice, you would replace this with your actual PDF
base_pdf_path = "not.pdf"
c = canvas.Canvas(base_pdf_path)
for i in range(1, 8):  # 7 pages
    c.drawString(100, 750, f"Page {i}")
    c.showPage()
c.save()

# Step 2: Open the PDF and create a writer
reader = PdfReader(base_pdf_path)
writer = PdfWriter()

# Copy all pages
for page in reader.pages:
    writer.add_page(page)

# Step 3: Add court-compliant bookmarks
bookmarks = [
    ("Petition", 0),      # page 1
    ("Certificate", 2),   # page 3
    ("Verification", 3),  # page 4
    ("Compliance", 4),    # page 5
    ("Parties", 5),       # page 6
    ("Memorandum", 6),    # page 7
]

for title, page_index in bookmarks:
    writer.add_outline_item(title, page_index)

# Step 4: Ensure PageMode is set to show outlines
writer._root_object[NameObject("/PageMode")] = NameObject("/UseOutlines")

# Step 5: Save the new PDF
output_path = "not_court_ready.pdf"
with open(output_path, "wb") as f:
    writer.write(f)

print(f"Court-compliant bookmarked PDF saved as {output_path}")