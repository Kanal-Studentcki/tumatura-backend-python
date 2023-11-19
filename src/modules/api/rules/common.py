from pydantic import BaseModel


class RequestModel(BaseModel):
    class Config:
        populate_by_name = True
