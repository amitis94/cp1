from urllib import request
import uvicorn
from flask import Flask, render_template, request
import numpy as np
import GetInstaImage
import OCR_STS_sBERT
import os
import time

#from fastapi import FastAPI, Request
#from fastapi.responses import HTMLResponse
#from fastapi.templating import Jinja2Templates

app = Flask(__name__)

## 개발한 모델 넣어주기
# model = pickle.load()

@app.route('/')
def main():
    return render_template('home.html')

@app.route('/predict', methods=['GET'])
def home():

    print('!!!!!!')
    data1 = request.form['a']  # 예시
    data2 = request.form['b']
    data3 = request.form['c']
    data4 = request.form['d']
    arr = np.array([[data1, data2, data3, data4]])
    # pred = model.predict(arr) ## 모델 풀어주면 주석 지우기

    ## 실제사용
    # image = request.args.get('image','')
    # reader = easyocr.Reader(['ko', 'en'])
    # result = reader.readtext(image, detail=0)
    # return ",".join(result)
    return render_template('after.html', data=0.6)




    data1 = request.form['a'] # 예시
    now = time
    dir_name =( 'instaImages' )
    GetInstaImage.DownInstaImage(data1, dir_name)
    df_ocr = OCR_STS_sBERT.GetCharFromImage(dir_name)

    str_all = ''
    for i in range(10):
        str_all += ' '.join(df_ocr.iloc[0, i])

    if '광고' in str_all:
        isAd = True
        print("이 게시글은 광고입니다.")

    df_sts = OCR_STS_sBERT.GetStsFromDataFrame(df_ocr)
    print(df_sts)
    if len(df_sts) > 0:
        scores, target_nums = OCR_STS_sBERT.GetScoreFromSTS(df_sts)
        scores = scores.tolist()
        # print(scores, target_nums)

        for i in range(len(scores)):
            print('1번째 이미지와 ', target_nums[i] + 1, '번째 이미지의 연관성 점수 = ', scores[i])
            if scores[i] < 0.3:
                isFishing = True

    else:
        # 표지에서 글자가 없거나 못찾은 경우
        isFishing = False

    if isAd == True:
        if isFishing == True:
            print("이 게시글은 낚시성 광고입니다.")
        else:
            print("이 게시글은 일반적인 광고입니다.")
    else:
        print("이 게시글은 일반적인 글입니다.")

    return render_template('after.html', data=0.6)



if __name__ == '__main__':
    uvicorn.run(app)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8888, reload=False, log_level="debug", debug=True,
                workers=1, limit_concurrency=1, limit_max_requests=1)




