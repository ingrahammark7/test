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
        footer_text = "Motion for CM/ECF user name and password"  # Title of the paper
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
    c.drawCentredString(width / 2, top_margin - 3.33 * inch, "UNITED STATES DISTRICT COURT FOR THE DISTRICT OF COLUMBIA")
    c.drawCentredString(width / 2, top_margin - 3.66 * inch, "CIVIL DIVISION")

    # (4) Case Title
    c.setFont("Times-Bold", 12)
    case_title = [
        "Mark Ingraham,",
        "             Petitioner and Plaintiff,",
        "         v.",
        "Office of the Comptroller of the Currency",
        "of the United States Department of the Treasury",
        "             Respondent and Defendant."
    ]
    y_position = top_margin - 4.75* inch
    counter=0
    for line in case_title:
        c.setFont("Times-Bold",12)
        if counter==1 or counter==5:
        	c.setFont("Times-Roman",12)
        c.drawString(left_margin, y_position, line)
        y_position -= 0.25 * inch
        counter+=1

    # (5) Case Number
    c.setFont("Times-Roman", 12)
    space=width / 2 + 1 * inch
    c.drawString(space, top_margin - 4* inch, "Case Number:")
    # (6) Nature of the Paper (moved slightly lower)
    c.setFont("Times-Bold", 12)
    c.drawString(space, top_margin - 4.25* inch, "")
    c.setFont("Times-Bold", 12)
    c.drawString(space, top_margin - 4.5* inch, "Motion for CM/ECF username and password")

    # (7) Judge and Department
    c.setFont("Times-Roman", 12)
    c.drawString(space, top_margin - 4.75 * inch, "Judge: ")
    c.drawString(space, top_margin - 5* inch, "Department: ")

   


    # I. INTRODUCTION
    c.setFont("Times-Bold", 12)
    c.drawString(left_margin, y_position - 0.5 * inch, "I. Motion for CM/ECF user name and password")
    c.setFont("Times-Roman", 12)
    c.setFont("Times-Roman", 12)
    intro_text = [
        "1. Petitioner, Mark Ingraham, petitions this Court for a CM/ECF user name and password.",
        "2. Account will be used to file documents on PACER.",
              "3. Petitioner has regular access to the internet, has the capacity to regularly file and view documents", "electronically, and has completed the Clerk's Office tutorial.",
        ]
    y_position -= 1*inch
    for line in intro_text:
        c.drawString(left_margin, y_position, line)
        y_position -= 0.25 * inch



    # Signature Block
    c.setFont("Times-Roman", 12)
    c.drawString(left_margin, y_position - 0.5 * inch, "Submitted,")
    c.drawString(left_margin, y_position - 1 * inch, "Mark Ingraham, 2/15/2025")

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
    output_filename = "ecf1.pdf"
    create_pdf(output_filename)
    print(f"PDF created: {output_filename}")