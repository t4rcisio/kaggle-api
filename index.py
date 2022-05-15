import os
from dotenv import load_dotenv
load_dotenv()

os.environ['KAGGLE_USERNAME'] = os.getenv('KAGGLE_USERNAME')
os.environ['KAGGLE_KEY'] = os.getenv('KAGGLE_KEY')

from kaggle.api.kaggle_api_extended import KaggleApi
from fastapi import FastAPI
from zipfile import ZipFile

import csv


PATH = "omicron-covid19-variant-daily-cases"
CSV="covid-variants.csv"

app = FastAPI()

@app.get("/")
def home():
    return ("Backend Challenge 2021 🏅 - Covid Daily Cases")


@app.get("/kaggle")
def kaggle():
    api = KaggleApi()
    api.authenticate()
    csvfile =  api.dataset_download_files("yamqwe/"+PATH)
    print(type(csvfile))
    Unzip()
    list = csvReader()
    return ("done")

def Unzip():
    zf = ZipFile('./' + PATH + '.zip', 'r')
    zf.extractall('./csv')
    zf.close()

def csvReader():
    list = []
    with open("./csv/"+CSV, newline='') as csvfile:
        spamreader = csv.reader(csvfile, skipinitialspace=False,delimiter=',', quotechar='|')
        for row in spamreader:
            report = {
                "location": row[0],
                "data": row[1],
                "variant": row[2],
                "num_sequences" : row[3],
                "perc_sequences" : row[4],
                "num_sequences_total": row[5]
            }
            list.append(report)
    print(list)
    return list