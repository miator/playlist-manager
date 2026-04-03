from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SongCreate(BaseModel):
    title: str = Field(min_length=1)
    artist: str = Field(min_length=1)
    duration: int = Field(gt=0)
    genre: str = Field(min_length=1)
    playlist_name: str = Field(min_length=1)


class SongUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    artist: Optional[str] = Field(default=None, min_length=1)
    duration: Optional[int] = Field(default=None, gt=0)
    genre: Optional[str] = Field(default=None, min_length=1)
    playlist_name: Optional[str] = Field(default=None, min_length=1)


class SongRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    artist: str
    duration: int
    genre: str
    playlist_name: str
