import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import io
import base64
from django.shortcuts import render
import pymysql
from matplotlib import font_manager as fm

# 한글 폰트 경로 설정
# /usr/share/fonts/nanum/NanumGothicExtraBold.ttf: NanumGothic,나눔고딕,NanumGothicExtraBold,나눔고딕 ExtraBold:style=ExtraBold,Regular,Bold
font_path = '/usr/share/fonts/nanum/NanumGothic.ttf'

# 폰트 매니저에 폰트 추가
fm.fontManager.addfont(font_path)

# 폰트 설정 변경
plt.rcParams['font.family'] = 'NanumGothic'

# 한글 폰트 깨짐 문제 해결
plt.rcParams['axes.unicode_minus'] = False

def index(request):
    # MySQL 데이터베이스 연결
    conn = pymysql.connect(host="team4-db.cpa0spimmjj8.us-east-2.rds.amazonaws.com", port=3306, 
                           user='admin', passwd='team4qwer', db='masterDB', charset='utf8')
    
    cur = conn.cursor()

    # 쿼리 실행
    query =  "SELECT * FROM masterDB.frige_log;"
    cur.execute(query)
    rows = cur.fetchall()

    # 결과 처리
    drinkname = []
    quantity = []
    created_at = []

    for row in rows:
        drinkname.append(row[2])
        quantity.append(row[3])
        created_at.append(row[4])

    # 연결 및 커서 닫기
    cur.close()
    conn.close()

    # 데이터프레임 생성
    df = pd.DataFrame({
        'created_at': created_at,
        'drinkname' : drinkname,
        'quantity': quantity
    })

    # created_at 열을 datetime 형식으로 변환
    df['created_at'] = pd.to_datetime(df['created_at'])

    # 최근 일주일 동안의 데이터 필터링
    end_date = datetime.now()
    start_date = end_date - timedelta(days=6)
    filtered_df = df[(df['created_at'] >= start_date) & (df['created_at'] <= end_date)]

    # drinkname 별로 quantity 합산
    drink_totals = filtered_df.groupby('drinkname')['quantity'].sum()

    # 막대 그래프 생성
    plt.bar(drink_totals.index, drink_totals.values)
    plt.xlabel('술')
    plt.ylabel('합산된 개수')
    plt.title('일주일간 주류 리포트')

    # Y축 눈금 설정
    plt.yticks(range(int(min(drink_totals.values)), int(max(drink_totals.values))+1))

    # 그래프를 이미지로 저장
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # 이미지를 base64로 인코딩하여 HTML에 포함시키기
    graph = base64.b64encode(image_png).decode('utf-8')
    reportgraph = 'data:image/png;base64,{}'.format(graph)

    return render(request, 'report/drink_report.html', {'report': reportgraph})
