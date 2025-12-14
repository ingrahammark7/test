from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Frame

footer_text = "Petition for Writ of Mandate"

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

   

    # (3) Court Title
    c.setFont("Times-Bold", 14)
    c.drawCentredString(width / 2, top_margin - 0 * inch, "UNITED STATES DISTRICT COURT")
    c.drawCentredString(width / 2, top_margin - 0.33 * inch, "CENTRAL DISTRICT OF CALIFORNIA")
 

    # (4) Case Title
    c.setFont("Times-Bold", 12)
    case_title = [
        "Mark Ingraham,",
        "Plaintiff and Petitioner,",
        "vs",
        "Los Angeles Police Department",
        "Respondent and Defendant.",        
    ]
    y_position = top_margin - 1.75* inch
    counter=0
    for line in case_title:
        c.setFont("Times-Bold",12)
        if counter==1 or counter==4:
        	c.setFont("Times-Roman",12)
        c.drawCentredString(width/2, y_position, line)
        y_position -= 0.25 * inch
        counter+=1

    # (5) Case Numbe
    c.setFont("Times-Roman", 12)
    space=width / 2 + 1 * inch
    
    y_position=top_margin-4*inch
    
    # First Page Format (Rule 2.111)
    # (1) Attorney Information
    c.setFont("Times-Roman", 12)
    attorney_info = [
        "Case Number: ",
        "Mark Ingraham",
        "3553 Atlantic Avenue",
        "Long Beach, CA 90807",
        "Telephone: (408) 660-5425",
        "Email: ingrahammark7@gmail.com"
    ]
    
    for line in attorney_info:
        c.drawString(space, y_position, line)
        y_position -= 0.25 * inch 
   


    # I. INTRODUCTION
    c.setFont("Times-Bold", 12)
    c.drawCentredString(width/2, top_margin -0.75* inch, footer_text.upper())
    c.setFont("Times-Roman",12)
    intro_text = "/n" 
    y_position -= .25*inch
    
    
    def doer(intro_text,y_position):
    	return doer1(intro_text,y_position,"Times-Roman",80)
    
    def doer1(intro_text,y_position,font,marg):
    	siz=12
    	c.setFont(font, siz)
    	spr=intro_text.split(" ")
    	intro_text1=[""]
    	cc=0
    	tt=""
    	for s in spr:
    		ll=len(s)
    		cc+=ll
    		if(s=="/n"):
    		    		cc=marg+1
    		    		s=""
    		if(cc>marg):
    		    		cc=0
    		    		intro_text1.append(tt)
    		    		tt=""
    		tt+=" "
    		tt+=s
    	for line in intro_text1:
    		if "I." in line or "V." in line:
    			c.setFont("Times-Bold",siz)
    		else:
    			c.setFont(font,siz)
    		c.drawString(left_margin, y_position, line)
    		y_position -= 0.25* inch
    	return y_position
    	
    y_position=doer(intro_text,y_position)
    
    
    
    
    def dopage(cc,num):
    	# Add line numbers to the first page
    	line_height = 0.25 * inch  # Adjusted to match text spacing
    	if(num>1):
    		add_line_numbers(top_margin - 0.5 * inch, bottom_margin + 0.5 * inch, line_height)
    	add_footer(num)
    	cc.showPage()
    	return cc
    	
   
    c=dopage(c,1)
    
    def heads(text,y_position):
    	y_position-=.25*inch
    	c.setFont("Times-Bold", 12)
    	c.drawString(left_margin, y_position, text)
    	c.setFont("Times-Roman",12)
    	intro_text = "/n" 
    	y_position -= .25*inch
    	return y_position
    	
    
    h1=""
    y_position=top_margin-.0*inch
    y_position=heads(h1,y_position)    
    
    c.setFont("Times-Roman", 12)
    text="/n I. INTRODUCTION /n The majority of LAPD officers are illegal inmigrants. Auction and destroy all LAPD vehicles to prevent use by illegals. /n There are four ways this case is under federal jurisdiction. One, if I kill LAPD officers in federal operations there is a non discretionary duty to arrest. Two, the majority of LAPD officers are illegal immigrants. Three, the LAPD violates false claims act by pretending to be law enforcement and not following the law. Four, the LAPD is a Foreign Terrorist Organization. /n II. CONCLUSION /n Petitioner requests court to: /n 2. Auction and destroy all LAPD vehicles. /n 3. Recommend non-discretionary arrest and deportation of all LAPD officers. /n 4. Evidence in report 241015900229 supports all claims. /n"
    y_position=doer(text,y_position)
    c.drawString(left_margin, y_position - 0.25* inch, "Submitted, Mark Ingraham, 12/10/2025")


    # Save the PDF
    c=dopage(c,2)
    c.save()

if __name__ == "__main__":
    output_filename = "not.pdf"
    create_pdf(output_filename)
    print(f"PDF created: {output_filename}")