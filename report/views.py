import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
# from pymysql import render
from django.shortcuts import render
import pymysql
from PIL import Image
import os

def index(request):
    # MySQL 데이터베이스 연결
    #conn = pymysql.connect(host="team4rds.cpa0spimmjj8.us-east-2.rds.amazonaws.com", port=3306, 
    #                       user='admin', passwd='team4123', db='team4rds', charset='utf8')
    cur = conn.cursor()

    # 쿼리 실행
    query =  "SELECT * FROM team4rds.frige_log;"
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
    if (len(drink_totals) > 0):

        # 막대 그래프 생성
        plt.bar(drink_totals.index, drink_totals.values)
        plt.xlabel('술')
        plt.ylabel('합산된 개수')
        plt.title('최근 일주일간 주류 리포트')

        # Y축 눈금 설정
        plt.yticks(range(int(min(drink_totals.values)), int(max(drink_totals.values))+1))

        # 그래프 출력
        plt.tight_layout()
        plt.show()
        reportgraph = plt.to_html()
    else:
        reportgraph =  ""
        print("데이터가 부족합니다.")

    return render(request, 'report/drink_report.html', {'report':reportgraph})