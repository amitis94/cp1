import numpy as np
import time
import os

from start.flask_app.model import GetInstaImage
from start.flask_app.model import OCR_STS_sBERT


from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/predict', methods=['GET', 'POST'])
def after():
    print(request)
    url = request  # 예시

    post_url = str(url).split('/')[-2]

    now = time

    url_str = str(url).split("?")[1]
    url_str = url_str.replace('%2F', '/')
    url_str = str(url_str).split('/')[-2]


    GetInstaImage.DownInstaImage(url_str, 'static')
    df_ocr = OCR_STS_sBERT.GetCharFromImage('./' + 'static/')

    import shutil
    shutil.rmtree("flask_app/static/static")
    shutil.move("./static", "flask_app/static")

    str_all = ''
    for i in range(10):
        str_all += ' '.join(df_ocr.iloc[0, i])

    isAd = False
    if '광고' in str_all:
        isAd = True
        #print("이 게시글은 광고입니다.")
    isFishing = False

    df_sts = OCR_STS_sBERT.GetStsFromDataFrame(df_ocr, app)
    print(df_sts)
    if len(df_sts) > 0:
        scores, target_nums = OCR_STS_sBERT.GetScoreFromSTS(df_sts)
        scores = scores.tolist()
        # print(scores, target_nums)

        for i in range(len(scores)):
            #print('1번째 이미지와 ', target_nums[i] + 1, '번째 이미지의 연관성 점수 = ', scores[i])
            app.logger.warning(str(i) + ' ' + str(scores[i]))
            if scores[i] < 0.4:
                isFishing = True

    else:
        # 표지에서 글자가 없거나 못찾은 경우
        isFishing = False

    str_out = ''
    if isAd == True:
        if isFishing == True:
            str_out = "이 게시글은 낚시성 광고입니다."
        else:
            str_out = "이 게시글은 일반적인 광고입니다."
    else:
        str_out = "이 게시글은 일반적인 글입니다."

    #return render_template('after.html', data=0.6)


    image_file = [''] * 10
    raw_list = os.listdir("flask_app/static/static")
    jpg_list = []

    for i in range(len(raw_list)):
        if 'jpg' in raw_list[i]:
            jpg_list.append(raw_list[i])

    for i in range(10):
        if i < len(jpg_list):
            image_file[i] = jpg_list[i]
    if len(jpg_list) >= 10:
        image_file[1] , image_file[9] = image_file[9] ,image_file[1]



    return render_template('after.html',
                           file1 = "static/static/" + image_file[0],
                           file2 = "static/static/" + image_file[1],
                           file3 = "static/static/" + image_file[2],
                           file4 = "static/static/" + image_file[3],
                           file5 = "static/static/" + image_file[4],
                           file6 = "static/static/" + image_file[5],
                           file7 = "static/static/" + image_file[6],
                           file8 = "static/static/" + image_file[7],
                           file9 = "static/static/" + image_file[8],
                           file10 = "static/static/" + image_file[9],
                           str_out= str_out)

#if __name__ == '__main__':
#     app.run()
