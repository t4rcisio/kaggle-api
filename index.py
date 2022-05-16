import datetime
from email import message
import os
from urllib import response
from dotenv import load_dotenv
load_dotenv()

# Variáveis de ambiente
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

# Rota default
@app.get("/")
def home():
    return ("Backend Challenge 2021 🏅 - Covid Daily Cases")

# Rota para atualizar o banco
@app.get("/kaggle")
def kaggle():
    # O Banco está configurado para atualizar a cada 24 horas
    # Assim, sempre que a rota de atualização do banco for solicitada,
    # vefifica se é preciso fazer uma atualização
    if(not(VerifyUpdates())):
        return ({"Database":"Updated"})
    api = KaggleApi()
    api.authenticate()

    # Baixa o arquivo zip da página
    csvfile =  api.dataset_download_files("yamqwe/"+PATH)

    # Descompacta o arquivo na pasta ./csv
    Unzip()

    # Gera um array com os dados do arquivo
    list = csvReader()

    #Envia os arquivos para resem gravados no banco
    StoreData(list, os.environ['COLLECTION'])

    #Deleta os arquivos gerados
    DeleleFiles()
    return ({"Database":"Updating"})

def Unzip():
    zip = ZipFile('./' + PATH + '.zip', 'r')
    zip.extractall('./csv')
    zip.close()

def csvReader():
    # Percorre as linhas do arquivo CSV e as coloca em uma lista
    list = []
    with open("./csv/"+CSV, newline='') as csvfile:
        spamreader = csv.reader(csvfile, skipinitialspace=False,delimiter=',', quotechar='|')
        index = 0
        for row in spamreader:
            if(index == 0):
                # A primeira linha trata-se do cabeçalho, então ela é descartada
                # Nesse momento, um novo metadata é gerado
                report = {
                    "PATH": PATH,
                    "CSV": CSV,
                    "last_update": datetime.datetime.now(), # Data e hora atual
                    "next_update": datetime.datetime.now() + datetime.timedelta(days=1) # Próximo update do banco
                }
                StoreData([report], os.environ['HEADER']) # Grava os dados
                DropCollection(os.environ['COLLECTION']) # Apaga a coleção dados atual
                index = index + 1
            else:
                # Monta um objeto no formato do esquema a ser gravado no banco
                report = {
                    "location": row[0],
                    "date": datetime.datetime.strptime(row[1]+"T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
                    "variant": row[2],
                    "num_sequences" : int(float(row[3])),
                    "perc_sequences" : int(float(row[4])),
                    "num_sequences_total": int(float(row[5]))
                }
                list.append(report)
                # Insere o elemento na lista 
    return list


def VerifyUpdates():
    # Consulta na tabela metadata quando foi a última atualização do banco 
    client = pymongo.MongoClient(os.environ['MONGO_DB'])
    database = client[os.environ['DATABASE']]
    collection = database[os.environ['HEADER']]
    header = collection.find_one()
    try:
        # Caso tenha mais de 24h da última atualização, então o banco sofrerá uma atualização
        if(datetime.datetime.now() > header["next_update"]):
            return True
        else:
            return False
    except:
        #Apaga os dados do metadata
        DropCollection(os.environ['HEADER'])
        return True

def DropCollection(collectionName):
    client = pymongo.MongoClient(os.environ['MONGO_DB'])
    database = client[os.environ['DATABASE']]
    collection = database[collectionName]
    collection.drop()


def StoreData(itens, collectionName):
    # Faz uma conexão com o banco
    client = pymongo.MongoClient(os.environ['MONGO_DB'])
    database = client[os.environ['DATABASE']]
    collection = database[collectionName]
    # Insere tudo no banco - Devido ao alto volume de dados, 
    # o processo leva em torno de 55 segundos!
    list = collection.insert_many(itens)

def DeleleFiles():
    os.remove("./" + PATH +".zip")
    os.remove("./csv/"+CSV)