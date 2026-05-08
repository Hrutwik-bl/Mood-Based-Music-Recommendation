from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import json
from app.database import get_db
from app.models import User, SpotifySong, RecommendationHistory
from app.schemas import RecommendationRequest, RecommendationResponse, SongResponse
from app.utils import get_current_user
from app.ml_model import MusicRecommendationModel

router = APIRouter()
recommendation_model = MusicRecommendationModel()

# Language name to code mapping
LANGUAGE_NAME_TO_CODE = {
    "English": "en",
    "Kannada": "kn",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Malayalam": "ml",
    "Gujarati": "gu",
    "Odia": "or",
    "Nepali": "ne",
    "Urdu": "ur",
    "Konkani": "kok",
    "Bengali": "bn",
    "Punjabi": "pa",
    "Sanskrit": "sa",
    "Marathi": "mr",
    "French": "fr",
    "Spanish": "es",
}


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
        limit=request.limit * 3  # Get extra to filter by mood/language/artist
    )

    if not recommendations:
        return RecommendationResponse(songs=[], total_results=0)

    # Fetch songs from database
    song_ids = [rec[0] for rec in recommendations]
    songs = db.query(SpotifySong).filter(SpotifySong.id.in_(song_ids)).all()

    # Filter by moods - only keep songs that have at least one requested mood
    mood_filtered_recommendations = []
    song_map_temp = {song.id: song for song in songs}
    for song_id, score in recommendations:
        song = song_map_temp.get(song_id)
        if song:
            song_moods = json.loads(song.moods)
            # Check if any of the requested moods match
            if any(mood.lower() in [m.lower() for m in song_moods] for mood in request.moods):
                mood_filtered_recommendations.append((song_id, score))

    recommendations = mood_filtered_recommendations
    if not recommendations:
        return RecommendationResponse(songs=[], total_results=0)

    # Re-fetch the mood-filtered songs
    song_ids = [rec[0] for rec in recommendations]
    songs = db.query(SpotifySong).filter(SpotifySong.id.in_(song_ids)).all()

    # Create a mapping for quick lookup
    song_map = {song.id: song for song in songs}

    # Filter by language and artist if specified
    filtered_songs = []

    # Convert language name to code
    language_filter = None
    if request.language:
        language_filter = LANGUAGE_NAME_TO_CODE.get(request.language, request.language)

    # Apply filters in order of priority
    for song_id, score in recommendations:
        song = song_map.get(song_id)
        if not song:
            continue

        # Language filter (always applied if specified)
        if language_filter and song.language != language_filter:
            continue

        # Artist filter (always applied if specified)
        if request.artist and request.artist.lower() not in song.artist.lower():
            continue

        filtered_songs.append(song)

        if len(filtered_songs) >= request.limit:
            break

    # If no results and both filters were used, retry with language only
    if not filtered_songs and language_filter and request.artist:
        for song_id, score in recommendations:
            song = song_map.get(song_id)
            if not song:
                continue
            if song.language != language_filter:
                continue
            filtered_songs.append(song)
            if len(filtered_songs) >= request.limit:
                break

    # Convert to response schema
    song_responses = [SongResponse.model_validate(song) for song in filtered_songs]

    # Save recommendation history
    history_record = RecommendationHistory(
        user_id=current_user.id,
        moods_queried=json.dumps(request.moods),
        filters_applied=json.dumps({
            "language": request.language,
            "artist": request.artist
        }) if request.language or request.artist else None,
        results_count=len(song_responses)
    )
    db.add(history_record)
    db.commit()

    return RecommendationResponse(
        songs=song_responses,
        total_results=len(song_responses)
    )
