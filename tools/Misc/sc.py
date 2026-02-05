from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Frame

footer_text = ""

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
     #   c.drawCentredString(width / 2, footer_y, footer_text)
        # Draw a line above the footer
     #   c.line(left_margin, footer_y + 0.1 * inch, right_margin, footer_y + 0.1 * inch)

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
    c.drawCentredString(width/2, top_margin - 0 * inch, "No.")
    c.drawCentredString(width / 2, top_margin - .25*inch, "IN THE SUPREME COURT OF THE UNITED STATES")
    
    # (4) Case Title
    c.setFont("Times-Bold", 12)
    case_title = [
        "Mark Ingraham,",
        "Petitioner,",
        "v.",
        "Chase Bank",
        "Respondent.",
        "",
        "",
        "Emergency Petition for Writ of Certiorari to the Supreme Court of California"
    ]
    y_position = top_margin - 1* inch
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
        "Mark Ingraham",
        "3553 Atlantic Avenue",
        "Long Beach, CA 90807",
        "Email: ingrahammark7@gmail.com",
        "Telephone: (408) 660-5425"     
    ]
    
    y_position=bottom_margin+2*inch
    
    for line in attorney_info:
        c.drawString(left_margin, y_position, line)
        y_position -= 0.25 * inch 
   


    # I. INTRODUCTION
    c.setFont("Times-Bold", 12)
    c.drawCentredString(left_margin, top_margin -0.75* inch, footer_text.upper())
    c.setFont("Times-Roman",12)
    intro_text = "" 
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
    		if "I." in line or "V." in line or "X." in line:
    			c.setFont("Times-Bold",siz)
    		else:
    			c.setFont(font,siz)
    		c.drawString(left_margin, y_position, line)
    		y_position -= 0.3* inch
    	return y_position
    	
    y_position=doer(intro_text,y_position)
    
    
    
    
    def dopage(cc,num):
    	# Add line numbers to the first page
    	#line_height = 0.25 * inch  # Adjusted to match text spacing
    	#if(num>1):
    		#add_line_numbers(top_margin - 0.5 * inch, bottom_margin + 0.5 * inch, line_height)
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
    fll=top_margin+1*inch
    y_position=fll
    y_position=heads(h1,y_position)    
    
    c.setFont("Times-Roman", 12)
    text=" I. EXHAUSTION /n All remedies in lower courts have been exhausted per appendix docket information. San Francisco Superior Court case CGC-25-625577 was dismissed. Writ filed to First District Court of Appeals 10/13/2025 case A174520 summary dismissal 10/21/2025. Case S293600 appealed to California Supreme Court and dismissed 11/25/2025. /n II. TABLE OF CONTENTS /n 1. Questions, Parties, Authorities, Opinions, Jurisdiction, Provisions, Case, Argument, Conclusion /n III. STATEMENT OF EMERGENCY /n This case should be forwarded to judge immediately. Immient and irreparable harm will occur. /n IV. QUESTIONS /n Consider all filings fraudulent. Arrest all lower court judges and any other parties to the case. The majority of California employees are illegal immigrants. Petitioner seeks non-discretionary arrest, deportation and execution of all parties to case. /n V. PARTIES /n Original case parties are petitioner, respondent, and California Superior, Appellate and Supreme Courts. /n VI. OPINIONS /n Lower courts issued summary dismissal and no published opinion. /n VII. JURISDICTION /n The federal government has sole jurisdiction over immigration and has jurisdiction over case, as the majority of California employees are illegal immigrants. /n VIII. PROVISIONS /n 18 USC 2381 Treason. /n IX. CASE /n None. /n X. ARGUMENTS /n None. /n XI. CONCLUSION /n Petitioner petitions Court to: /n 1. Arrest, deport and execute all parties to case. /n"
    f2=""
    y_position=doer(text,y_position)
   


    # Save the PDF
    
    """
    y_position=fll
    y_position=doer(f2,y_position)
    """
    c.drawString(left_margin, y_position - 0.25* inch, "Submitted, Mark Ingraham, 1/18/2026")
    c=dopage(c,2)
    """
    c=dopage(c,3)
    app="I. Appendix Index /n A1. Case CGC-25-625577 San Francisco Superior Court docket 10/13/2025 /n A2. Case A174520 First District Appellate Court decision  10/21/2025 /n A3. Case S293600 California Supreme Court docket 11/25/2025 with review denial /n"
  #  y_position=fll
 #   y_position=doer(app,y_position)
#    c=dopage(c,1)
"""
    fl="CERTIFICATE OF SERVICE /n Parties were mailed petition and appendix by US Mail. Parties served are: /n /n Rochelle East, Superior Court Judge /n 400 McAllister St /n San Francisco CA 94102 /n /n San Franciso Superior Court /n 400 McAllister Street /n San Francisco CA 94012 /n /n Chase Bank /n 270 Park Avenue /n New York NY 10017 /n /n California First District Appellate Court /n 350 McAllister Street /n San Francisco CA 94102 /n /n California Supreme Court /n 350 McAllister Street /n San Francisco CA 94102 /n "
    y_position = top_margin
    y_position=doer(fl,y_position)
    c=dopage(c,3)
    c.save()

if __name__ == "__main__":
    output_filename = "not.pdf"
    create_pdf(output_filename)
    print(f"PDF created: {output_filename}")