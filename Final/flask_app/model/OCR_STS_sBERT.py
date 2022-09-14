import easyocr
import pandas as pd
from os import listdir,makedirs
from os.path import isfile,join

#이미지 경로들을 입력받아 OCR로 문자들을 검출하여 데이터프레임으로 저장
#입력 : 이미지들이 있는 폴더의 경로
#출력 : OCR 결과 데이터셋 (데이터프레임)
def GetCharFromImage(path):
    raw_files = list(filter(lambda f: isfile(join(path, f)), listdir(path)))

    files = []
    for f in raw_files:
        if 'jpg' in f:
            files.append(f)

    files.sort()
    results = []
    reader = easyocr.Reader(['en', 'ko'])
    ocr = []
    valid = []
    part_ocr = []
    part_vaild = []

    if len(files) == 0:
        print("폴더 안에 이미지가 없습니다.")
        return -1
    elif len(files) == 1:
        print("게시글에 1장의 이미지만 있다면 낚시라고 볼 수 없습니다.")
        return -1

    for fname in files:

        result = reader.readtext(path + fname)
        count_ocr = []
        count_vaild = []
        for i in range(len(result)):
            count_ocr.append(result[i][1])
            count_vaild.append(result[i][2])
        part_ocr.append(count_ocr)
        part_vaild.append(count_vaild)
    ocr.append(part_ocr)
    valid.append(part_vaild)

    for i in range(len(ocr)):
        if len(ocr[i]) < 10:
            while len(ocr[i]) <= 10 - 1:
                ocr[i].append([])
                continue
    else:
        pass

    for i in range(len(valid)):
        if len(valid[i]) < 10:
            while len(valid[i]) <= 10 - 1:
                valid[i].append([])
            continue
    else:
        pass

    category3 = []
    for file in files:
        temp_list = file.split("_")
        category3.append(temp_list[0] + '_' + temp_list[1])

    counter3 = {}
    for value in category3:
        try:
            counter3[value] += 1
        except:
            counter3[value] = 1

    img_silce3 = list(counter3.keys())
    value3 = list(counter3.values())
    print(counter3)
    img_ocr_col = ['img_ocr1', 'img_ocr2', 'img_ocr3', 'img_ocr4', 'img_ocr5', 'img_ocr6', 'img_ocr7', 'img_ocr8', 'img_ocr9', 'img_ocr10']
    img_valid_col = ['img_valid1', 'img_valid2', 'img_valid3', 'img_valid4', 'img_valid5', 'img_valid6', 'img_valid7', 'img_valid8', 'img_valid9', 'img_valid10']

    ocr_data = pd.DataFrame(ocr, columns=img_ocr_col, index=img_silce3)
    valid_data = pd.DataFrame(valid, columns=img_valid_col, index=img_silce3)
    val_data = pd.DataFrame(value3, columns=['img_size'], index=img_silce3)

    data = pd.concat([ocr_data, valid_data, val_data], axis=1)

    return data



#데이터프레임을 받아 Sementic Textual Similarity 데이터셋
#입력 : OCR 결과 (데이터프레임)
#출력 : df_sts (데이터프레임)
def GetStsFromDataFrame(df_ocr, app):

    #신뢰도 필터링
    def truth_filter(ocr_list, truth_list, threshold=0.4):
        r_index = []
        for s_index in range(len(ocr_list)):

            if float(truth_list[s_index]) < threshold:
                continue
            else:
                r_index.append(s_index)
        return [ocr_list[s] for s in r_index]

    df_sts = pd.DataFrame(columns={'1', '2', '3', '4', })
    df_sts.columns = ['first_page', 'target_page', 'score', 'target_num']



    last_index = df_ocr['img_size'][0]

    first_page = truth_filter(df_ocr.iloc[0, 0], df_ocr.iloc[0, 10], 0.4)

    if df_ocr.iloc[0, 0] == df_ocr.iloc[0, 0 + 10]:
        print("첫번째 페이지에서 글자를 찾을 수 없습니다. 첫번째 페이지에서 글자가 없을 경우는 낚시라 판단하지 않아 본 알고리즘에서는 제외")
        return None

    print('last', last_index)
    for j in range(1, last_index):

        target_page = (truth_filter(df_ocr.iloc[0, j], df_ocr.iloc[0, j + 10], 0.4))

        if len(target_page) == 0:
            continue
        else:
            target_page = ' '.join(target_page)

        score = 5
        target_num = j


        df_sts = df_sts.append(pd.Series([first_page, target_page, score, target_num], index=df_sts.columns), ignore_index=True)


    return df_sts

from sentence_transformers import SentenceTransformer, util
import numpy as np

def GetScoreFromSTS(df_sts):

    # 입력이 없을 경우
    if len(df_sts) == 0:
        print("STS 데이터가 없음")
        return -1, -1

    embedder = SentenceTransformer("./output/kor_sts_klue-roberta-base-2022-09-11_06-38-16")


    sentence1 = df_sts['first_page'][0]

    sentence2 = []
    target_nums = []



    for i in range(len(df_sts)):
        sentence2.append(str(df_sts['target_page'][i]))
        target_nums.append(df_sts['target_num'][i])


    sentence2_embeddings = embedder.encode(sentence2, convert_to_tensor=True)

    # Query sentences:

    sentence1_embedding = embedder.encode(sentence1, convert_to_tensor=True)
    cos_scores = util.pytorch_cos_sim(sentence1_embedding, sentence2_embeddings)[0]
    cos_scores = cos_scores.cpu()

    return cos_scores, target_nums

