from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def main():
    return ("Backend Challenge 2021 🏅 - Covid Daily Cases")