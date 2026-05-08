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
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]

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


class UserPreferencesSchema(BaseModel):
    preferred_languages: Optional[List[str]] = None
    preferred_genres: Optional[List[str]] = None

    class Config:
        from_attributes = True


class UserPreferencesResponse(BaseModel):
    id: int
    user_id: int
    preferred_languages: Optional[List[str]]
    preferred_genres: Optional[List[str]]
    updated_at: datetime

    class Config:
        from_attributes = True


class LikedSongResponse(BaseModel):
    id: int
    user_id: int
    song_id: int
    liked_at: datetime
    song: Optional[SongResponse] = None

    class Config:
        from_attributes = True


class RecommendationHistoryResponse(BaseModel):
    id: int
    user_id: int
    moods_queried: List[str]
    filters_applied: Optional[dict] = None
    results_count: Optional[int]
    query_timestamp: datetime

    class Config:
        from_attributes = True
