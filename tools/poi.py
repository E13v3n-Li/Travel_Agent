# use gaode map to find landscape
# 使用高德地图api
from langchain_core.tools import tool
from dotenv import load_dotenv
import os
from agent_utils.make_request import make_req

load_dotenv()

api_key = os.getenv("gaode_map_api_key")

@tool
def search_attraction(city, keywords="景点"):
    """在指定城市搜索景点、美食或酒店等兴趣点。

    Args:
        city: 城市名称，如"北京"、"成都"
        keywords: 搜索关键词，如"历史景点"、"美食"
    """
    url = "https://restapi.amap.com/v3/place/text"
    params = {"key":api_key, "keywords":keywords, "city":city, "offset":20, "page":1, "extensions":"all"}
    res = make_req(url, "GET", params=params)

    if res is None:
        print("请求失败: res is None")
        return None

    try:
        if res.status_code == 200:
            data = res.json()
            if data.get("status") == "0":
                print(f"请求失败：{data.get('info')}")

            pois = data.get("pois", [])
            if not pois:
                print(f"未在{city}找到与{keywords}相关的地点")

            lines = []
            for poi in pois:
                name = poi.get("name", "未知")
                address = poi.get("address", "")
                rating = poi.get("biz_ext", {}).get("rating", "")
                cost = poi.get("biz_ext", {}).get("cost")
                type_name = poi.get("type","")

                line = f"· {name} （{type_name}）"
                if rating:
                    line += f"  评分: {rating}"
                if cost:
                    line += f"  人均: {cost}元"
                if address:
                    line += f"  地址: {address}"
                lines.append(line)

        return "\n".join(lines)  
            
    except Exception as e:
        return f"景点搜索异常: {e}"