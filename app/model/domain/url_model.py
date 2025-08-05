# model/domain/base_model.py
from datetime import date, datetime
from typing import Optional


class UrlModel:
    def __init__(
        self, original_url: str, expires_at: datetime, short_code:str,  visits: Optional[int] = 0
    ):
        self.id: int
        self.short_code: str = short_code
        self.original_url: str = original_url
        self.created_at: datetime = datetime.now()
        self.expires_at: datetime = expires_at
        self.visits: int = visits

    def dump(self):
        return self.__dict__

    def __str__(self):
        return f"id={self.id}, short_code={self.short_code} original_url={self.original_url}"