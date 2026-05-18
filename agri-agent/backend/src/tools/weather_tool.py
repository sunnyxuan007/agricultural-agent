import httpx
import yaml
from langchain_core.tools import tool


def load_weather_key():
    """从配置文件读取高德天气 API Key"""
    try:
        with open("config/settings.yaml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        return config.get("apis", {}).get("weather", {}).get("key", "")
    except:
        return ""


@tool
def get_weather(city: str) -> str:
    """
    根据城市名称获取当前天气和未来3天预报。
    优先使用高德 API，若无 Key 或请求失败则返回模拟数据。
    """
    key = load_weather_key()

    if key:
        try:
            # 高德天气 API 需要城市 adcode，但也可以直接传中文城市名（高德会自动匹配）
            url = "https://restapi.amap.com/v3/weather/weatherInfo"
            params = {
                "key": key,
                "city": city,
                "extensions": "all",  # all 返回预报天气
                "output": "JSON"
            }
            resp = httpx.get(url, params=params, timeout=10)
            data = resp.json()

            # 打印完整响应（便于调试，正式环境可移除）
            print(f"高德 API 响应: {data}")

            if data.get("status") == "1":
                forecasts = data.get("forecasts", [])
                if not forecasts:
                    return f"未获取到 {city} 的天气预报数据，请检查城市名称是否正确。"
                casts = forecasts[0].get("casts", [])
                if not casts:
                    return f"{city} 未来几天的预报数据为空。"
                today = casts[0]
                report = (
                    f"{city}今日天气：{today['dayweather']}，"
                    f"温度 {today['nighttemp']}~{today['daytemp']}℃，"
                    f"风力 {today['daywind']} {today['daypower']}级"
                )
                if "雨" in today['dayweather'] or "雪" in today['dayweather']:
                    report += "。请注意田间排水，防范渍害。"
                return report
            else:
                return f"高德 API 返回错误：{data.get('info', '未知错误')}"
        except Exception as e:
            print(f"高德天气请求失败：{e}，将使用模拟数据")
            # 继续执行模拟数据逻辑
        # 如果真实 API 失败，降级到模拟数据
        return f"{city}未来三天有阴雨天气，建议做好排水准备。"
    else:
        # 无 API Key 时也返回模拟数据
        return f"{city}未来三天有阴雨天气，建议做好排水准备。"