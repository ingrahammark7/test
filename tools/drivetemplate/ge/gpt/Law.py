from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Frame

def create_pdf(output_filename):
    # Create a PDF document
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter

    # Set margins
    left_margin = 1 * inch
    right_margin = width - 1 * inch
    top_margin = height - 1 * inch
    bottom_margin = 1 * inch

    # Set font and size (Times New Roman, 12-point)
    c.setFont("Times-Roman", 12)

    # Add page numbers (starting from page 2)
    def add_page_number(page_num):
        if page_num > 1:  # Suppress page number on the first page
            c.setFont("Times-Roman", 10)
            c.drawCentredString(width / 2, 0.5 * inch, f"{page_num}")

    # Add footer
    def add_footer(page_num):
        footer_y = 0.4 * inch  # Position for footer
        footer_text = "Writ of Mandate Petition"  # Title of the paper
        c.setFont("Times-Roman", 10)  # Font size for footer
        c.drawCentredString(width / 2, footer_y, footer_text)
        # Draw a line above the footer
        c.line(left_margin, footer_y + 0.1 * inch, right_margin, footer_y + 0.1 * inch)

    # Add line numbers
    def add_line_numbers(start_y, end_y, line_height):
        line_number_x = left_margin - 0.5 * inch  # Position for line numbers
        line_number = 1
        current_y = start_y
        while current_y >= end_y:
            c.drawString(line_number_x, current_y, str(line_number))
            line_number += 1
            current_y -= line_height

    # First Page Format (Rule 2.111)
    # (1) Attorney Information
    c.setFont("Times-Roman", 12)
    attorney_info = [
        "Attorney Name: [Name]",
        "Office Address: [Address]",
        "Telephone: [Phone]",
        "Fax: [Fax]",
        "Email: [Email]",
        "State Bar Number: [Number]"
    ]
    y_position = top_margin - 0.5 * inch
    for line in attorney_info:
        c.drawString(left_margin, y_position, line)
        y_position -= 0.25 * inch

    # (2) Clerk's Space (blank space to the right of center)
    c.rect(width / 2 + 0.5 * inch, top_margin - 2 * inch, 2 * inch, 1.5 * inch, stroke=1, fill=0)

    # (3) Court Title
    c.setFont("Times-Bold", 14)
    c.drawCentredString(width / 2, top_margin - 3.33 * inch, "SUPERIOR COURT OF CALIFORNIA")
    c.drawCentredString(width / 2, top_margin - 3.66 * inch, "COUNTY OF [COUNTY NAME]")

    # (4) Case Title
    c.setFont("Times-Bold", 12)
    c.drawString(left_margin, top_margin - 4 * inch, "Case Title:")
    c.setFont("Times-Roman", 12)
    case_title = [
        "Petitioner: [Petitioner Name]",
        "Respondent: [Respondent Name]"
    ]
    y_position = top_margin - 4.5 * inch
    for line in case_title:
        c.drawString(left_margin, y_position, line)
        y_position -= 0.25 * inch

    # (5) Case Number
    c.setFont("Times-Roman", 12)
    c.drawString(width / 2 + 1 * inch, top_margin - 4 * inch, "Case Number: [Number]")

    # (6) Nature of the Paper
    c.setFont("Times-Bold", 12)
    c.drawString(left_margin, top_margin - 5 * inch, "Nature of the Paper:")
    c.setFont("Times-Roman", 12)
    c.drawString(left_margin, top_margin - 5.25 * inch, "Writ of Mandate Petition")

    # (7) Judge and Department
    c.setFont("Times-Roman", 12)
    c.drawString(left_margin, top_margin - 5.75 * inch, "Judge: [Judge Name]")
    c.drawString(left_margin, top_margin - 6 * inch, "Department: [Department Number]")

    # Add line numbers
    line_height = 0.2 * inch  # Approximately 3 line numbers per vertical inch
    add_line_numbers(top_margin - 7 * inch, bottom_margin + 0.5 * inch, line_height)

    # Add footer (suppressed on the first page)
    add_footer(1)

    # Save the first page
    c.showPage()

    # Add a second page with page number and footer
    add_page_number(2)
    add_footer(2)
    c.drawString(left_margin, top_margin - 1 * inch, "Continued...")

    # Save the PDF
    c.save()

if __name__ == "__main__":
    output_filename = "writ_of_mandate_petition.pdf"
    create_pdf(output_filename)
    print(f"PDF created: {output_filename}")
