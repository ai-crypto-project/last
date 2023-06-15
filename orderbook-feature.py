import requests
import pandas as pd

# Bithumb API 요청
url = "https://api.bithumb.com/public/transaction_history/BTC"
params = {
    "count": 100,
    "page": 1
}

all_transactions = []
page = 1
while True:
    params["page"] = page
    response = requests.get(url, params=params)
    data = response.json()
    
    if data["status"] != "0000":
        print("API 요청에 실패하였습니다.")
        break
    
    transactions = data["data"]
    if not transactions:
        # 더 이상 데이터가 없는 경우 종료
        break
    
    all_transactions.extend(transactions)
    page += 1

# 데이터가 있는 경우에만 처리
if all_transactions:
    # 데이터프레임 생성
    df = pd.DataFrame(all_transactions)

    # 4월 29일의 데이터만 필터링
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    df = df[df["transaction_date"].dt.date == pd.to_datetime("2023-04-29").date()]

    # CSV 파일로 저장
    df.to_csv("AA.csv", index=False)
    print("데이터를 저장하였습니다.")
else:
    print("데이터가 없습니다.")
