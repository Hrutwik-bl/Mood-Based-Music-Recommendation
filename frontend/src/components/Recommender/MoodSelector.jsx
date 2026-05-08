import { useState, useEffect } from 'react';
import api from '../../api/client';

export default function MoodSelector({ onRecommendations, isLoading, setIsLoading }) {
  const [moods, setMoods] = useState([]);
  const [selectedMoods, setSelectedMoods] = useState([]);
  const [languages, setLanguages] = useState([]);
  const [artists, setArtists] = useState([]);
  const [selectedLanguage, setSelectedLanguage] = useState('');
  const [selectedArtist, setSelectedArtist] = useState('');
  const [error, setError] = useState('');

  // Fetch available moods, languages, and artists
  useEffect(() => {
    const fetchMetadata = async () => {
      try {
        const [moodsRes, langRes, artistRes] = await Promise.all([
          api.get('/metadata/moods'),
          api.get('/metadata/languages'),
          api.get('/metadata/artists'),
        ]);

        setMoods(moodsRes.data || []);
        setLanguages(langRes.data || []);
        setArtists(artistRes.data || []);
      } catch (err) {
        console.error('Error fetching metadata:', err);
        setError('Failed to load available moods and filters');
      }
    };

    fetchMetadata();
  }, []);

  const toggleMood = (mood) => {
    setSelectedMoods((prev) =>
      prev.includes(mood)
        ? prev.filter((m) => m !== mood)
        : [...prev, mood]
    );
  };

  const handleGetRecommendations = async () => {
    if (selectedMoods.length === 0) {
      setError('Please select at least one mood');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const response = await api.post('/recommend/', {
        moods: selectedMoods,
        language: selectedLanguage || undefined,
        artist: selectedArtist || undefined,
        limit: 20,
      });

      onRecommendations(response.data.songs);
    } catch (err) {
      const message = err.response?.data?.detail || 'Failed to get recommendations';
      setError(message);
      console.error('Error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Select Your Mood</h2>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {/* Mood Selection */}
      <div className="mb-6">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
          {moods.map((mood) => (
            <button
              key={mood.mood}
              onClick={() => toggleMood(mood.mood)}
              className={`p-3 rounded-lg font-semibold transition ${
                selectedMoods.includes(mood.mood)
                  ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                  : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
              }`}
              title={mood.description}
            >
              {mood.mood.charAt(0).toUpperCase() + mood.mood.slice(1)}
            </button>
          ))}
        </div>
        <p className="text-sm text-gray-600 mt-2">
          Selected: {selectedMoods.length > 0 ? selectedMoods.join(', ') : 'None'}
        </p>
      </div>

      {/* Filters */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div>
          <label className="block text-gray-700 text-sm font-medium mb-2">Language</label>
          <select
            value={selectedLanguage}
            onChange={(e) => setSelectedLanguage(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          >
            <option value="">All Languages</option>
            {languages.map((lang) => (
              <option key={lang.language} value={lang.language}>
                {lang.language}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-gray-700 text-sm font-medium mb-2">Artist</label>
          <select
            value={selectedArtist}
            onChange={(e) => setSelectedArtist(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          >
            <option value="">All Artists</option>
            {artists.map((artist) => (
              <option key={artist.artist} value={artist.artist}>
                {artist.artist}
              </option>
            ))}
          </select>
        </div>
      </div>

      <button
        onClick={handleGetRecommendations}
        disabled={isLoading || selectedMoods.length === 0}
        className="w-full bg-gradient-to-r from-purple-500 to-pink-500 text-white font-bold py-3 px-4 rounded-lg hover:opacity-90 transition disabled:opacity-50"
      >
        {isLoading ? 'Getting recommendations...' : 'Get Recommendations'}
      </button>
    </div>
  );
}
