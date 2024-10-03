from pydantic import BaseModel
from typing import List,Optional
from typing_extensions import TypedDict

class UploadImageSchema(BaseModel):
    road_image: str
    latitude: str
    longitude: str

    class Config:
        from_attributes = True