import time
import openai
from fastapi import FastAPI
from pytrends.request import TrendReq

import os  # 環境変数を使うために追加

API_KEY = os.getenv("OPENAI_API_KEY")  # 環境変数からAPIキーを取得

app = FastAPI()

@app.get("/get_trends")
def get_trends(keyword: str):
    pytrends = TrendReq(hl='ja-JP', tz=540)
    kw_list = [keyword]

    for _ in range(3):
        try:
            pytrends.build_payload(kw_list, timeframe='now 1-H', geo='JP')
            time.sleep(30)  # 30秒待機（Googleのブロック回避）

            data = pytrends.interest_over_time()
            if data.empty:
                return {"error": "Google Trendsのデータが取得できませんでした"}

            latest_data = data.tail(1).to_dict()
            trends_dict = {
                "keyword": keyword,
                "trend_data": [
                    {"date": str(data.index[0]), "interest": int(data[keyword].values[0])}
                ]
            }
            return trends_dict
        except Exception as e:
            print(f"エラー発生: {e}")
            time.sleep(30)  # 30秒待機してリトライ

    return {"error": "Google Trends APIのリクエスト上限に達しました。時間を置いて再試行してください。"}