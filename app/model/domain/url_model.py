# model/domain/base_model.py
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

@dataclass
class UrlModel:
    id:Optional[int] = None
    short_code:str
    original_url:str
    created_at:datetime
    expires_at:datetime
    visits:int

    def dump(self):
        return self.__dict__