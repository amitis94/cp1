from statistics import variance
import uvicorn
from fastapi import FastAPI
from BankNotes import BankNote
import numpy as np
import pickle
import pandas as pd

app = FastAPI()
pickle_in = open("classifier.pkl", "rb")
classifier = pickle.load(pickle_in)

@app.get('/')
def mainpage():
    return "hello world"

@app.post('/predict')
def predict_banknote(data :BankNote):
    data = data.dict()
    print(data)
    print("Hello")

    variance = data['variance']
    skewness = data['skewness']
    curtosis = data['curtosis']
    entropy = data['entropy']
    print(classifier.predict([[variance, skewness, curtosis, entropy]]))

    prediction = classifier.predict([[variance, skewness, curtosis, entropy]])
    if prediction[0] > 0.5:
        prediction = "Fake note"
    else:
        prediction = "It's a Bank note"
    
    return {
        'prediction' : prediction
        }

if __name__ == '__main__':
    uvicorn.run(app, host = '127.0.0.1', port= 8000)
# uvicorn app:app --reload
## 위 명령어에서 처음 언급된 app은 파일 app.py의 app
## 마지막 app은 app.py에 있는 객체 app = FastAPI()