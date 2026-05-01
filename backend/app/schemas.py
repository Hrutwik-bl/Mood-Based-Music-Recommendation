from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    email: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class SongResponse(BaseModel):
    id: int
    spotify_id: str
    name: str
    artist: str
    language: str
    moods: str
    album_art_url: Optional[str]
    preview_url: Optional[str]
    youtube_url: Optional[str]
    danceability: Optional[float]
    energy: Optional[float]
    valence: Optional[float]
    acousticness: Optional[float]
    tempo: Optional[float]

    class Config:
        from_attributes = True


class RecommendationRequest(BaseModel):
    moods: List[str]
    language: Optional[str] = None
    artist: Optional[str] = None
    limit: int = 10


class RecommendationResponse(BaseModel):
    songs: List[SongResponse]
    total_results: int


class MoodResponse(BaseModel):
    mood: str
    description: Optional[str] = None


class ArtistResponse(BaseModel):
    artist: str
    song_count: int


class LanguageResponse(BaseModel):
    language: str
    song_count: int
