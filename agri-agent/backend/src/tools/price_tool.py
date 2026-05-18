from langchain_core.tools import tool

@tool
def get_agricultural_price(product: str) -> str:
    """
    查询农产品批发价格（元/公斤）。
    无真实API时返回模拟数据。
    """
    # 简单模拟数据
    mock_prices = {
        "玉米": 2.6,
        "小麦": 2.4,
        "水稻": 3.0,
        "大豆": 4.5,
        "西红柿": 3.5,
        "黄瓜": 2.8,
        "苹果": 5.2,
    }
    price = mock_prices.get(product, 2.8)
    return f"{product}当前全国批发均价约{price}元/公斤，较昨日持平。"