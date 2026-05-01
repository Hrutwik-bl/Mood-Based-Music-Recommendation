#!/usr/bin/env python
"""
Script to populate the database with Spotify songs and train the ML model.
Run this after setting up your Spotify API credentials in .env
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, init_db
from app.spotify_client import SpotifyClient
from app.models import SpotifySong, MoodMapping
from app.ml_model import MusicRecommendationModel

# Define mood search queries for Spotify
MOOD_QUERIES = {
    "happy": [
        "happy uplifting joyful",
        "feel good pop",
        "positive vibes",
    ],
    "sad": [
        "sad emotional melancholic",
        "breakup songs",
        "sad indie",
    ],
    "energetic": [
        "energetic powerful pump up",
        "heavy metal rock",
        "motivational intense",
    ],
    "chill": [
        "chill relaxing ambient",
        "lo-fi hip hop",
        "meditation relaxation",
    ],
    "focused": [
        "focus study concentration",
        "lo-fi beats",
        "jazz instrumental",
    ],
    "romantic": [
        "romantic love songs",
        "slow love ballads",
        "couples date night",
    ],
    "party": [
        "party dance electronic",
        "club bangers",
        "festival music",
    ],
}


def populate_database():
    """Fetch songs from Spotify and populate the database."""
    print("Initializing database...")
    init_db()

    db = SessionLocal()

    try:
        # Check if data already exists
        existing_songs = db.query(SpotifySong).count()
        if existing_songs > 0:
            print(f"Database already contains {existing_songs} songs. Skipping population.")
            return

        print("Connecting to Spotify...")
        spotify_client = SpotifyClient()

        print("Fetching songs from Spotify...")
        all_songs = spotify_client.fetch_songs_by_mood(MOOD_QUERIES, songs_per_mood=30)

        print(f"Found {len(all_songs)} unique songs. Adding to database...")
        for song_data in all_songs:
            existing = db.query(SpotifySong).filter(
                SpotifySong.spotify_id == song_data["spotify_id"]
            ).first()

            if not existing:
                song = SpotifySong(**song_data)
                db.add(song)

        db.commit()
        print(f"✓ Added {len(all_songs)} songs to database")

        # Create mood mappings
        print("Creating mood mappings...")
        for mood in MOOD_QUERIES.keys():
            existing_mapping = db.query(MoodMapping).filter(
                MoodMapping.mood == mood
            ).first()

            if not existing_mapping:
                mapping = MoodMapping(mood=mood)
                db.add(mapping)

        db.commit()
        print("✓ Mood mappings created")

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

    populate_database()
    train_model()

    print("\n" + "=" * 60)
    print("Setup complete! You can now start the server.")
    print("=" * 60)
