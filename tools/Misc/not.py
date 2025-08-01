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
    bottom_margin = 0 * inch

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
        footer_text = "Request for Order"  # Title of the paper
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
        "Mark Ingraham",
        "3553 Atlantic Avenue",
        "Long Beach, CA 90807",
        "Telephone: (408) 660-5425",
        "Email: ingrahammark7@gmail.com"
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
    c.drawCentredString(width / 2, top_margin - 3.66 * inch, "COUNTY OF LOS ANGELES")

    # (4) Case Title
    c.setFont("Times-Bold", 12)
    case_title = [
        "Mark Ingraham,",
        "Plaintiff and Petitioner,",
        "vs",
        "Los Angeles Police Department",
        "Respondent and Defendant.",        
    ]
    y_position = top_margin - 4.75* inch
    counter=0
    for line in case_title:
        c.setFont("Times-Bold",12)
        if counter==1 or counter==4:
        	c.setFont("Times-Roman",12)
        c.drawString(left_margin, y_position, line)
        y_position -= 0.25 * inch
        counter+=1

    # (5) Case Number
    c.setFont("Times-Roman", 12)
    space=width / 2 + 1 * inch
    c.drawString(space, top_margin - 4* inch, "Casd Number: 25STCP00742")
    # (6) Nature of the Paper (moved slightly lower)
    c.setFont("Times-Bold", 12)
    c.drawString(space, top_margin - 4.25* inch, "")
    c.setFont("Times-Bold", 12)
    c.drawString(space, top_margin - 4.5* inch, "")

    # (7) Judge and Department
    c.setFont("Times-Roman", 12)
    c.drawString(space, top_margin - 4.75 * inch, "Judge: ")
    c.drawString(space, top_margin - 5* inch, "Department: ")

   


    # I. INTRODUCTION
    c.setFont("Times-Bold", 12)
    c.drawString(left_margin, y_position - 0.25* inch, "REQUEST FOR ORDER")
    c.setFont("Times-Roman",12)
    intro_text = [
        "1. I requested an order to prohibit defendant from arresting me.",
        "2. Judge denied order.",
        "3. In that case I can order defendant deported.",
        "4. Most of the LAPD is illegal immigrants.",
        "5. Most officers of the LAPD are eligible for deportation.",
        "6. The remaining officers are bereft of citizenship by treason and also eligible for deportation.",
        "7. All officers of the LAPD are excellent candidates for deportation.",
        "8. Judge should issue order confirming that LAPD is eligible for deportation.",
        ]
    y_position -= .5*inch
    for line in intro_text:
        c.drawString(left_margin, y_position, line)
        y_position -= 0.25* inch



    # Signature Block
    c.setFont("Times-Roman", 12)
    c.drawString(left_margin, y_position - 0.25* inch, "Submitted, Mark Ingraham, 7/29/2025")

 # Add line numbers to the first page
    line_height = 0.25 * inch  # Adjusted to match text spacing
    add_line_numbers(top_margin - 0.5 * inch, bottom_margin + 0.5 * inch, line_height)

    # Add footer (suppressed on the first page)
    add_footer(1)

    # Save the first page
    c.showPage()
    # Save the PDF
    c.save()

if __name__ == "__main__":
    output_filename = "not.pdf"
    create_pdf(output_filename)
    print(f"PDF created: {output_filename}")