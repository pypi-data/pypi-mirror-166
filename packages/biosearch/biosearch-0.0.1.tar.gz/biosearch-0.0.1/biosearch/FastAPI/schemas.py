from datetime import datetime
from typing import Union

from pydantic import BaseModel


class PersonSerializer(BaseModel):
    id : int
    first_name : str
    last_name : str
    age : int
    gender : str
    nationality : str
    hasWatch : bool

    class Config:
        orm_mode = True

class PresentationSerializer(BaseModel):
    presentation_id : int
    presentation_link : str
    club_name : str
    revision_id : str
    created_at : datetime
    updated_at : datetime

    class Config:
        orm_mode = True

class SlideSerializer(BaseModel):
    slide_id : int
    slide_link : str
    presentation_id :int
    created_at : datetime
    updated_at : datetime

    class Config:
        orm_mode = True

class TextboxSerializer(BaseModel):
    textbox_id : int
    textbox_link : str
    slide_id : int
    text : str
    created_at : datetime
    updated_at : datetime

    class Config:
        orm_mode = True
