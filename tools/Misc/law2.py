from fpdf import FPDF
import os

def sanitize_text(text):
    replacements = {
        "’": "'",
        "“": '"',
        "”": '"',
        "—": "-",
        "–": "-",
        "…": "...",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "SUPERIOR COURT OF CALIFORNIA, COUNTY OF LOS ANGELES", 0, 1, "C")
        self.cell(0, 10, "STANLEY MOSK COURTHOUSE", 0, 1, "C")
        self.ln(5)
        
    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, 0, 1, "L")
        self.ln(3)
        
    def chapter_body(self, body):
        self.set_font("Arial", "", 11)
        body = sanitize_text(body)
        self.multi_cell(0, 8, body)
        self.ln()
        
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Title page with case info
pdf.set_font("Arial", "B", 14)
pdf.cell(0, 10, "NOTICE OF MOTION AND MOTION TO CONSOLIDATE HEARINGS", 0, 1, "C")
pdf.cell(0, 10, "Case No. 25STCP00742 and 25STCP02262", 0, 1, "C")
pdf.cell(0, 10, "Stanley Mosk Courthouse - Dept. 86", 0, 1, "C")
pdf.ln(10)

# Notice of Motion and Motion to Consolidate Hearings
pdf.chapter_title("NOTICE OF MOTION AND MOTION TO CONSOLIDATE HEARINGS")
notice_motion_text = (
    "MARK INGRAHAM\n"
    "Petitioner in Pro Per\n\n"
    "TO ALL PARTIES AND TO THE COURT:\n\n"
    "PLEASE TAKE NOTICE that petitioner Mark Ingraham hereby moves the Court to consolidate the hearing "
    "currently set in case number 25STCP02262 into the earlier hearing set in case number 25STCP00742, scheduled "
    "for July 24, 2025, in Department 86 of the Stanley Mosk Courthouse.\n\n"
    "This motion is made pursuant to Code of Civil Procedure section 1048(a) on the grounds that both cases involve "
    "overlapping facts and legal issues concerning police records and actions, and judicial economy favors hearing "
    "the matters together.\n\n"
    "This motion is based on this Notice, the attached Memorandum of Points and Authorities, the Declaration of Mark "
    "Ingraham, the pleadings and papers on file, and any argument the Court may permit at the hearing.\n\n"
    "Dated: July 2, 2025\n"
    "Respectfully submitted,\n\n"
    "_________________________\n"
    "Mark Ingraham\n"
    "Petitioner in Pro Per\n"
)
pdf.chapter_body(notice_motion_text)

# Memorandum of Points and Authorities
pdf.chapter_title("MEMORANDUM OF POINTS AND AUTHORITIES")
mpa_text = (
    "I. INTRODUCTION\n\n"
    "Petitioner seeks to consolidate the hearing in case number 25STCP02262 with the earlier hearing in case number 25STCP00742, "
    "currently scheduled for July 24, 2025, in Department 86 of the Stanley Mosk Courthouse. Both cases relate to the same factual "
    "background and involve overlapping legal issues concerning petitioner’s efforts to obtain police records and compel specific law "
    "enforcement actions.\n\n"
    "II. LEGAL STANDARD\n\n"
    "Under Code of Civil Procedure section 1048(a), “when actions involving a common question of law or fact are pending before the court, "
    "it may order a joint hearing or trial of any or all the matters in issue in the actions.”\n\n"
    "III. ARGUMENT\n\n"
    "Consolidation of hearings is appropriate where it promotes judicial economy, avoids duplication, and prevents inconsistent rulings. "
    "Here, petitioner is the sole party in 25STCP02262, and LAPD is the respondent in 25STCP00742. The issues in both matters stem from a "
    "related set of facts and requests directed at law enforcement. Holding separate hearings would waste court resources and create procedural redundancy. "
    "Consolidation of hearings—not full consolidation—is sufficient to address the overlapping issues and ensure consistent handling.\n\n"
    "IV. CONCLUSION\n\n"
    "For the foregoing reasons, petitioner respectfully requests that the Court order that the hearing in case 25STCP02262 be consolidated "
    "into the hearing in case 25STCP00742, set for July 24, 2025.\n\n"
    "Dated: July 2, 2025\n"
    "Respectfully submitted,\n\n"
    "_________________________\n"
    "Mark Ingraham\n"
    "Petitioner in Pro Per\n"
)
pdf.chapter_body(mpa_text)

# Declaration of Mark Ingraham
pdf.chapter_title("DECLARATION OF MARK INGRAHAM")
declaration_text = (
    "I, Mark Ingraham, declare as follows:\n\n"
    "1. I am the petitioner in both case number 25STCP00742 and 25STCP02262, currently pending in the Los Angeles County Superior Court, Stanley Mosk Courthouse.\n\n"
    "2. Case number 25STCP00742, in which the Los Angeles Police Department is named as respondent, is scheduled for hearing on July 24, 2025, in Department 86.\n\n"
    "3. Case number 25STCP02262 is also related to police records and actions and involves issues that are duplicative of those in case 25STCP00742.\n\n"
    "4. I previously filed a Notice of Related Case stating that these cases are connected and that the hearing in 25STCP02262 could be merged with the hearing in 25STCP00742.\n\n"
    "5. I respectfully request that the Court consolidate the hearing in 25STCP02262 into the hearing already scheduled in 25STCP00742 to avoid duplication and promote judicial efficiency.\n\n"
    "I declare under penalty of perjury under the laws of the State of California that the foregoing is true and correct.\n\n"
    "Executed on July 2, 2025, in Los Angeles, California.\n\n"
    "_________________________\n"
    "Mark Ingraham\n"
)
pdf.chapter_body(declaration_text)

# Proposed Order
pdf.chapter_title("[PROPOSED] ORDER GRANTING MOTION TO CONSOLIDATE HEARINGS")
order_text = (
    "The Court, having reviewed and considered petitioner’s motion to consolidate the hearing in case number 25STCP02262 "
    "with the hearing in case number 25STCP00742, and good cause appearing:\n\n"
    "IT IS HEREBY ORDERED:\n\n"
    "The hearing in case number 25STCP02262 is consolidated into the hearing in case number 25STCP00742, currently scheduled for "
    "July 24, 2025, in Department 86 of the Stanley Mosk Courthouse. Both matters will be heard together at that time.\n\n"
    "IT IS SO ORDERED.\n\n"
    "Dated: _______________                   _______________________________\n"
    "                                         JUDGE OF THE SUPERIOR COURT\n"
)

pdf.chapter_body(order_text)

file_path = os.path.join(os.getcwd(), "Motion_to_Consolidate_Hearings_25STCP00742_25STCP02262.pdf")
pdf.output(file_path)

print(f"PDF generated at: {file_path}")