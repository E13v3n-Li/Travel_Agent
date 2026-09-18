from langchain_core.tools import tool
from dotenv import load_dotenv
import httpx
import os
from agent_utils.geo import city_2_location
from agent_utils.make_request import make_req

load_dotenv()

weather_api_key = os.getenv("weather_api_key")
weather_api_host = os.getenv("weather_api_host")

@tool
def get_weather(city:str, days:int):
    """查询指定城市未来几天的天气预报。
    Args:
        city: 城市名称，如"北京"、"上海"
        days: 预报天数，1-10，默认 10
    """
    loc = city_2_location(city)
    headers = {"X-QW-Api-Key":weather_api_key}
    params = {"days":days, "localTime": "true"}  # 查询未来几天的天气
    url = f"https://{weather_api_host}/weather/v1/daily/{loc['lat']}/{loc['lon']}"


    res = make_req(url, "GET", params=params, headers=headers)


    if res is None:
        print("请求失败：res 为 None")
        return None

    try:
        if res.status_code == 200:
            data = res.json()
            day_weather = process_data(city,days,data)
            #print(data)
            return day_weather
        else:
            print(f"无法访问天气，错误码: {res.status_code}")
    except Exception as e:
        return f"weather请求异常: {e}"



def process_data(city, days, data):
    days_data = data.get("days", [])
    if not days_data:
        print(f"{city} 暂无天气预报")
        return None

    print(f"{city} 未来 {days} 天的天气")
    lines = []

    for d in days_data:
        date = d["forecastStartTime"][:10]  #取天气的日期
        t_max = d["temperatureMax"]["value"]
        t_min = d["temperatureMin"]["value"]
        day_text = d["daytime"]["condition"]["text"]
        night_text = d["nighttime"]["condition"]["text"]
        rain_prob = d["daytime"]["precipitation"]["probability"]

        lines.append(
            f"{date} 白天{day_text}，夜间{night_text}，全天气温{t_min:.0f} ~{t_max:.0f}℃，降水概率 {rain_prob:.0%}"
        )
    return "\n".join(lines)
# if __name__ == "__main__":
#     get_weather("沈阳", 3)