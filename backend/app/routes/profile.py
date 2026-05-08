import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, UserPreferences, LikedSongs, RecommendationHistory, SpotifySong
from app.schemas import (
    UserPreferencesSchema,
    UserPreferencesResponse,
    LikedSongResponse,
    RecommendationHistoryResponse,
    SongResponse
)
from app.utils import get_current_user

router = APIRouter()


@router.get("/preferences", response_model=UserPreferencesResponse)
def get_user_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's language and genre preferences."""
    preferences = db.query(UserPreferences).filter(
        UserPreferences.user_id == current_user.id
    ).first()

    if not preferences:
        # Create default preferences if not exists
        preferences = UserPreferences(user_id=current_user.id)
        db.add(preferences)
        db.commit()
        db.refresh(preferences)

    # Parse JSON fields
    result = {
        "id": preferences.id,
        "user_id": preferences.user_id,
        "preferred_languages": json.loads(preferences.preferred_languages) if preferences.preferred_languages else [],
        "preferred_genres": json.loads(preferences.preferred_genres) if preferences.preferred_genres else [],
        "updated_at": preferences.updated_at
    }

    return result


@router.post("/preferences", response_model=UserPreferencesResponse)
def update_user_preferences(
    preferences_data: UserPreferencesSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user's language and genre preferences."""
    preferences = db.query(UserPreferences).filter(
        UserPreferences.user_id == current_user.id
    ).first()

    if not preferences:
        preferences = UserPreferences(user_id=current_user.id)
        db.add(preferences)

    if preferences_data.preferred_languages is not None:
        preferences.preferred_languages = json.dumps(preferences_data.preferred_languages)
    if preferences_data.preferred_genres is not None:
        preferences.preferred_genres = json.dumps(preferences_data.preferred_genres)

    db.commit()
    db.refresh(preferences)

    # Parse JSON fields
    result = {
        "id": preferences.id,
        "user_id": preferences.user_id,
        "preferred_languages": json.loads(preferences.preferred_languages) if preferences.preferred_languages else [],
        "preferred_genres": json.loads(preferences.preferred_genres) if preferences.preferred_genres else [],
        "updated_at": preferences.updated_at
    }

    return result


@router.get("/liked-songs", response_model=list[LikedSongResponse])
def get_liked_songs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's liked songs."""
    liked_songs = db.query(LikedSongs).filter(
        LikedSongs.user_id == current_user.id
    ).order_by(LikedSongs.liked_at.desc()).all()

    return liked_songs


@router.post("/liked-songs/{song_id}")
def like_song(
    song_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Like a song (add to favorites)."""
    # Check if song exists
    song = db.query(SpotifySong).filter(SpotifySong.id == song_id).first()
    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Song not found"
        )

    # Check if already liked
    existing = db.query(LikedSongs).filter(
        LikedSongs.user_id == current_user.id,
        LikedSongs.song_id == song_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Song already liked"
        )

    # Add to liked songs
    liked = LikedSongs(user_id=current_user.id, song_id=song_id)
    db.add(liked)
    db.commit()
    db.refresh(liked)

    return {"status": "success", "message": "Song liked successfully"}


@router.delete("/liked-songs/{song_id}")
def unlike_song(
    song_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Unlike a song (remove from favorites)."""
    liked = db.query(LikedSongs).filter(
        LikedSongs.user_id == current_user.id,
        LikedSongs.song_id == song_id
    ).first()

    if not liked:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Liked song record not found"
        )

    db.delete(liked)
    db.commit()

    return {"status": "success", "message": "Song unliked successfully"}


@router.get("/history", response_model=list[RecommendationHistoryResponse])
def get_recommendation_history(
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's recommendation search history."""
    history = db.query(RecommendationHistory).filter(
        RecommendationHistory.user_id == current_user.id
    ).order_by(RecommendationHistory.query_timestamp.desc()).limit(limit).all()

    # Parse JSON fields
    result = []
    for record in history:
        result.append({
            "id": record.id,
            "user_id": record.user_id,
            "moods_queried": json.loads(record.moods_queried) if record.moods_queried else [],
            "filters_applied": json.loads(record.filters_applied) if record.filters_applied else None,
            "results_count": record.results_count,
            "query_timestamp": record.query_timestamp
        })

    return result
