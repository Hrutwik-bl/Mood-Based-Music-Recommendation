import os
import json
from typing import List, Optional
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()


class SpotifyClient:
    def __init__(self):
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

        if not client_id or not client_secret:
            raise ValueError(
                "SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET must be set in .env"
            )

        auth_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

    def search_tracks(
        self,
        query: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[dict]:
        """Search for tracks on Spotify."""
        try:
            results = self.sp.search(
                q=query,
                type="track",
                limit=limit,
                offset=offset
            )
            return results.get("tracks", {}).get("items", [])
        except Exception as e:
            print(f"Error searching tracks: {e}")
            return []

    def get_audio_features(self, track_id: str) -> Optional[dict]:
        """Get audio features for a track."""
        try:
            features = self.sp.audio_features(track_id)
            if features and len(features) > 0:
                return features[0]
            return None
        except Exception as e:
            print(f"Error getting audio features for {track_id}: {e}")
            return None

    def get_track_details(self, track_id: str) -> Optional[dict]:
        """Get detailed information about a track."""
        try:
            track = self.sp.track(track_id)
            return track
        except Exception as e:
            print(f"Error getting track details for {track_id}: {e}")
            return None

    def fetch_songs_by_mood(
        self,
        mood_queries: dict,
        songs_per_mood: int = 50
    ) -> List[dict]:
        """
        Fetch songs from Spotify for each mood.

        Args:
            mood_queries: Dict mapping mood names to Spotify search queries
            songs_per_mood: Number of songs to fetch per mood

        Returns:
            List of songs with metadata
        """
        all_songs = []
        seen_spotify_ids = set()

        for mood, queries in mood_queries.items():
            if isinstance(queries, str):
                queries = [queries]

            for query in queries:
                tracks = self.search_tracks(query, limit=songs_per_mood)

                for track in tracks:
                    spotify_id = track.get("id")
                    if spotify_id and spotify_id not in seen_spotify_ids:
                        song_data = self._extract_song_data(track, mood)
                        if song_data:
                            all_songs.append(song_data)
                            seen_spotify_ids.add(spotify_id)

        return all_songs

    def _extract_song_data(self, track: dict, mood: str) -> Optional[dict]:
        """Extract relevant song data from Spotify track object."""
        try:
            album_art_url = None
            images = track.get("album", {}).get("images", [])
            if images:
                album_art_url = images[0]["url"]

            preview_url = track.get("preview_url")
            artist_name = track.get("artists", [{}])[0].get("name", "Unknown")

            audio_features = self.get_audio_features(track.get("id"))

            song_data = {
                "spotify_id": track.get("id"),
                "name": track.get("name"),
                "artist": artist_name,
                "language": "en",  # Spotify doesn't provide language, default to English
                "moods": json.dumps([mood]),
                "album_art_url": album_art_url,
                "preview_url": preview_url,
                "youtube_url": None,
                "danceability": audio_features.get("danceability") if audio_features else None,
                "energy": audio_features.get("energy") if audio_features else None,
                "valence": audio_features.get("valence") if audio_features else None,
                "acousticness": audio_features.get("acousticness") if audio_features else None,
                "tempo": audio_features.get("tempo") if audio_features else None,
            }

            return song_data
        except Exception as e:
            print(f"Error extracting song data: {e}")
            return None
