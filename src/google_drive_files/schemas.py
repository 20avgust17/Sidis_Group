from pydantic import BaseModel


class File(BaseModel):
    id: str
    title: str
