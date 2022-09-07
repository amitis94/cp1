import uvicorn
from fastapi import FastAPI

#1

app = FastAPI()

@app.get('/')
def index():
    return "hello world"

@app.get('/welcome')
def get_name(name :str):
    return {'Welcome to amitis page': f'{name}'}

if __name__ == '__main__':
    uvicorn.run(app, host= '127.0.0.1', port= 8000)
#uvicorn main:app --reload