# 使用高德地图去规划出行路线
from langchain_core.tools import tool
from dotenv import load_dotenv
import os
from agent_utils.make_request import make_req

load_dotenv()
api_key = os.getenv("gaode_map_api_key")


@tool
def go_plan(ori: str, dest: str, mode: str = "walking", city: str = "") -> str:
    """规划同一城市内两点之间的出行路线，支持步行、驾车、骑行、公交。

    Args:
        ori: 起点经纬度，格式为"经度,纬度"
        dest: 终点经纬度，格式为"经度,纬度"
        mode: 出行方式，可选 walking / driving / bicycling / transit
        city: 城市名称（公交模式必填，例如"北京"）
    """
    if mode == "transit":
        if not city:
            return "公交规划需要提供城市名（city 参数）"
        url = "https://restapi.amap.com/v3/direction/transit/integrated"
        params = {"key": api_key, "origin": ori, "destination": dest, "city": city}
    else:
        url = f"https://restapi.amap.com/v3/direction/{mode}"
        params = {"key": api_key, "origin": ori, "destination": dest}

    res = make_req(url, "GET", params=params)
    if res is None:                     
        return "请求失败：res 为 None"

    try:
        if res.status_code != 200:
            return f"请求失败，状态码: {res.status_code}"

        data = res.json()          
        if data.get("status") != "1":     # 高德：status == "1" 才成功
            return f"规划失败：{data.get('info')}"

        if mode == "transit":
            transits = data.get("route", {}).get("transits", [])
            if not transits:
                return "未找到公交方案"

            lines = ["公交方案："]
            for i, t in enumerate(transits[:3], 1):
                cost = t.get("cost", "")
                duration = int(t.get("duration") or 0)
                lines.append(f"方案{i}：耗时{duration // 60}分钟，票价{cost}元")
            return "\n".join(lines)

        paths = data.get("route", {}).get("paths", [])
        if not paths:
            return "未找到路线方案"

        path = paths[0]
        distance = path.get("distance", "0")
        duration = int(path.get("duration") or 0)
        lines = [
            "路线方案：",
            f"总距离：{distance}米",
            f"预计耗时：{duration // 60}分钟",
            "途经路段：",
        ]
        for step in path.get("steps", []):
            instruction = step.get("instruction", "")
            step_dist = step.get("distance", "")
            if instruction:
                lines.append(f"  · {instruction}（{step_dist}米）")
        return "\n".join(lines)

    except Exception as e:
        return f"规划异常: {e}"