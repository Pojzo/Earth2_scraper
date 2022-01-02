import dataclasses


@dataclasses.dataclass
class Property:
    deed: str
    owned_by: str
    land_title: str
    land_class: int
    tier: int
    tiles: int
    location: str
    controlled_by: str
    purchased_for: float
    new_land_value: float
    current_market_value: float
    buy_now_for: float
