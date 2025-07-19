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
        footer_text = "Brief of Appellant"  # Title of the paper
        c.setFont("Times-Roman", 10)  # Font size for footer
        c.drawCentredString(width / 2, footer_y, footer_text)
        # Draw a line above the footer
        c.line(left_margin, footer_y + 0.1 * inch, right_margin, footer_y + 0.1 * inch)



    c.setFont("Times-Bold",14)
    c.drawCentredString(width/2,top_margin,"25-4338")
    # (3) Court Title
    c.setFont("Times-Bold", 14)
    c.drawCentredString(width / 2, top_margin - 3.33 * inch, "UNITED STATES COURT OF APPEALS")
    c.drawCentredString(width / 2, top_margin - 3.66 * inch, "NINTH CIRCUIT")

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
        c.drawCentredString(width/2, y_position, line)
        y_position -= 0.25 * inch
        counter+=1
    y_position -=.25*inch
    c.setFont("Times-Bold",12)
    c.drawCentredString(width/2, y_position, "Brief of Appellant")
# First Page Format (Rule 2.111)
    # (1) Attorney Information
    y_position -=.25*inch
    c.setFont("Times-Roman", 12)
    attorney_info = [
        "Mark Ingraham",
        "3553 Atlantic Avenue",
        "Long Beach, CA 90807",
        "Telephone: (408) 660-5425",
        "Email: ingrahammark7@gmail.com"
    ]
  
    for line in attorney_info:
        c.drawCentredString(width/2, y_position, line)
        y_position -= 0.25 * inch


 

    # Save the first page
    c.showPage()

    # Second Page: Petition Text
    c.setFont("Times-Bold", 14)
    

    y_position = top_margin-1*inch
    # I. INTRODUCTION
    c.setFont("Times-Bold", 12)
    c.drawString(left_margin, y_position, "I. TABLE OF CONTENTS")
    c.setFont("Times-Roman", 12)
    intro_text = [
        "One page.",
    ]
    y_position -= .5*inch
    for line in intro_text:
        c.drawString(left_margin, y_position, line)
        y_position -= 0.5 * inch
    
    c.setFont("Times-Bold", 12)
    c.drawString(left_margin, y_position, "II. TABLE OF AUTHORITIES")
    c.setFont("Times-Roman", 12)
    intro_text = [
        "FOIA.",
    ]
    y_position -= .5*inch
    for line in intro_text:
        c.drawString(left_margin, y_position, line)
        y_position -= 0.5 * inch
    
    c.setFont("Times-Bold", 12)
    c.drawString(left_margin, y_position, "III. JURISDICTIONAL STATEMENT")
    c.setFont("Times-Roman", 12)
    intro_text = [
        "Original case filed 6/25 as FOIA request in plaintiff residing jurisdiction.",
        "Appellate case in district jurisdiction. Dismissal 6/25 appeal 7/11.",
    ]
    y_position -= .5*inch
    for line in intro_text:
        c.drawString(left_margin, y_position, line)
        y_position -= 0.5 * inch
        
    c.setFont("Times-Bold", 12)
    c.drawString(left_margin, y_position, "IV. ISSUES")
    c.setFont("Times-Roman", 12)
    intro_text = [
        "FOIA request for case CS0366753 dismissed because ''cartel activity''.",
    ]
    y_position -= .5*inch
    for line in intro_text:
        c.drawString(left_margin, y_position, line)
        y_position -= 0.5 * inch
    
    c.setFont("Times-Bold", 12)
    c.drawString(left_margin, y_position, "V. CASE")
    c.setFont("Times-Roman", 12)
    intro_text = [
        "Dismissed 6/25.",
    ]
    y_position -= .5*inch
    for line in intro_text:
        c.drawString(left_margin, y_position, line)
        y_position -= 0.5 * inch
    
    c.setFont("Times-Bold", 12)
    c.drawString(left_margin, y_position, "VI. FACTS AND ARGUMENT")
    c.setFont("Times-Roman", 12)
    intro_text = [
        "None.",
    ]
    y_position -= .5*inch
    for line in intro_text:
        c.drawString(left_margin, y_position, line)
        y_position -= 0.5 * inch
        
    c.setFont("Times-Bold", 12)
    c.drawString(left_margin, y_position, "VII. CONCLUSION")
    c.setFont("Times-Roman", 12)
    intro_text = [
        "Defendant will not respond and default will occur if case is heard.",
    ]
    y_position -= .5*inch
    for line in intro_text:
        c.drawString(left_margin, y_position, line)
        y_position -= 0.5 * inch
    
    c.setFont("Times-Bold", 12)
    c.drawString(left_margin, y_position, "IIX. CERTIFICATE OF COMPLAINCE")
    c.setFont("Times-Roman", 12)
    intro_text = [
        "Appellate Brief is 250 words, Roman font, double spaced.",
    ]
    y_position -= .5*inch
    for line in intro_text:
        c.drawString(left_margin, y_position, line)
        y_position -= 0.5 * inch
        


    

    
    
    # Add footer and page number
    add_footer(2)
    add_page_number(2)
    
    c.showPage()
    # Signature Block
    c.setFont("Times-Roman", 12)
    y_position=top_margin-1*inch
    c.drawString(left_margin, y_position - 0.5 * inch, "Submitted,")
    c.drawString(left_margin, y_position - 1 * inch, "Mark Ingraham")
    c.drawString(left_margin, y_position - 1.5 * inch, "7/18/2025")

    # Save the PDF
    c.save()

if __name__ == "__main__":
    output_filename = "writ_of_mandate_petition.pdf"
    create_pdf(output_filename)
    print(f"PDF created: {output_filename}")