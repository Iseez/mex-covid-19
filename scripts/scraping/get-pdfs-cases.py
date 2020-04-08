import requests
import bs4
import urllib.request
import os
import argparse
ag = argparse.ArgumentParser()
ag.add_argument("-f","--folder",required = True, help = "Folder where the pdf files will be downloaded.")
args = vars(ag.parse_args())
#pdf_path = "/Users/invitado/Documents/Temas compu/covid-19_mex/data/pdf/cases/"
pdf_path = args["folder"]
if pdf_path[-1:] != "/":
    pdf_path = pdf_path+"/"
def get_links():
    url = "https://www.gob.mx/salud/documentos/coronavirus-covid-19-comunicado-tecnico-diario-238449"
    response = requests.get(url)
    html_parse = bs4.BeautifulSoup(response.text,"html.parser")
    class_a_blank = html_parse.findAll("a",{"target":"_blank"})
    class_a_blank
    notices = [a for a in class_a_blank if a.parent.name == "div" and a.has_attr("class") == False]
    notices
    dwnld = []
    for notice in notices:
        link_base = "https://www.gob.mx"
        link_end = notice["href"]
        dwnld.append(link_base+link_end)
    return dwnld

def dwnld(links):
    n=0
    for link in links:
        if("sospechosos" in link):
            urllib.request.urlretrieve(link,pdf_path+"unconfirmed/"+link[-14:])
        elif("positivo" in link):
            urllib.request.urlretrieve(link,pdf_path+"confirmed/"+link[-14:])
    print("Files updated correctly.\n")
    return f"Files updated correctly."

if __name__ == "__main__":
    links = get_links()
    links
    dwnld(links)
