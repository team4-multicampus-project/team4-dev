import csv
import requests
import json
from datetime import datetime, timedelta
import time
import random
import pandas as pd 
data = pd.read_csv('wth.csv')

# 프론트로 가져올필요 없음
def read_csv_file(): # csv 파일 읽기
    # CSV 파일 경로
    file_path = 'wth.csv' # csv 파일은 그냥 DB에 넣지 말고 파일로 넣기
    data = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

# 프론트로 가져올필요 없음
def find_matching_location(data, user_location):
    for row in data:
        if row['1단계'] == user_location or row['2단계'] == user_location or row['3단계'] == user_location:
            grid_x = row['격자 X']
            grid_y = row['격자 Y']
            return grid_x, grid_y
    return None
# 프론트로 가져올필요 없음
# 날씨 정보(api) 호출하는 함수
def get_current_weather(grid_x, grid_y):
    api_url = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"

    api_key = "NfupLYj2CO3o5otVdlf89svkodG41mt0W1iia%2B0vBlVMeLQrthCYXlpIEns2fvWyVTCy3kHqrAmsZ31swYn7DQ%3D%3D"
    # "jSyht54oXEynj%2B2YfWIm4rgQ%2F0BmAP9QkmXIOPwG9Oh6kXqjpMK2WwKKcZTStBj8swVyL6lEcJj555RyTRch9A%3D%3D" 안되면 이걸로 활용

    now = datetime.now()
    base_date = now.strftime("%Y%m%d")
    base_time = (now - timedelta(hours=1)).strftime("%H30")

    params = {
        "serviceKey": api_key,
        "pageNo": "1",
        "numOfRows": "30",
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": grid_x,  
        "ny": grid_y
    }

    response = None
    data = None

    while True:
        try:
            response = requests.get(api_url, params=params)
            data = json.loads(response.text)
            break  # 성공적으로 데이터를 가져왔을 경우 반복문 종료
        except:
            time.sleep(5)  # 10초 대기 후 재시도
    
    return data
# 프론트로 가져와야됨
def data_parse(data):
    print('parse')
    # 날씨 정보 출력
    if 'response' in data and 'body' in data['response'] and 'items' in data['response']['body']:
        items = data['response']['body']['items']['item']
        for item in items:
            category = item['category']
            fcst_value = item['fcstValue']
            
            if category == 'PTY':
                pty = fcst_value
            elif category == 'SKY':
                sky = fcst_value
            elif category == 'T1H':
                t1h = fcst_value

        # '강수형태:', pty
        # '하늘상태:', sky
        # '기온:', t1h

        sky_mapping = {
            '1': '맑음',
            '3': '구름많음',
            '4': '흐림'
        }
        sky_description = sky_mapping.get(sky, '알 수 없음')

        # Map PTY code to weather description
        pty_mapping = {
            '0': '없음',
            '1': '비',
            '2': '비/눈',
            '3': '눈',
            '5': '빗방울',
            '6': '빗방울눈날림',
            '7': '눈날림',
            '4': '소나기'  # (단기) 소나기 코드 추가
        }
        pty_description = pty_mapping.get(pty, '알 수 없음')

        pty_f = [pty,pty_description]

        print('강수형태:', pty_description)
        print('하늘상태:', sky_description)
        print('기온:', t1h)
        return sky_description, pty_f, t1h
    else:
        print("날씨 정보를 가져올 수 없습니다.")
        return None, None, None
    
# 프론트로 가져와야됨
def get_loc(user_location):
    data = read_csv_file()
    grid_x, grid_y = find_matching_location(data,user_location)

    if grid_x and grid_y:
        print(f"격자 X: {grid_x}")
        print(f"격자 Y: {grid_y}")
    else:
        print("일치하는 장소가 없습니다.")   

    # 현재 날씨 정보 조회
    # data_w = get_current_weather(grid_x, grid_y) # api쓰는건데 너무 오래걸림... 시연할때는 밑에꺼 바꿔서 하는게 좋음
    data_w = {"response":{"header":{"resultCode":"00","resultMsg":"NORMAL_SERVICE"},"body":{"dataType":"JSON","items":{"item":[{"baseDate":"20230630","baseTime":"0630","category":"LGT","fcstDate":"20230630","fcstTime":"0700","fcstValue":"0","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"LGT","fcstDate":"20230630","fcstTime":"0800","fcstValue":"0","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"LGT","fcstDate":"20230630","fcstTime":"0900","fcstValue":"0","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"LGT","fcstDate":"20230630","fcstTime":"1000","fcstValue":"0","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"LGT","fcstDate":"20230630","fcstTime":"1100","fcstValue":"0","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"LGT","fcstDate":"20230630","fcstTime":"1200","fcstValue":"0","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"PTY","fcstDate":"20230630","fcstTime":"0700","fcstValue":"0","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"PTY","fcstDate":"20230630","fcstTime":"0800","fcstValue":"0","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"PTY","fcstDate":"20230630","fcstTime":"0900","fcstValue":"0","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"PTY","fcstDate":"20230630","fcstTime":"1000","fcstValue":"0","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"PTY","fcstDate":"20230630","fcstTime":"1100","fcstValue":"0","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"PTY","fcstDate":"20230630","fcstTime":"1200","fcstValue":"0","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"RN1","fcstDate":"20230630","fcstTime":"0700","fcstValue":"강수없음","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"RN1","fcstDate":"20230630","fcstTime":"0800","fcstValue":"강수없음","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"RN1","fcstDate":"20230630","fcstTime":"0900","fcstValue":"강수없음","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"RN1","fcstDate":"20230630","fcstTime":"1000","fcstValue":"강수없음","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"RN1","fcstDate":"20230630","fcstTime":"1100","fcstValue":"강수없음","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"RN1","fcstDate":"20230630","fcstTime":"1200","fcstValue":"강수없음","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"SKY","fcstDate":"20230630","fcstTime":"0700","fcstValue":"4","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"SKY","fcstDate":"20230630","fcstTime":"0800","fcstValue":"4","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"SKY","fcstDate":"20230630","fcstTime":"0900","fcstValue":"3","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"SKY","fcstDate":"20230630","fcstTime":"1000","fcstValue":"1","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"SKY","fcstDate":"20230630","fcstTime":"1100","fcstValue":"1","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"SKY","fcstDate":"20230630","fcstTime":"1200","fcstValue":"1","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"T1H","fcstDate":"20230630","fcstTime":"0700","fcstValue":"24","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"T1H","fcstDate":"20230630","fcstTime":"0800","fcstValue":"25","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"T1H","fcstDate":"20230630","fcstTime":"0900","fcstValue":"25","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"T1H","fcstDate":"20230630","fcstTime":"1000","fcstValue":"25","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"T1H","fcstDate":"20230630","fcstTime":"1100","fcstValue":"26","nx":61,"ny":126},{"baseDate":"20230630","baseTime":"0630","category":"T1H","fcstDate":"20230630","fcstTime":"1200","fcstValue":"27","nx":61,"ny":126}]},"pageNo":1,"numOfRows":30,"totalCount":60}}}
    
    sky_description, pty_f, temp = data_parse(data_w) # sky_description은 날씨 정보  text라서 나중에 랜더링 시켜서 안드로이드 화면에 띄우면 됨
    # pty_f,temp에 1번 인덱스는 강수형태 string 이것도 화면에 넘겨야 
    return sky_description, pty_f, temp


# 프론트로 안가져와도됨
def read_drink_data(file_path):
    drink_data = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            drink_data.append(row)
    return drink_data

# 프론트로 가져와야됨
def recommend_drinks(drink_type, drink_data):
    recommended_drinks = []
    for drink in drink_data:
        if drink['주류'] == drink_type:
            recommended_drinks.append(drink)
    return recommended_drinks
# 프론트로 가져와야됨

def recom_weather(t1h, pty):

    # CSV 파일 경로
    file_path = 'alcohol_df_1.csv'

    temperature = float(t1h)    

    if 6 <= temperature <= 10:
        temperature_recommendation = "소주"
    elif 0 <= temperature <= 5:
        temperature_recommendation = "위스키, 꼬냑"
    elif temperature >= 25:
        temperature_recommendation = "맥주"
    elif 10 <= temperature <= 24:
        temperature_recommendation = "전통주"
    elif temperature < 0:
        temperature_recommendation = "와인"
    else:
        temperature_recommendation = "추천 주종이 없습니다."

    # 비/눈 여부에 따라 추가적인 주류 추천
    if pty in ['1', '4', '5']:
        precipitation_recommendation = "전통주"  # 비, 소나기, 빗방울일 때 전통주를 추가 추천
    elif pty in ['3', '7']:
        precipitation_recommendation = "와인"  # 눈, 눈날림일 때 와인을 추가 추천
    else:
        precipitation_recommendation = None

    recommendation = []
    if temperature_recommendation:
        recommendation.append(temperature_recommendation)
    if precipitation_recommendation:
        recommendation.append(precipitation_recommendation)

    if recommendation:
        recommendation = ", ".join(recommendation)
    else:
        recommendation = "추천 주종이 없습니다."

    print("추천 주종:", recommendation)

    # 음료 데이터 읽어오기
    drink_data = read_drink_data(file_path)

    # 예시: 추천 음료가 나왔을 때 해당 주종에 해당되는 주류명 추천
    if temperature_recommendation == '맥주':
        drink_type = '맥주'
    elif temperature_recommendation == '와인':
        drink_type = '와인'
    elif temperature_recommendation == '소주':
        drink_type = '소주'
    elif temperature_recommendation == '위스키':
        drink_type = '위스키'
    elif temperature_recommendation == '전통주':
        drink_type = '전통주'
    else:
        print('추천 음료가 없습니다.')

    temp_drink = [] # 추천 주류 정보 랜덤하게 3개 정보 넣는곳
    if drink_type:
        recommended_drinks = recommend_drinks(drink_type, drink_data)
        if recommended_drinks:
            random.shuffle(recommended_drinks)
            recommended_drinks = recommended_drinks[:3]
            for drink in recommended_drinks:
                print('추천 주류 정보:')
                for key, value in drink.items():
                    if key not in ['id', '용량'] and value:
                        # temp_dict = {}
                        # temp_dict[key] = value
                        temp = f"{key} : {value}"
                        temp_drink.append(temp)
                        print(f'{key}: {value}')
                        
                print()
        else:
            print('해당 주종에 대한 추천 주류가 없습니다.')

    if precipitation_recommendation == '전통주':
        drink_type = '전통주'
    elif precipitation_recommendation == '와인':
        drink_type = '와인'
    else:
        drink_type = None

    pty_drink = []
    if drink_type:
        recommended_drinks = recommend_drinks(drink_type, drink_data)
        if recommended_drinks:
            random.shuffle(recommended_drinks)
            recommended_drinks = recommended_drinks[:3]
            for drink in recommended_drinks:
                print('추천 주류 정보:')
                for key, value in drink.items():
                    if key not in ['id', '용량'] and value:
                        # temp_dict = {}
                        # temp_dict[key] = value
                        temp = f"{key} {value}"
                        pty_drink.append(temp)
                        print(f'{key}: {value}')
                print()
        else:
            print('해당 주종에 대한 추천 주류가 없습니다.')



    print(recommendation)
    print(t1h)
    print(pty)
    return recommendation, temp_drink, pty_drink

# sky_description, pty, t1h = get_loc("강남구")
# recommendation = recom_weather(t1h, pty)
# print(sky_description)
# print(recommendation)
# print(t1h)
# print(pty)