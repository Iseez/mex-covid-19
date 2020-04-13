import argparse
import os
ag = argparse.ArgumentParser()
ag.add_argument("-f","--folder", required = True, help = "Folder with the csv data to put together.")
args = vars(ag.parse_args())

folder = args["folder"]
if folder[-1:] != "/":
    folder +="/"
g_path = os.path.join(os.path.abspath(os.path.join(folder, os.pardir)),"grouping")
if not os.path.exists(g_path):
    os.mkdir(g_path)
f_path = os.path.join(g_path,"per_day.csv")

def new():
    head = ["Day","Suspected","New suspected","Positive","New positive","Deceased","New deceased"]
    conf_f = [0,1,1,3,8,11,21,39,26,35,36,30,24,12,37,49,82,105]
    unc_f = [0,1,0,0,2,5,3,10,18,-13,9,1,-6,-6,-12,15,12,33,23]
    for f in sorted(get_files(folder)):
        if f[-4:]==".csv":
            if "/confirmed/" in f:
                conf_f.append(f)
            if "/unconfirmed/" in f:
                unc_f.append(f)
    lens_conf = len_files(conf_f)
    lens_unc = len_files(unc_f)
    new_conf = diffs(lens_conf)
    new_unc = diffs(lens_unc)
    day1 = ["2020.02.24","2020.02.25","2020.02.26","2020.02.27","2020.02.28","2020.02.29","2020.03.1","2020.03.2","2020.03.3","2020.03.4","2020.03.5","2020.03.6","2020.03.7","2020.03.8","2020.03.9","2020.03.10","2020.03.11","2020.03.12","2020.03.13"]
    day2 = [f[-14:-4] for f in conf_f]
    day = day1+day2
    with open(f_path,"w") as csv:
        for i in range(len(head)):
            if i != len(head)-1:
                print(head[i],end=",",file=csv)
            else:
                print(head[i],end="\n",file=csv)
        for i in range(len(conf_f)):
            print(day[i],",",lens_unc[i],",",new_unc[i],",",lens_conf[i],",",new_conf[i],",","0,0", sep='', end='\n', file=csv)
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
def len_files(files):
    lens = []
    for f in files:
        lst = csv2list(f,header=True)
        lens.append(len(lst))
    return lens
def csv2list(path,header = True):
    csv = open(path,"r", encoding = "UTF-8")
    list = []
    i=1
    if header == True:
        i = 0
    for line in csv:
        if i ==0:
            i+=1
            pass
        else:
            list.append(line.strip().split(','))
    csv.close()
    return list
def diffs(arr):
    past = 0
    dif = []
    for current in arr:
        r = current-past
        dif.append(r)
        past = current
    return dif
def add():
    D = csv2list(f_path,header=False)
    last_day = D[-1:][0][0]
    conf_f = []
    unc_f = []
    for f in sorted(get_files(folder)):
        if f[-4:]==".csv":
            if "/confirmed/" in f:
                conf_f.append(f)
            if "/unconfirmed/" in f:
                unc_f.append(f)
    lc = 0
    for f in conf_f:
        if last_day in f:
            lc+=1
            break
        else:
            lc+=1
    conf_f = conf_f[lc:]
    unc_f = unc_f[lc:]
    lens_conf = len_files(conf_f)
    lens_unc = len_files(unc_f)
    new_conf = diffs(lens_conf)
    new_unc = diffs(lens_unc)
    day = [f[-14:-4] for f in conf_f]
    with open(f_path,"a") as csv:
        for i in range(len(conf_f)):
            print(day[i],",",lens_unc[i],",",new_unc[i],",",lens_conf[i],",",new_conf[i],",","0,0", sep='', end='\n', file=csv)
    return

if __name__ == "__main__":
    if os.path.exists(f_path):
        add()
    else:
        new()
