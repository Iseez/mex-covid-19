import argparse
import pdfplumber
ag = argparse.ArgumentParser()
ag.add_argument("-i","--in", required = True, help = "Name of pdf file to convert to be converted.")
ag.add_argument("-o","--out", type = argparse.FileType("w"), required = True, help = "Name of csv output file.")
args = vars(ag.parse_args())
def pdf2csv(in_f,out_f):
    pdf = pdfplumber.open(in_f)
    content = []
    for page in pdf.pages:
        content += page.extract_table()
    for i in range(len(content)):
        if content[i][0] != None:
            if content[i][0][0].isdigit():
                break
    head = [col.replace("\n","") for col in content[0] if len(col)>0]
    body = [head]
    for row in content[i:]:
        body.append([col.replace("\n","") for col in row if col != None])
    writecsv(body,out_f)
    print(f"Succesfully converted file {in_f} to csv.\n")
    return
def writecsv(arr,out):
    header = ["No. caso","Estado","Sexo","Edad","Fecha de inicio de sintomas",]
    print()
    for row in arr:
        print(row,sep="",end="\n",file=out)
    out.close()
    return
if __name__ == "__main__":
    pdf2csv(args["in"],args["out"])
