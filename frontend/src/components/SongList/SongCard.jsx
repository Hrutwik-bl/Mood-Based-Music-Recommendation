import { useState } from 'react';
import api from '../../api/client';

export default function SongCard({ song, onLikeChange }) {
  const [isLiked, setIsLiked] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const getYoutubeUrl = (songName, artistName) => {
    const query = `${songName} ${artistName}`;
    return `https://www.youtube.com/results?search_query=${encodeURIComponent(query)}`;
  };

  const handleLike = async (e) => {
    e.preventDefault();
    try {
      setIsLoading(true);
      if (isLiked) {
        await api.delete(`/profile/liked-songs/${song.id}`);
        setIsLiked(false);
      } else {
        await api.post(`/profile/liked-songs/${song.id}`);
        setIsLiked(true);
      }
      if (onLikeChange) {
        onLikeChange(song.id, !isLiked);
      }
    } catch (err) {
      console.error('Failed to like/unlike song', err);
    } finally {
      setIsLoading(false);
    }
  };

  const moods = JSON.parse(song.moods);

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition">
      {/* Album Art */}
      <img
        src={song.album_art_url || '/music_vibe.png'}
        alt={song.name}
        className="w-full h-48 object-cover bg-gray-200"
        onError={(e) => {
          e.target.src = '/music_vibe.png';
        }}
      />

      {/* Song Details */}
      <div className="p-4">
        <div className="flex justify-between items-start mb-2">
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-800 truncate">{song.name}</h3>
            <p className="text-gray-600 text-sm truncate">{song.artist}</p>
          </div>
          <button
            onClick={handleLike}
            disabled={isLoading}
            className={`ml-2 text-2xl transition ${
              isLiked ? 'text-red-500' : 'text-gray-400 hover:text-red-500'
            } disabled:opacity-50`}
            title={isLiked ? 'Unlike' : 'Like'}
          >
            ❤️
          </button>
        </div>

        {/* Moods */}
        <div className="flex flex-wrap gap-1 mb-3">
          {moods.map((mood) => (
            <span
              key={mood}
              className="inline-block bg-purple-100 text-purple-700 text-xs px-2 py-1 rounded-full"
            >
              {mood}
            </span>
          ))}
        </div>

        {/* Audio Features */}
        <div className="grid grid-cols-2 gap-2 text-xs text-gray-600 mb-3">
          {song.energy !== null && (
            <div>Energy: {(song.energy * 100).toFixed(0)}%</div>
          )}
          {song.danceability !== null && (
            <div>Danceability: {(song.danceability * 100).toFixed(0)}%</div>
          )}
          {song.valence !== null && (
            <div>Mood: {(song.valence * 100).toFixed(0)}%</div>
          )}
          {song.acousticness !== null && (
            <div>Acoustic: {(song.acousticness * 100).toFixed(0)}%</div>
          )}
        </div>

        {/* Audio Player */}
        {song.preview_url ? (
          <div className="mb-3">
            <audio
              controls
              className="w-full h-8"
              controlsList="nodownload"
            >
              <source src={song.preview_url} type="audio/mpeg" />
              Your browser does not support the audio element.
            </audio>
          </div>
        ) : (
          <div className="mb-3 bg-gray-100 text-gray-600 text-sm p-2 rounded text-center">
            No preview available
          </div>
        )}

        {/* Links */}
        <div className="flex gap-2">
          <a
            href={getYoutubeUrl(song.name, song.artist)}
            target="_blank"
            rel="noopener noreferrer"
            className="flex-1 bg-red-500 text-white text-sm font-semibold py-2 px-3 rounded hover:bg-red-600 transition text-center"
          >
            🎵 YouTube
          </a>
        </div>
      </div>
    </div>
  );
}
