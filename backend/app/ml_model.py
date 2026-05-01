import os
import json
import numpy as np
import pickle
from typing import List, Optional, Tuple
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sqlalchemy.orm import Session
from app.models import SpotifySong, MoodMapping

MODEL_PATH = "ml_model.pkl"
SCALER_PATH = "scaler.pkl"


class MusicRecommendationModel:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.song_ids = None
        self.features = None
        self.load_or_create_model()

    def load_or_create_model(self):
        """Load model from disk or create a new one."""
        if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
            try:
                with open(MODEL_PATH, "rb") as f:
                    self.model = pickle.load(f)
                with open(SCALER_PATH, "rb") as f:
                    self.scaler = pickle.load(f)
                print("Loaded pretrained model from disk")
            except Exception as e:
                print(f"Error loading model: {e}")
                self.model = None
                self.scaler = None
        else:
            print("No pretrained model found. Will train after Spotify data is loaded.")

    def train(self, db: Session, k: int = 5):
        """Train the KNN model on Spotify song data."""
        # Get all songs with audio features
        songs = db.query(SpotifySong).filter(
            SpotifySong.danceability.isnot(None),
            SpotifySong.energy.isnot(None),
            SpotifySong.valence.isnot(None),
            SpotifySong.acousticness.isnot(None),
            SpotifySong.tempo.isnot(None)
        ).all()

        if len(songs) < k:
            raise ValueError(
                f"Not enough songs in database to train model. Need at least {k}, have {len(songs)}"
            )

        # Extract features
        features = np.array([
            [
                song.danceability,
                song.energy,
                song.valence,
                song.acousticness,
                song.tempo / 200.0  # Normalize tempo
            ]
            for song in songs
        ])

        # Normalize features
        self.scaler = StandardScaler()
        features_scaled = self.scaler.fit_transform(features)

        # Train KNN model
        self.model = NearestNeighbors(n_neighbors=k, metric="euclidean")
        self.model.fit(features_scaled)

        # Store references
        self.song_ids = [song.id for song in songs]
        self.features = features_scaled

        # Save model to disk
        with open(MODEL_PATH, "wb") as f:
            pickle.dump(self.model, f)
        with open(SCALER_PATH, "wb") as f:
            pickle.dump(self.scaler, f)

        print(f"Model trained on {len(songs)} songs")

    def get_mood_vector(
        self,
        moods: List[str],
        db: Session
    ) -> Optional[np.ndarray]:
        """
        Convert moods to a feature vector.

        Strategy: Average the audio features of songs tagged with these moods.
        """
        songs_with_moods = []

        for mood in moods:
            # Get songs with this mood
            songs = db.query(SpotifySong).filter(
                SpotifySong.danceability.isnot(None),
                SpotifySong.energy.isnot(None),
                SpotifySong.valence.isnot(None),
                SpotifySong.acousticness.isnot(None),
                SpotifySong.tempo.isnot(None)
            ).all()

            # Filter by mood
            for song in songs:
                song_moods = json.loads(song.moods)
                if mood.lower() in [m.lower() for m in song_moods]:
                    songs_with_moods.append(song)

        if not songs_with_moods:
            # Fallback: Use mood mapping defaults if available
            mood_mapping = db.query(MoodMapping).filter(
                MoodMapping.mood.in_([m.lower() for m in moods])
            ).first()

            if mood_mapping:
                return np.array([[
                    mood_mapping.target_danceability,
                    mood_mapping.target_energy,
                    mood_mapping.target_valence,
                    mood_mapping.target_acousticness,
                    mood_mapping.target_tempo / 200.0
                ]])

            # Last resort: average across all moods
            return self._get_default_mood_vector(moods)

        # Average features of songs with these moods
        avg_features = np.array([
            [
                np.mean([s.danceability for s in songs_with_moods]),
                np.mean([s.energy for s in songs_with_moods]),
                np.mean([s.valence for s in songs_with_moods]),
                np.mean([s.acousticness for s in songs_with_moods]),
                np.mean([s.tempo for s in songs_with_moods]) / 200.0
            ]
        ])

        return avg_features

    def _get_default_mood_vector(self, moods: List[str]) -> np.ndarray:
        """Get default feature vectors for moods."""
        mood_defaults = {
            "happy": [0.7, 0.7, 0.8, 0.2, 120.0],
            "sad": [0.3, 0.3, 0.2, 0.6, 80.0],
            "energetic": [0.6, 0.9, 0.6, 0.1, 130.0],
            "chill": [0.4, 0.4, 0.5, 0.7, 90.0],
            "focused": [0.5, 0.5, 0.4, 0.4, 100.0],
            "romantic": [0.5, 0.4, 0.6, 0.5, 95.0],
            "party": [0.8, 0.8, 0.7, 0.1, 120.0],
        }

        vectors = []
        for mood in moods:
            vector = mood_defaults.get(mood.lower(), [0.5, 0.5, 0.5, 0.5, 100.0])
            vectors.append(vector)

        avg_vector = np.mean(vectors, axis=0)
        avg_vector[-1] /= 200.0  # Normalize tempo
        return np.array([avg_vector])

    def recommend(
        self,
        moods: List[str],
        db: Session,
        limit: int = 10
    ) -> List[Tuple[int, float]]:
        """
        Get song recommendations for given moods.

        Returns:
            List of (song_id, distance) tuples
        """
        if self.model is None:
            raise ValueError("Model not trained yet. Please train the model first.")

        # Get mood vector
        mood_vector = self.get_mood_vector(moods, db)
        if mood_vector is None:
            return []

        # Normalize mood vector
        mood_vector_scaled = self.scaler.transform(mood_vector)

        # Find nearest neighbors
        distances, indices = self.model.kneighbors(mood_vector_scaled, n_neighbors=min(limit, len(self.song_ids)))

        # Return song IDs and distances
        results = [
            (self.song_ids[idx], float(dist))
            for idx, dist in zip(indices[0], distances[0])
        ]

        return results
