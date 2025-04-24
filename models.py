from pydantic import BaseModel

class Outlet(BaseModel):
    name: str
    latitude: float
    longitude: float
    address: str
    telephone: str
    waze_link: str
    has_birthday_party: bool
    has_breakfast: bool
    has_cashless_facility: bool
    has_mccafe: bool
    has_mcdelivery: bool
    has_wifi: bool
    has_digital_kiosk: bool
    has_ev_charging: bool
    operating_hours: str
