from pydantic import BaseModel

class Location(BaseModel):
    orderNum: int
    lat: float
    lng: float
    name: str
    info: str