
from fpdf import FPDF
import img2pdf

#Sample usage:
#generateReport('plots/facts.txt','plots/distPlots.png', 'plots/relPlot')
def generateReport(t, img1, img2):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Reads each line of facts.txt into an array then prints it to the pdf
    with open(t, 'r') as myfile:
        stringReport=myfile.readlines()
    for s in stringReport:
        pdf.cell(200, 5, txt=s, ln=1, align="C")
    print(s)

    pdf.ln(1)  # move 85 down
    pdf.image(img1, w=150, x=30)#, x=10, y=8, w=100)
    pdf.cell(500, 6, ln=1, align="C")
    pdf.image(img2, w=100, x=45)
    pdf.cell(500, 6, ln=1, align="C")
    pdf.output("plots/report.pdf")
    
