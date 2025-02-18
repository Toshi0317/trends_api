from fastapi import FastAPI
from pytrends.request import TrendReq

app = FastAPI()

@app.get("/get_trends")
def get_trends(keyword: str):
    pytrends = TrendReq(hl='ja-JP', tz=540)
    kw_list = [keyword]
    pytrends.build_payload(kw_list, timeframe='now 1-H', geo='JP')

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