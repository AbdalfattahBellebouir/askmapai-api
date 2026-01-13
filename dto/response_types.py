from typing import List
from models.location import Location
from pydantic import BaseModel

class AskMapAIResponse(BaseModel):
    locations: List[Location]
    answer: str