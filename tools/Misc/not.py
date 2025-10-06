from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Frame

footer_text = "Request for Order"

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
         # Title of the paper
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
    def doy():
    	return top_margin - 0.5 * inch
    y_position = doy()
    for line in attorney_info:
        c.drawString(left_margin, y_position, line)
        y_position -= 0.25 * inch

    # (2) Clerk's Space (blank space to the right of center)
    c.rect(width / 2 + 0.5 * inch, top_margin - 2 * inch, 2 * inch, 1.5 * inch, stroke=1, fill=0)

    # (3) Court Title
    c.setFont("Times-Bold", 14)
    #c.drawCentredString(width / 2, top_margin - 3.33 * inch, "UNITED STATES DISTRICT COURT")
    #c.drawCentredString(width / 2, top_margin - 3.66 * inch, "CENTRAL DISTRICT OF CALIFORNIA")
    c.drawCentredString(width / 2, top_margin - 3.33 * inch, "SUPERIOR COURT OF CALIFORNIA")
    c.drawCentredString(width / 2, top_margin - 3.66 * inch, "COUNTY OF LOS ANGELES")
 

    # (4) Case Title
    c.setFont("Times-Bold", 12)
    case_title = [
        "Mark Ingraham,",
        "Plaintiff and Petitioner,",
        "vs",
        "Department of Public Social Services",
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
    c.drawString(space, top_margin - 4* inch, "Case Number: 25STCP03728")
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
    c.drawString(left_margin, y_position - 0.25* inch, footer_text.upper())
    c.setFont("Times-Roman",12)
    intro_text = "As I stated before, all my order requests are standing requests that apply to all cases. Attached are some orders I am requesting. /n Judge should order UPS store at address on complaint (3553 Atlantic Avenue) to maintain service and not tamper with mail. /n" 
    y_position -= .25*inch
    
    
    def doer(intro_text,y_position):
    	c.setFont("Times-Roman", 12)
    	spr=intro_text.split(" ")
    	intro_text1=[""]
    	cc=0
    	tt=""
    	for s in spr:
    		ll=len(s)
    		cc+=ll
    		if(s=="/n"):
    		    		cc=81
    		    		s=""
    		if(cc>80):
    		    		cc=0
    		    		intro_text1.append(tt)
    		    		tt=""
    		tt+=" "
    		tt+=s
    	for line in intro_text1:
    		c.drawString(left_margin, y_position, line)
    		y_position -= 0.25* inch
    	return y_position
    	
    y_position=doer(intro_text,y_position)
    
    
    
    def dopage(cc,num):
    	# Add line numbers to the first page
    	line_height = 0.25 * inch  # Adjusted to match text spacing
    	add_line_numbers(top_margin - 0.5 * inch, bottom_margin + 0.5 * inch, line_height)
    	add_footer(num)
    	cc.showPage()
    	return cc
    	
    c.setFont("Times-Roman", 12)
    c.drawString(left_margin, y_position - 0.25* inch, "Submitted, Mark Ingraham, 9/19/2025")
    c=dopage(c,2)


    # Save the PDF
    c.save()

if __name__ == "__main__":
    output_filename = "not.pdf"
    create_pdf(output_filename)
    print(f"PDF created: {output_filename}")