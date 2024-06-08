from pydantic import BaseModel


class VideoBase(BaseModel):
    name: str
    path: str
    size: float
    format: str


class VideoCreate(VideoBase):
    pass


class Video(VideoBase):
    id: int

    class Config:
        orm_mode = True
