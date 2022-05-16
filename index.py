import datetime
from email import message
import os
from urllib import response
from dotenv import load_dotenv
load_dotenv()

os.environ['KAGGLE_USERNAME'] = os.getenv('KAGGLE_USERNAME')
os.environ['KAGGLE_KEY'] = os.getenv('KAGGLE_KEY')
os.environ['MONGO_DB'] = os.getenv('MONGO_DB')
os.environ['DATABASE'] = os.getenv('DATABASE')
os.environ['COLLECTION'] = os.getenv('COLLECTION')
os.environ['HEADER'] = os.getenv('HEADER')

import pymongo
import csv
from kaggle.api.kaggle_api_extended import KaggleApi
from fastapi import FastAPI
from zipfile import ZipFile




PATH = "omicron-covid19-variant-daily-cases"
CSV="covid-variants.csv"

app = FastAPI()

@app.get("/")
def home():
    return ("Backend Challenge 2021 🏅 - Covid Daily Cases")


@app.get("/kaggle")
def kaggle():
    if(not(VerifyUpdates())):
        return ({"Database":"Updated"})
    api = KaggleApi()
    api.authenticate()
    csvfile =  api.dataset_download_files("yamqwe/"+PATH)
    Unzip()
    list = csvReader()
    StoreData(list, os.environ['COLLECTION'])
    DeleleFiles()
    return ({"Database":"Updating"})

def Unzip():
    zf = ZipFile('./' + PATH + '.zip', 'r')
    zf.extractall('./csv')
    zf.close()

def csvReader():
    list = []
    with open("./csv/"+CSV, newline='') as csvfile:
        spamreader = csv.reader(csvfile, skipinitialspace=False,delimiter=',', quotechar='|')
        index = 0
        for row in spamreader:
            if(index == 0):
                report = {
                    "PATH": PATH,
                    "CSV": CSV,
                    "last_upadte": datetime.datetime.now(),
                    "next_update": datetime.datetime.now() + datetime.timedelta(days=1)
                }
                StoreData([report], os.environ['HEADER'])
                DropCollection(os.environ['COLLECTION'])
                index = index + 1
            else:
                report = {
                    "location": row[0],
                    "date": datetime.datetime.strptime(row[1]+"T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
                    "variant": row[2],
                    "num_sequences" : int(float(row[3])),
                    "perc_sequences" : int(float(row[4])),
                    "num_sequences_total": int(float(row[5]))
                }
                list.append(report)

    print(list[1])
    return list


def VerifyUpdates():
    client = pymongo.MongoClient(os.environ['MONGO_DB'])
    database = client[os.environ['DATABASE']]
    collection = database[os.environ['HEADER']]
    header = collection.find_one()
    print(header)
    try:
        if(datetime.datetime.now() > header["next_update"]):
            return True
        else:
            return False
    except:
        DropCollection(os.environ['HEADER'])
        return True

def DropCollection(collectionName):
    client = pymongo.MongoClient(os.environ['MONGO_DB'])
    database = client[os.environ['DATABASE']]
    collection = database[collectionName]
    collection.drop()


def StoreData(itens, collectionName):
    client = pymongo.MongoClient(os.environ['MONGO_DB'])
    database = client[os.environ['DATABASE']]
    collection = database[collectionName]
    list = collection.insert_many(itens)

def DeleleFiles():
    os.remove("./" + PATH +".zip")
    os.remove("./csv/"+CSV)