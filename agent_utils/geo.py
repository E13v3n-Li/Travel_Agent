# 城市获取经纬度
from dotenv import load_dotenv
import os
from agent_utils.make_request import make_req

load_dotenv()

api_key = os.getenv("weather_api_key")
api_host = os.getenv("weather_api_host")

def city_2_location(city:str):

    if not api_key or not api_host:
        print("error: 未配置weather_api_key or weather_api_host")
        return None

    headers = {"X-QW-Api-Key":api_key}
    params = {"location":city}
    url = f"https://{api_host}/geo/v2/city/lookup"
    res = make_req(url, "GET", params=params, headers=headers)

    if res is None:
        print("请求失败：res 为 None")
        return None

    try:

        if res.status_code == 200:
            data = res.json()
            #print(data)
            if data.get("location"):
                loc = data["location"][0]
                return {
                    "id": loc["id"],
                    "name": loc["name"],
                    "lat": loc["lat"],
                    "lon": loc["lon"],
                }

            return f"未找到城市: {city}"
        return f"请求失败，状态码: {res.status_code}"

    except Exception as e:

        return f"geo请求异常: {e}"