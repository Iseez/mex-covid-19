import requests
import bs4
import urllib.request
import os
from datetime import timedelta, date
import time
import argparse
ag = argparse.ArgumentParser()
ag.add_argument("mode",help="Mode of operation, 'all' will download all the pdf technical files in the designated folder while 'update' will only download the missing ones", nargs='?', choices=("all", "update"))
ag.add_argument("-f","--folder",required = True, help = "Folder where the pdf files will be downloaded.")
args = vars(ag.parse_args())
#pdf_path = "/Users/invitado/Documents/Temas compu/covid-19_mex/data/pdf/ctd/"
pdf_path = args["folder"]
if pdf_path[-1:] != "/":
    pdf_path = pdf_path+"/"
def gen_names(no):
    names = []
    for dt in daterange(no):
        names.insert(0,pdf_path+dt.strftime("%Y%m%d")+".pdf")
    return names
def get_links():
    url = "https://www.gob.mx/salud/documentos/informacion-internacional-y-nacional-sobre-nuevo-coronavirus-2019-ncov"
    response = requests.get(url)
    html_parse = bs4.BeautifulSoup(response.text,"html.parser")
    class_a_blank = html_parse.findAll("a",{"target":"_blank"})
    notices = [a for a in class_a_blank if a.parent.name == "div" and a.has_attr("class") == False]
    dwnld = []
    for notice in notices:
        link_base = "https://www.gob.mx"
        link_end = notice["href"]
        dwnld.append(link_base+link_end)
    return dwnld[:-1]
def daterange(days):
    for n in range(days):
        yield date(2020, 1, 23) + timedelta(n)
def download(mode,links):
    os.system('cls' if os.name=='nt' else 'clear')
    if mode == "all":
        if not os.path.exists(pdf_path):
            raise Exception(f'Selected path {pdf_path} was not found, please use a valid path.')
        else:
            all(links)
    elif mode == "update":
        if not os.path.exists(pdf_path):
            raise Exception(f'Couldnt update files, folder path was not {pdf_path}, please use a valid path.')
        else:
            update(links)
    else:
        raise Exception("Value for argument 'mode' isn't valid.")
    return 0
def all(links):
    n=0
    for link in links:
        print(f"Downloading {link[54:]}:\n")
        if len(link) == 103 and link[-14:-10] == "2020":
            n+=1
            urllib.request.urlretrieve(link,pdf_path+link[-14:])
        elif 108>len(link)>103:
            urllib.request.urlretrieve(link,pdf_path+link[89:99]+".pdf")
            n+=1
        elif len(link)<61:
            urllib.request.urlretrieve(link,pdf_path+"2020.02.10.pdf")
            n+=1
        elif len(link) == 64:
            urllib.request.urlretrieve(link,pdf_path+"2020.02.03.pdf")
            n+=1
        elif "China" in link:
            print("Omited file, not from Mexico.")
        else:
            name = input(f"Insert file date in format month.date for file {link[54:]}\n")
            if name[-4:] != ".pdf":
                name = name + ".pdf"
            urllib.request.urlretrieve(link,pdf_path+"2020."+name)
            n+=1
        time.sleep(0.4)
    print(f"Downloaded {n} files in {pdf_path}")
    return f"Downloaded {n} files in {pdf_path}"
def update(links):
    no_links = len(links)-2
    files = [f for f in os.listdir(pdf_path) if os.path.isfile(os.path.join(pdf_path, f)) and f[-4:]==".pdf"]
    no_files = len(files)
    no_dwnld = no_links-no_files
    absent = links[:no_dwnld]
    print(f"Updating {pdf_path}...\n")
    all(absent)
    return f"Downloaded {no_dwnld} files in {pdf_path}"

if __name__ == "__main__":
    links = get_links()
    download(args["mode"],links)
