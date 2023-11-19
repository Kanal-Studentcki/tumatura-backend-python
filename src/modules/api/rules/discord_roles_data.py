from src.modules.api.rules.common import RequestModel


class WPItemData(RequestModel):
    product_id: int


class WPOrderUpdateData(RequestModel):
    status: str
    customer_id: int
    line_items: list[WPItemData]
