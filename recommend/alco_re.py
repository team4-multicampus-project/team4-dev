import numpy as np
import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from scipy.spatial import distance_matrix
from scipy.spatial.distance import squareform
from sklearn.preprocessing import MinMaxScaler
from string import punctuation
import re
import json

alco = pd.read_csv('alcohol_df_1.csv')

def percent(dosu):
    # 도수 유사도 구하기
    percent = dosu
    dist_pair = []

    # y축에 임의로 0을 부여한 거리 순서쌍 생성
    for i in range(0,len(percent)):
        temp = []
        temp.append(alco.loc[i]['도수'])
        temp.append(0)
        dist_pair.append(temp)

    # get a distance matrix
    df = pd.DataFrame(dist_pair, columns=['x', 'y'])
    dist_matrix = distance_matrix(df.values, df.values)

    # 정규화
    min_max_scaler = MinMaxScaler()
    regularised = min_max_scaler.fit_transform(dist_matrix)

    # 1에서 빼줘서 더 가까운 것이 우선순위를 갖도록 변경하기
    one_matrix = np.ones((1410,1410))

    final_dist = one_matrix - regularised

    # 확인
    # print(final_dist)
    return final_dist
    
def flavour_sim(flavour):
    flavour = alco['맛'].fillna('')
    # flavour 코사인 유사도 구하기
    # instantiating and generating the count matrix
    count = CountVectorizer()
    count_matrix = count.fit_transform(flavour)

    # generating the cosine similarity matrix
    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    # 확인
    # print(cosine_sim)
    return cosine_sim

def flavour_dosu(cosine_sim, final_dist):
    new_sim = 0.5 * cosine_sim + 0.5 * final_dist

    # print(new_sim)
    return new_sim

# 여러 주종 내 추천
# 주종에 상관 없이 도수와 풍미만 고려해 비슷한 술을 추천해줌
# 항목: 도수, 풍미 (약 6개 항목)

# 주류명을 넣으면 해당 술과 비슷한 Top 10의 주류명을 return
def general_recommendation(input_id, new_sim):
    
    alco_list = []  # 결과를 저장할 리스트

    # 주류명으로 index 찾기 
    idx = alco.index[alco['주류명'] == input_id].tolist() # Int64Index 형식이라 list로 바꾸어줌
    
    # 해당 index의 유사도 리스트 sort in descending order
    score_series = pd.Series(new_sim[idx[0]]).sort_values(ascending=False)
    
    # 유사도 Top 10의 index 추출
    top_10_indexes = list(score_series.iloc[1:11].index)

    # 유사도 1인 항목이 하나 더 있어서 자기 자신이 포함되는 경우에는 자신을 뺀 Top 10의 index 재추출
    if top_10_indexes[0] == idx[0]:
        top_10_indexes = list(score_series.iloc[1:12].index)
        top_10_indexes.remove(idx[0])
    
    # 고유 주류명을 담기 위한 empty list 생성
    top_10_id = []
    
    # 주류명 list
    for i in top_10_indexes:
        id = alco.loc[i]['주류명']
        top_10_id.append(id)
    
    for i in range(0, 10):
        filtered_alco = alco[alco['주류명'] == top_10_id[i]]  # 주류명이 일치하는 데이터 필터링
        filtered_data = filtered_alco[[ '주류','주류명', '생산국가', '도수','음용온도','특징']].fillna('')  # 가져오고자 하는 열을 선택
        for _, row in filtered_data.iterrows():
            for key, value in row.items():
                if key not in ['id', '용량'] and pd.notnull(value):
                    filtered_data= f"{key} : {value}"
                    alco_list.append(filtered_data)  # 필터링된 데이터를 리스트에 추가
                    # print(f'{key}: {value}')

    return alco_list


def wine_sim(alco):
    # wine word list 만들기
    wine_list = [] # empty list

    # wine index list 추출
    wine_idx = alco.index[alco['주류'] == "와인"].tolist()

    # wine: category, percent, origin, producer, wine_grape, flavour
    # 중분류, 도수, 생산자, 생산국가, 주요품종 

    for i in wine_idx:
        temp = ""
        temp = temp + alco.loc[i]['중분류'] + " " + alco.loc[i]['생산국가'] + " " + alco.loc[i]['생산자/제조사'].replace(" ", "") + " " + alco.loc[i]['포도품종'].replace(" ", "") + " "
        
        alco['맛'] = alco['맛'].fillna('')
        for flavour in alco.loc[i]['맛']:
            temp = temp + flavour

        wine_list.append(temp)

    # wine 코사인 유사도 구하기
    # instantiating and generating the count matrix
    count = CountVectorizer()
    wine_matrix = count.fit_transform(wine_list)

    # generating the cosine similarity matrix
    wine_sim = cosine_similarity(wine_matrix, wine_matrix)

    # wine 도수 유사도 구하기
    wine_pair = []

    # y축을 임의로 0을 부여한 거리 순서쌍 생성
    for i in wine_idx:
        temp = []
        temp.append(alco.loc[i]['도수'])
        temp.append(0)
        wine_pair.append(temp)

    # get a distance matrix
    wine_df = pd.DataFrame(wine_pair, columns=['x', 'y'])
    wine_matrix = distance_matrix(wine_df.values, wine_df.values)

    # 정규화
    min_max_scaler = MinMaxScaler()
    wine_regularised = min_max_scaler.fit_transform(wine_matrix)

    # 1에서 빼줘서 더 가까운 것이 우선순위를 갖도록 변경하기
    wine_one_matrix = np.ones((len(wine_idx),len(wine_idx)))

    wine_final_dist = wine_one_matrix - wine_regularised

    # 도수 유사도, 타 정보 유사도 각각 0.5씩 weight 부여 후 새로운 matrix 생성
    wine_new_sim = 0.5 * wine_sim + 0.5 * wine_final_dist

    # 확인
    # print(wine_new_sim)
    return wine_new_sim,wine_idx

def kor_sim(alco):
    # 전통주 word list 만들기
    kor_list = [] # empty list

    # 전통주 index list 추출
    kor_idx = alco.index[alco['주류'] == "전통주"].tolist()

    # 도수, 중분류, 주원료 , 생산자/제조사

    for i in kor_idx:
        temp = ""
        temp = temp + str(alco.loc[i]['중분류']) + " " + str(alco.loc[i]['주원료'])+ " " +alco.loc[i]['생산자/제조사'].replace(" ", "")
        
        for flavour in alco.loc[i]['맛']:
            temp = temp + flavour

        kor_list.append(temp)

    # 전통주 코사인 유사도 구하기
    # instantiating and generating the count matrix
    count = CountVectorizer()
    kor_matrix = count.fit_transform(kor_list)

    # generating the cosine similarity matrix
    kor_sim = cosine_similarity(kor_matrix, kor_matrix)

    # 전통주 도수 유사도 구하기
    kor_pair = []

    # y축을 임의로 0을 부여한 거리 순서쌍 생성
    for i in kor_idx:
        temp = []
        temp.append(alco.loc[i]['도수'])
        temp.append(0)
        kor_pair.append(temp)

    # get a distance matrix
    kor_df = pd.DataFrame(kor_pair, columns=['x', 'y'])
    kor_matrix = distance_matrix(kor_df.values, kor_df.values)

    # 정규화
    min_max_scaler = MinMaxScaler()
    kor_regularised = min_max_scaler.fit_transform(kor_matrix)

    # 1에서 빼줘서 더 가까운 것이 우선순위를 갖도록 변경하기
    kor_one_matrix = np.ones((len(kor_idx),len(kor_idx)))

    kor_final_dist = kor_one_matrix - kor_regularised

    # 도수 유사도, 타 정보 유사도 각각 0.5씩 weight 부여 후 새로운 matrix 생성
    kor_new_sim = 0.5 * kor_sim + 0.5 * kor_final_dist

    # 확인
    # print(kor_new_sim)
    return kor_new_sim, kor_idx

# 해당 id의 술이 와인인지 체크
def is_wine(input_id):
    temp_idx = alco.index[alco['주류명'] == input_id].tolist() # Int64Index 형식이라 list로 바꾸어줌
    result = alco.loc[temp_idx[0]]['주류'] == "와인"
    return result

# 와인의 고유 id를 넣으면 해당 와인과 비슷한 Top 10 와인의 id를 return
def wine_recommendation(input_id, wine_new_sim,wine_idx):
    
    w_list = []  # 결과를 저장할 리스트

    # 주류명으로 index 찾기 
    idx = alco.index[alco['주류명'] == input_id].tolist() # Int64Index 형식이라 list로 바꾸어줌
    
    # wine_idx list 내에서 몇번째 와인인지 구하기
    w_idx = wine_idx.index(idx[0])
    
    # 해당 index의 유사도 리스트 sort in descending order
    score_series = pd.Series(wine_new_sim[w_idx]).sort_values(ascending=False)
    
    # 유사도 Top 10의 index 추출
    wine_top_10_indexes = list(score_series.iloc[1:11].index)

    # 유사도 1인 항목이 하나 더 있어서 자기 자신이 포함되는 경우에는 자신을 뺀 Top 10의 index 재추출
    if wine_top_10_indexes[0] == w_idx:
        wine_top_10_indexes = list(score_series.iloc[1:12].index)
        wine_top_10_indexes.remove(w_idx)
    
    # 고유 주류명을 담기 위한 empty list 생성
    wine_top_10_id = []
    
    # 주류명 list
    for i in wine_top_10_indexes:
        index = wine_idx[i] # wine list에서 몇번째인지가 아니라 전체 술 list에서 몇번째인지 구함
        id = alco.loc[index]['주류명']
        wine_top_10_id.append(id)
    
    for i in range(0, 10):
        filtered_alco = alco[alco['주류명'] == wine_top_10_id[i]]  # 주류명이 일치하는 데이터 필터링
        filtered_data = filtered_alco[[ '주류', '중분류', '주류명', '생산국가', '포도품종','도수','음용온도','추천음식']].fillna('')  # 가져오고자 하는 열을 선택
        for _, row in filtered_data.iterrows():
            for key, value in row.items():
                if key not in ['id', '용량'] and pd.notnull(value):
                    filtered_data= f"{key} : {value}"
                    w_list.append(filtered_data)  # 필터링된 데이터를 리스트에 추가
                    # print(f'{key}: {value}')   

    return w_list


# 해당 id의 술이 전통주인지 체크
def is_kor(input_id):
    temp_idx = alco.index[alco['주류명'] == input_id].tolist() # Int64Index 형식이라 list로 바꾸어줌
    result = alco.loc[temp_idx[0]]['주류'] == "전통주"
    return result

#  전통주의 고유 id를 넣으면 해당 전통주와 비슷한 Top 10 전통주의 주류명를 return
def kor_recommendation(input_id, kor_new_sim, kor_idx):
    
    k_list = []  # 결과를 저장할 리스트

    # 주류명으로 index 찾기 
    idx = alco.index[alco['주류명'] == input_id].tolist() # Int64Index 형식이라 list로 바꾸어줌
    
    # kor_idx list 내에서 몇번째 전통주인지 구하기
    k_idx = kor_idx.index(idx[0])
    
    # 해당 index의 유사도 리스트 sort in descending order
    score_series = pd.Series(kor_new_sim[k_idx]).sort_values(ascending=False)
    
    # 유사도 Top 10의 index 추출
    kor_top_10_indexes = list(score_series.iloc[1:11].index)

    # 유사도 1인 항목이 하나 더 있어서 자기 자신이 포함되는 경우에는 자신을 뺀 Top 10의 index 재추출
    if kor_top_10_indexes[0] == k_idx:
        kor_top_10_indexes = list(score_series.iloc[1:12].index)
        kor_top_10_indexes.remove(k_idx)
    
    # 고유 주류명을 담기 위한 empty list 생성
    kor_top_10_id = []
    
    # 주류명 list
    for i in kor_top_10_indexes:
        index = kor_idx[i] # wine list에서 몇번째인지가 아니라 전체 술 list에서 몇번째인지 구함
        id = alco.loc[index]['주류명']
        kor_top_10_id.append(id)
    
    for i in range(0, 10):
        filtered_alco = alco[alco['주류명'] == kor_top_10_id[i]]  # 주류명이 일치하는 데이터 필터링
        filtered_data = filtered_alco[['주류', '중분류','주류명',  '생산국가', '주원료','도수','음용온도','특징']].fillna('')  # 가져오고자 하는 열을 선택
        for _, row in filtered_data.iterrows():
            for key, value in row.items():
                if key not in ['id', '용량'] and pd.notnull(value):
                    filtered_data= f"{key} : {value}"
                    k_list.append(filtered_data)  # 필터링된 데이터를 리스트에 추가
                    # print(f'{key}: {value}')
            
    return k_list


def recom(test_num):

    # 주류명 출력 
    alc = pd.read_csv('alcohol_df_1.csv')
    dosu = alc['도수']
    final_dist = percent(dosu) 
    flavor = alc['맛']
    cosine_sim = flavour_sim(flavor)
    new_sim = flavour_dosu(cosine_sim, final_dist)
    wine_new_sim,wine_idx = wine_sim(alc)
    kor_new_sim,kor_idx =kor_sim(alc)

    if not test_num :  # 검색어가 비어있는 경우 빈 리스트 반환
        return {"general": [], "alc_cate": []}
    
    ge_re = general_recommendation(test_num, new_sim) # 주류명을 넣으면 주류상관없이 비슷한 술 top10 추천  

    if is_wine(test_num) == True:
        realco = wine_recommendation(test_num,wine_new_sim,wine_idx)# 와인 주류명을 넣으면 해당 와인과 비슷한 Top 10 와인의 주류명 출력 
    elif is_kor(test_num) == True:
        realco = kor_recommendation(test_num,kor_new_sim,kor_idx)# 전통주 주류명을 넣으면 해당 전통주와 비슷한 top10 와인의 주류명을 출력 
    else :
        realco = ''
    # print(ge_re)
    # print(realco)
    contx_dic = {
    'general': ge_re,
    'alc_cate': realco,
            }
    
    return contx_dic

