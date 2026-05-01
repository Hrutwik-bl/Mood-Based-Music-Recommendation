from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# Association table for many-to-many relationship between users and moods
user_moods = Table(
    'user_moods',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('mood', String(50), primary_key=True)
)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    recommendations = relationship("UserRecommendation", back_populates="user", cascade="all, delete-orphan")


class SpotifySong(Base):
    __tablename__ = "spotify_song"

    id = Column(Integer, primary_key=True, index=True)
    spotify_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    language = Column(String, default="en")
    moods = Column(Text, nullable=False)  # JSON string with list of moods
    album_art_url = Column(String, nullable=True)
    preview_url = Column(String, nullable=True)
    youtube_url = Column(String, nullable=True)

    # Audio features
    danceability = Column(Float, nullable=True)
    energy = Column(Float, nullable=True)
    valence = Column(Float, nullable=True)
    acousticness = Column(Float, nullable=True)
    tempo = Column(Float, nullable=True)

    added_at = Column(DateTime, default=datetime.utcnow)


class UserRecommendation(Base):
    __tablename__ = "user_recommendation"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    song_id = Column(Integer, ForeignKey("spotify_song.id"), nullable=False)
    mood_query = Column(String, nullable=False)  # The moods the user queried
    score = Column(Float, nullable=True)  # KNN similarity score
    recommended_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="recommendations")
    song = relationship("SpotifySong")


class MoodMapping(Base):
    __tablename__ = "mood_mapping"

    id = Column(Integer, primary_key=True, index=True)
    mood = Column(String(50), unique=True, nullable=False)
    # Audio feature targets for this mood
    target_danceability = Column(Float, default=0.5)
    target_energy = Column(Float, default=0.5)
    target_valence = Column(Float, default=0.5)
    target_acousticness = Column(Float, default=0.5)
    target_tempo = Column(Float, default=100.0)
