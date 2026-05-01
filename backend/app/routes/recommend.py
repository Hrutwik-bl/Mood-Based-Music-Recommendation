from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, SpotifySong
from app.schemas import RecommendationRequest, RecommendationResponse, SongResponse
from app.utils import get_current_user
from app.ml_model import MusicRecommendationModel

router = APIRouter()
recommendation_model = MusicRecommendationModel()


@router.post("/", response_model=RecommendationResponse)
def get_recommendations(
    request: RecommendationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get song recommendations based on moods."""
    if recommendation_model.model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ML model not initialized. Please run 'python load_data.py' to populate data and train the model."
        )

    # Get recommendations from ML model
    recommendations = recommendation_model.recommend(
        moods=request.moods,
        db=db,
        limit=request.limit * 2  # Get extra to filter by language/artist
    )

    if not recommendations:
        return RecommendationResponse(songs=[], total_results=0)

    # Fetch songs from database
    song_ids = [rec[0] for rec in recommendations]
    songs = db.query(SpotifySong).filter(SpotifySong.id.in_(song_ids)).all()

    # Create a mapping for quick lookup
    song_map = {song.id: song for song in songs}

    # Filter by language and artist if specified
    filtered_songs = []
    for song_id, score in recommendations:
        song = song_map.get(song_id)
        if not song:
            continue

        if request.language and song.language != request.language:
            continue
        if request.artist and request.artist.lower() not in song.artist.lower():
            continue

        filtered_songs.append(song)

        if len(filtered_songs) >= request.limit:
            break

    # Convert to response schema
    song_responses = [SongResponse.model_validate(song) for song in filtered_songs]

    return RecommendationResponse(
        songs=song_responses,
        total_results=len(song_responses)
    )
