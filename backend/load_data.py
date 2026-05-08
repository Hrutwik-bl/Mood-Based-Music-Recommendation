#!/usr/bin/env python
"""
Script to populate the database with song data and train the ML model.
Can use real Spotify API data (if credentials provided) or mock data for development.
Supports multi-language song loading (17+ languages).
"""

import sys
import os
import json
import random
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy import func
from app.database import SessionLocal, init_db
from app.models import SpotifySong, MoodMapping
from app.ml_model import MusicRecommendationModel

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Try to import SpotifyClient, set flag if not available
try:
    from app.spotify_client import SpotifyClient
    SPOTIFY_AVAILABLE = bool(os.getenv("SPOTIFY_CLIENT_ID") and os.getenv("SPOTIFY_CLIENT_SECRET"))
except:
    SPOTIFY_AVAILABLE = False

# Language code to info mapping
LANGUAGE_QUERIES = {
    "en": {"name": "English", "queries": ["English songs"]},
    "kn": {"name": "Kannada", "queries": ["Kannada music"]},
    "hi": {"name": "Hindi", "queries": ["Hindi songs"]},
    "te": {"name": "Telugu", "queries": ["Telugu music"]},
    "ta": {"name": "Tamil", "queries": ["Tamil songs"]},
    "ml": {"name": "Malayalam", "queries": ["Malayalam music"]},
    "gu": {"name": "Gujarati", "queries": ["Gujarati songs"]},
    "or": {"name": "Odia", "queries": ["Odia music"]},
    "ne": {"name": "Nepali", "queries": ["Nepali songs"]},
    "ur": {"name": "Urdu", "queries": ["Urdu music"]},
    "kok": {"name": "Konkani", "queries": ["Konkani songs"]},
    "bn": {"name": "Bengali", "queries": ["Bengali music"]},
    "pa": {"name": "Punjabi", "queries": ["Punjabi songs"]},
    "sa": {"name": "Sanskrit", "queries": ["Sanskrit chants"]},
    "mr": {"name": "Marathi", "queries": ["Marathi music"]},
    "fr": {"name": "French", "queries": ["French songs"]},
    "es": {"name": "Spanish", "queries": ["Spanish songs"]},
}

# Real artist names for each language
LANGUAGE_ARTISTS = {
    "en": ["Ed Sheeran", "Taylor Swift", "The Weeknd", "Ariana Grande", "Drake", "Billie Eilish", "Post Malone", "Dua Lipa", "Bruno Mars", "Coldplay"],
    "kn": ["Puneeth Rajkumar", "Sandalwood Ensemble", "Hamsalekha", "Vishnuvaradhan", "Mangli", "Chethan Kumar", "Rakshit Shetty", "Challenging Star Darshan", "Yash", "Ganesh"],
    "hi": ["Shah Rukh Khan", "Arijit Singh", "Neha Kakkar", "Bollywood Orchestra", "A.R. Rahman", "Bollywood Classics", "Vishal Bhardwaj", "Priyanka Chopra", "Deepika Padukone", "Ranbir Kapoor"],
    "te": ["Mahesh Babu", "Pawan Kalyan", "Telugu Hits", "Devi Sri Prasad", "Allu Arjun", "Sukumar", "Sreeleela", "Samantha Ruth Prabhu", "Nani", "Sundeep Kishan"],
    "ta": ["Vijay", "Rajinikanth", "Suriya", "Tamil Melodies", "Anirudh Ravichander", "A.R. Murugadoss", "Siddharth", "Nayanthara", "Trisha Krishnan", "Taapsee Pannu"],
    "ml": ["Mohanlal", "Mammootty", "Malayalam Dreams", "A.R. Rahman", "Dulquer Salmaan", "Prithviraj Sukumaran", "Parvathy Thiruvothu", "Nivin Pauly", "Manju Warrier", "Tovino Thomas"],
    "gu": ["Gujarati Classics", "Folk Singers", "Gujarati Music", "Arijit Singh", "Kailash Kher", "Abha Hanjari", "Suresh Wadkar", "Asha Parekh", "Anupam Kher", "Mallika Sherawat"],
    "or": ["Odia Folk", "Humane Sagar", "Mihir Rai", "Odia Classics", "Jyoti Mishra", "Pragyan Nayak", "Anubhav Mohanty", "Babushan Mohanty", "Lipika Samantaray", "Amlan Mishra"],
    "ne": ["Nepalese Folk", "Arun Rai", "Shiva Pariyar", "Nepalese Music", "Devi Gharti Magar", "Anit Rai", "Pramod Kharel", "Julee Ale", "Aaryan Sigdel", "Namrata Shrestha"],
    "ur": ["Nusrat Fateh Ali Khan", "Abida Parveen", "Ghulam Ali", "Urdu Classics", "Rahat Fateh Ali Khan", "Kailash Kher", "Asha Ali", "Pakistani Music", "Ahmed Mughal", "Naheed Akhtar"],
    "kok": ["Konkani Folk", "Konkani Music", "Anoushka Shankar", "Konkani Classics", "Vishwanath Kini", "Prakash Neelkanthapilla", "Gurbaksh Singh", "Ravi Varma", "Ramakrishnan", "Girish Kasaravalli"],
    "bn": ["Tagore Classics", "Bengali Music", "Ravi Shankar", "Amitabh Bachchan", "Bangla Folk", "Sarod Ali Khan", "Kanan Devi", "Uttam Kumar", "Suchitra Mitra", "Pratibha Banerjee"],
    "pa": ["Punjabi Music", "Gurdas Maan", "Punjabi Folk", "Amar Singh Chamkila", "Daler Mehndi", "Jagjit Singh", "Punjabi Classics", "Harbhajan Mann", "Gillian", "Jagjit Kaur"],
    "sa": ["Sanskrit Chants", "Vedic Music", "Hari Om", "Classical Sanskrit", "Mantras", "Spiritual Music", "Ancient Hymns", "Devaki Nandan Sharma", "Ravi Shankar", "Bismillah Khan"],
    "mr": ["Marathi Music", "Marathi Folk", "Asha Bhosle", "Suresh Wadkar", "Marathi Classics", "Shankar Mahadevan", "Kailash Kher", "Marathi Theater", "Ajay-Atul", "Shreya Ghoshal"],
    "fr": ["French Classics", "Edith Piaf", "Charles Aznavour", "French Jazz", "Carla Bruni", "Michel Legrand", "French Chansons", "Stephane Grappelli", "Georges Brassens", "Serge Gainsbourg"],
    "es": ["Spanish Classics", "Enrique Iglesias", "Spanish Flamenco", "Paco de Lucia", "Real Madrid Anthem", "Spanish Guitar", "Joan Manuel Serrat", "Carlos Santana", "Laura Pausini", "Alejandro Fernandez"],
}

# Moods to feature mapping
MOOD_QUERIES = {
    "happy": ["uplifting positive joyful", "feel good", "cheerful"],
    "sad": ["emotional melancholic breakup", "sad songs", "heartbreak"],
    "energetic": ["powerful intense motivational", "high energy", "workout"],
    "chill": ["relaxing ambient calm", "lofi", "chillhop"],
    "focused": ["study concentration productivity", "instrumental", "focus music"],
    "romantic": ["love intimate romantic", "romantic ballads", "date night"],
    "party": ["dance club fun", "party hits", "dance music"],
}


def fetch_multilingual_songs(songs_per_language: int = 50) -> list:
    """
    Fetch songs in multiple languages from Spotify or return empty list if not available.
    Each mood is fetched for each language to get diverse recommendations.
    """
    if not SPOTIFY_AVAILABLE:
        print("⚠️  Spotify credentials not available. Using mock data instead.")
        return None

    try:
        spotify_client = SpotifyClient()
        all_songs = []
        seen_spotify_ids = set()
        songs_loaded = 0

        print(f"\nFetching {len(LANGUAGE_QUERIES)} languages with {len(MOOD_QUERIES)} moods...")
        print(f"Target: ~{songs_per_language} songs per language\n")

        for lang_code, lang_info in LANGUAGE_QUERIES.items():
            lang_name = lang_info["name"]
            lang_queries = lang_info["queries"]
            lang_songs = 0

            print(f"  Loading {lang_name} ({lang_code})...")

            # For each mood, search in this language
            for mood, mood_queries in MOOD_QUERIES.items():
                if not isinstance(mood_queries, list):
                    mood_queries = [mood_queries]

                for query in mood_queries:
                    # Append language to make search more specific
                    lang_query = f"{query} {lang_code}" if lang_code != "en" else query
                    tracks = spotify_client.search_tracks(lang_query, limit=10)

                    for track in tracks:
                        spotify_id = track.get("id")
                        if spotify_id and spotify_id not in seen_spotify_ids:
                            try:
                                song_data = spotify_client._extract_song_data(track, mood)
                                if song_data:
                                    song_data["language"] = lang_code
                                    all_songs.append(song_data)
                                    seen_spotify_ids.add(spotify_id)
                                    songs_loaded += 1
                                    lang_songs += 1

                                    if lang_songs >= songs_per_language:
                                        break
                            except:
                                pass

                    if lang_songs >= songs_per_language:
                        break

                if lang_songs >= songs_per_language:
                    break

            print(f"    ✓ Loaded {lang_songs} songs")

        print(f"\n✓ Total songs fetched from Spotify: {songs_loaded}")
        return all_songs if len(all_songs) > 0 else None

    except Exception as e:
        print(f"⚠️  Error fetching from Spotify: {e}")
        print("Falling back to mock data...")
        return None


def get_mock_songs_multilingual() -> list:
    """
    Generate mock songs for multiple languages (fallback when Spotify not available).
    Uses realistic artist names for each language.
    """
    mock_songs = []
    moods_list = list(MOOD_QUERIES.keys())
    song_counter = 0

    for lang_code, lang_info in LANGUAGE_QUERIES.items():
        lang_name = lang_info["name"]
        songs_per_language = 30
        artists_list = LANGUAGE_ARTISTS.get(lang_code, [f"{lang_name} Artist {i}" for i in range(10)])

        for i in range(songs_per_language):
            mood = moods_list[i % len(moods_list)]
            artist_idx = i % len(artists_list)
            artist_name = artists_list[artist_idx]
            song_counter += 1

            # Create realistic mock songs for each language
            mock_song = {
                "spotify_id": f"mock_{lang_code}_{i:03d}",
                "name": f"{lang_name} {mood.title()} Song {i+1}",
                "artist": artist_name,
                "language": lang_code,
                "moods": json.dumps([mood]),
                "album_art_url": f"https://via.placeholder.com/300?text={artist_name.replace(' ', '+')[:20]}",
                "preview_url": None,
                "youtube_url": None,
                # Randomize audio features based on mood
                "danceability": 0.5 + random.uniform(-0.3, 0.3),
                "energy": 0.5 + random.uniform(-0.3, 0.3),
                "valence": 0.5 + random.uniform(-0.3, 0.3),
                "acousticness": 0.5 + random.uniform(-0.3, 0.3),
                "tempo": 100 + random.uniform(-40, 40),
            }
            mock_songs.append(mock_song)

    print(f"\n✓ Generated {len(mock_songs)} mock songs for {len(LANGUAGE_QUERIES)} languages")
    return mock_songs

def populate_database():
    """Populate database with multi-language song data from Spotify or mock data."""
    print("Initializing database...")
    init_db()

    db = SessionLocal()

    try:
        # Check if data already exists
        existing_songs = db.query(SpotifySong).count()
        if existing_songs > 0:
            print(f"Database already contains {existing_songs} songs. Skipping population.")
            return

        # Try to fetch from Spotify, fall back to mock data
        print("Attempting to load songs...")
        songs_data = fetch_multilingual_songs(songs_per_language=50)

        if songs_data is None:
            print("\nGenerating mock data for development...")
            songs_data = get_mock_songs_multilingual()

        print(f"\nAdding {len(songs_data)} songs to database...")
        added_count = 0
        for song_data in songs_data:
            try:
                song = SpotifySong(
                    spotify_id=song_data["spotify_id"],
                    name=song_data["name"],
                    artist=song_data["artist"],
                    language=song_data["language"],
                    moods=song_data["moods"],
                    album_art_url=song_data["album_art_url"],
                    preview_url=song_data.get("preview_url"),
                    youtube_url=song_data.get("youtube_url"),
                    danceability=song_data.get("danceability"),
                    energy=song_data.get("energy"),
                    valence=song_data.get("valence"),
                    acousticness=song_data.get("acousticness"),
                    tempo=song_data.get("tempo"),
                )
                db.add(song)
                added_count += 1
            except Exception as e:
                print(f"  Warning: Failed to add song {song_data['name']}: {e}")

        db.commit()
        print(f"✓ Added {added_count} songs to database")

        # Create mood mappings
        print("Creating mood mappings for all moods...")
        for mood in MOOD_QUERIES.keys():
            existing_mapping = db.query(MoodMapping).filter(
                MoodMapping.mood == mood
            ).first()

            if not existing_mapping:
                mapping = MoodMapping(mood=mood)
                db.add(mapping)

        db.commit()
        print("✓ Mood mappings created")

        # Print statistics
        total_songs = db.query(SpotifySong).count()
        languages_in_db = db.query(SpotifySong.language).distinct().count()
        print(f"\n📊 Database Statistics:")
        print(f"   Total songs: {total_songs}")
        print(f"   Languages: {languages_in_db}")

        # Show languages
        language_counts = db.query(
            SpotifySong.language,
            func.count(SpotifySong.id).label('count')
        ).group_by(SpotifySong.language).all()

        print("   Languages by count:")
        for lang, count in sorted(language_counts, key=lambda x: x[1], reverse=True):
            lang_name = LANGUAGE_QUERIES.get(lang, {}).get("name", lang)
            print(f"     - {lang_name} ({lang}): {count} songs")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def train_model():
    """Train the ML model on the populated data."""
    print("\nTraining ML model...")
    db = SessionLocal()

    try:
        model = MusicRecommendationModel()
        model.train(db, k=5)
        print("✓ ML model trained and saved")
    except Exception as e:
        print(f"Error training model: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("Music Recommendation App - Data Population & Model Training")
    print("=" * 60)

    if SPOTIFY_AVAILABLE:
        print("✓ Spotify API credentials found")
        print("Loading real songs from Spotify in 17+ languages\n")
    else:
        print("⚠️  Spotify API credentials not found")
        print("Using generated mock data for development")
        print("To use real data, set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in .env\n")

    populate_database()
    train_model()

    print("\n" + "=" * 60)
    print("✅ Setup complete! You can now start the server.")
    print("Run: python -m uvicorn app.main:app --reload")
    print("=" * 60)
