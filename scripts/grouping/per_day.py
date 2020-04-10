import argparse
import os
ag.add_argument("-f","--folder", required = True, help = "Folder with the csv data to put together.")
args = vars(ag.parse_args())
head = ["No. casos","Suspected","Positive","Deceased"]
folder = args["folder"]
folder = "/Users/invitado/Documents/Temas compu/mex-covid-19/data/csv/cases"
if folder[-1:] != "/":
    folder +="/"
g_path = os.path.join(os.path.dirname(folder),"grouping")
flag = 0
if not os.path.exists(g_path):
    os.mkdir(g_path)
f_path = os.path.join(g_path,"per_day.csv")
if os.path.exists(f_path)
