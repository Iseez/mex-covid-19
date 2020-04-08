from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import argparse
import tabula
import re
ag = argparse.ArgumentParser()
ag.add_argument("-i","--in", type = argparse.FileType("rb"), required = True, help = "Name of pdf file to convert to be converted.")
#ag.add_argument("-o","--out", type = argparse.FileType("w"), required = True, help = "Name of csv output file.")
args = vars(ag.parse_args())
in_file = open("/Users/invitado/Documents/Temas compu/mex-covid-19/data/pdf/cases/confirmed/2020.03.23.pdf","rb")
#in_file = args["in"]
#out_file = args["out"]
#Returns pdf as a string

def pdf_text(file):
    output_string = StringIO()      #A string loaded on buffer
    parser = PDFParser(file)     #Read file, add file to buffer maybe binary?
    doc = PDFDocument(parser)       #Now it is a pdf file
    rsrcmgr = PDFResourceManager()  #Idfk
    laparams=LAParams()
    device = TextConverter(rsrcmgr, output_string, laparams=laparams) #converts to string
    interpreter = PDFPageInterpreter(rsrcmgr, device)                   #Separates in pages?
    for page in PDFPage.create_pages(doc):                              #Separates in pages part 2?
        interpreter.process_page(page)
    return output_string.getvalue()
def extract_cases(string):
    rows = pdf.split("\n")
    rows
    i= 0
    for row in rows:
        print(row, i)
        i+=1
    cases = [row for row in rows if re.match(r"\d",row)]
    cases
    return 0
pdf = pdf_text(in_file)
pdf
if re.match(r"^ +\d",rows[157]).group():
    print("h")



# Read pdf into list of DataFrame
df = tabula.read_pdf("/Users/invitado/Documents/Temas compu/covid-19_mex/data/pdf/2020.01.23.pdf", pages='all',guess=False)
df
# Read remote pdf into list of DataFrame
df2 = tabula.read_pdf("https://github.com/tabulapdf/tabula-java/raw/master/src/test/resources/technology/tabula/arabic.pdf")

# convert PDF into CSV file
tabula.convert_into("/Users/invitado/Documents/Temas compu/covid-19_mex/data/pdf/2020.01.23.pdf","/Users/invitado/Documents/Temas compu/covid-19_mex/data/csv/2020.01.23_1.csv", output_format="csv", pages='all')

# convert all PDFs in a directory
tabula.convert_into_by_batch("input_directory", output_format='csv', pages='all')
