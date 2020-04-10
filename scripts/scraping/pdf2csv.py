import argparse
import os
import pdfplumber
ag = argparse.ArgumentParser()
ag.add_argument("mode",help="Mode of operation, 'all' will download all the pdf technical files in the designated folder while 'update' will only download the missing ones", nargs='?', choices=("all", "update"))
ag.add_argument("-f","--folder", required = True, help = "Folder with the pdf tables.")
args = vars(ag.parse_args())
pdf_path = args["folder"]
#pdf_path = "/Users/invitado/Documents/Temas compu/mex-covid-19/data/pdf/cases"
if pdf_path[-1:] != "/":
    pdf_path = pdf_path+"/"
def pdf2csv(in_f,out_f):
    #in_f = "/Users/invitado/Documents/Temas compu/mex-covid-19/data/pdf/cases/unconfirmed/2020.04.06.pdf"
    pdf = pdfplumber.open(in_f)
    content = []
    for page in pdf.pages:
        if len(page.rects) > 0:
            try:
                content += page.extract_table()
            except:
                content += page.extract_table(table_settings={"horizontal_strategy":"text"})
    clean_cont = []
    for row in content:
        clean_cont.append([col.replace("\n","") for col in row if col != None if len(col)>0])
    for i in range(len(clean_cont)):
        if len(clean_cont[i]) > 0:
            if clean_cont[i][0] != None:
                if clean_cont[i][0][0].isdigit():
                    break
    head = [""]*len(content[i])
    content[i]
    for col in range(len(content[0])):
        temp = []
        for row in content[:i]:
            temp.append(row[col])
        for c in temp:
            if c != None :
                if len(c) > 0:
                    head[col]+= c.replace("\n","")
    head = [col for col in head if len(col)>0]
    body = [head]
    n = 1
    for row in clean_cont[i:]:
        if len(row) > 0:
            tmp = [col.replace("\n","") for col in row if col != None if col!=""]
            if not tmp[0][0].isdigit():
                tmp.insert(0,f"{n}")
            body.append(tmp)
        n+=1
    out_f = in_f.replace("pdf","csv")
    parent = os.path.dirname(in_f).replace("pdf","csv")
    if not os.path.exists(parent):
        os.mkdir(parent)
        print(f"Folder '{parent}' created.\n")
    writecsv(body,out_f)
    print(f"Succesfully converted file {in_f} to csv.\n")
    return
def writecsv(arr,out):
    out_f = open(out,"w")
    for row in arr:
        for i in range(len(row)):
            if i != len(row)-1:
                print(row[i],end=",",file=out_f)
            else:
                print(row[i],end="\n",file=out_f)
    out_f.close()
    return
def convert(mode,arr):
    if mode == "all":
        print(f"Converting pdf files in {pdf_path}...\n")
        parent = pdf_path.replace("pdf","csv")
        if not os.path.exists(parent):
            os.mkdir(parent)
            print(f"Folder '{parent}' created.\n")
        n=0
        for f in arr:
            n+=1
            print(f"Converting file {f} to csv:\n")
            pdf2csv(f,f.replace("pdf","csv"))
        print(f"Conrrectly converted {n} files.\n")
    else:
        csvs = [f for f in get_files(pdf_path.replace("pdf","csv")) if f[-4:]==".csv"]
        if len(arr) == len(csvs):
            raise Exception("All files are up to date.\n")
        else:
            print("Updating files...\n")
            absent = []
            for p in arr:
                flag = 0
                for c in csvs:
                    if p.replace("pdf","csv") == c:
                        flag = 1
                if flag != 1:
                    absent.append(p)
            convert("all",absent)
    return
def get_files(path):
    dirs = os.listdir(path)
    files = []
    for entry in dirs:
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            files = files + get_files(full_path)
        else:
            files.append(full_path)
    return files
if __name__ == "__main__":
    pdfs = [f for f in get_files(pdf_path) if f[-4:]==".pdf"]
    convert(args["mode"],pdfs)
