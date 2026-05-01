export default function SongCard({ song }) {
  const getYoutubeUrl = (songName, artistName) => {
    const query = `${songName} ${artistName}`;
    return `https://www.youtube.com/results?search_query=${encodeURIComponent(query)}`;
  };

  const moods = JSON.parse(song.moods);

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition">
      {/* Album Art */}
      {song.album_art_url ? (
        <img
          src={song.album_art_url}
          alt={song.name}
          className="w-full h-48 object-cover"
        />
      ) : (
        <div className="w-full h-48 bg-gradient-to-br from-purple-300 to-pink-300 flex items-center justify-center">
          <span className="text-gray-600">No Image</span>
        </div>
      )}

      {/* Song Details */}
      <div className="p-4">
        <h3 className="text-lg font-semibold text-gray-800 truncate">{song.name}</h3>
        <p className="text-gray-600 text-sm truncate mb-2">{song.artist}</p>

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

        {/* Links */}
        <div className="flex gap-2">
          {song.preview_url && (
            <a
              href={song.preview_url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 bg-green-500 text-white text-sm font-semibold py-2 px-3 rounded hover:bg-green-600 transition text-center"
            >
              Preview
            </a>
          )}
          <a
            href={getYoutubeUrl(song.name, song.artist)}
            target="_blank"
            rel="noopener noreferrer"
            className="flex-1 bg-red-500 text-white text-sm font-semibold py-2 px-3 rounded hover:bg-red-600 transition text-center"
          >
            YouTube
          </a>
        </div>
      </div>
    </div>
  );
}
