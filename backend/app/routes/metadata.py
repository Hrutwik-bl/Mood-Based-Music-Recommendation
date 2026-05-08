from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import distinct, func
from app.database import get_db
from app.models import SpotifySong, MoodMapping, User
from app.schemas import MoodResponse, ArtistResponse, LanguageResponse
from app.utils import get_current_user

router = APIRouter()

# Language code to full name mapping
LANGUAGE_MAP = {
    "en": "English",
    "kn": "Kannada",
    "hi": "Hindi",
    "te": "Telugu",
    "ta": "Tamil",
    "ml": "Malayalam",
    "gu": "Gujarati",
    "or": "Odia",
    "ne": "Nepali",
    "ur": "Urdu",
    "kok": "Konkani",
    "bn": "Bengali",
    "pa": "Punjabi",
    "sa": "Sanskrit",
    "mr": "Marathi",
    "fr": "French",
    "es": "Spanish",
}

# Default moods
DEFAULT_MOODS = [
    {"mood": "happy", "description": "Uplifting and joyful music"},
    {"mood": "sad", "description": "Emotional and melancholic music"},
    {"mood": "energetic", "description": "Powerful and motivating music"},
    {"mood": "chill", "description": "Relaxing and calm music"},
    {"mood": "focused", "description": "Concentrating and productive music"},
    {"mood": "romantic", "description": "Lovely and intimate music"},
    {"mood": "party", "description": "Danceable and fun music"},
]


@router.get("/moods", response_model=list[MoodResponse])
def get_moods(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get list of available moods."""
    return DEFAULT_MOODS


@router.get("/languages", response_model=list[LanguageResponse])
def get_languages(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get list of available languages in the music dataset."""
    languages = db.query(
        SpotifySong.language,
        func.count(SpotifySong.id).label("song_count")
    ).group_by(SpotifySong.language).order_by(SpotifySong.language).all()

    if not languages:
        return []

    result = []
    for lang_code, song_count in languages:
        lang_name = LANGUAGE_MAP.get(lang_code, lang_code)
        result.append(LanguageResponse(language=lang_name, song_count=song_count))

    return sorted(result, key=lambda x: x.language)


@router.get("/artists", response_model=list[ArtistResponse])
def get_artists(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get list of available artists in the music dataset."""
    artists = db.query(
        SpotifySong.artist,
        func.count(SpotifySong.id).label("song_count")
    ).group_by(SpotifySong.artist).order_by(func.count(SpotifySong.id).desc()).limit(100).all()

    if not artists:
        return []

    return [
        ArtistResponse(artist=artist[0], song_count=artist[1])
        for artist in artists
    ]
