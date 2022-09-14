import uvicorn
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pickle
import numpy as np
import io
from starlette.responses import StreamingResponse

## 개발한 모델 넣어주기
# model = pickle.load()

app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/')
def main(request :Request):
    return templates.TemplateResponse('home.html', context={"request":request})

# html 환경에서 입력으로 받음

@app.post('/predict', response_class=HTMLResponse)
def home(request :Request):
    data1 = Request.form['a'] # Flask에서 request.form과 비슷
    data2 = Request.form['b']
    data3 = Request.form['c']
    data4 = Request.form['d']

    arr = np.array([[data1, data2, data3, data4]])
    # 모델을 설정했을 때
    #pred = model.predict(arr)
    pred = 1
    return templates.TemplateResponse('after.html', context={"request":request})

if __name__ == "__main__":
    uvicorn.run(app)