import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import api from '../../api/client';

export default function UserProfile() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('info');
  const [userInfo, setUserInfo] = useState(null);
  const [preferences, setPreferences] = useState({
    preferred_languages: [],
    preferred_genres: []
  });
  const [likedSongs, setLikedSongs] = useState([]);
  const [recommendationHistory, setRecommendationHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedLanguages, setSelectedLanguages] = useState([]);

  const languages = [
    'en', 'kn', 'hi', 'te', 'ta', 'ml', 'gu', 'or', 'ne', 'ur', 'kok', 'bn', 'pa', 'sa', 'mr', 'fr', 'es'
  ];

  const languageNames = {
    en: 'English',
    kn: 'Kannada',
    hi: 'Hindi',
    te: 'Telugu',
    ta: 'Tamil',
    ml: 'Malayalam',
    gu: 'Gujarati',
    or: 'Odia',
    ne: 'Nepali',
    ur: 'Urdu',
    kok: 'Konkani',
    bn: 'Bengali',
    pa: 'Punjabi',
    sa: 'Sanskrit',
    mr: 'Marathi',
    fr: 'French',
    es: 'Spanish'
  };

  useEffect(() => {
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      setIsLoading(true);
      const [infoRes, prefsRes, likedRes, historyRes] = await Promise.all([
        api.get('/auth/me'),
        api.get('/profile/preferences'),
        api.get('/profile/liked-songs'),
        api.get('/profile/history')
      ]);

      setUserInfo(infoRes.data);
      setPreferences(prefsRes.data);
      setSelectedLanguages(prefsRes.data.preferred_languages || []);
      setLikedSongs(likedRes.data);
      setRecommendationHistory(historyRes.data);
      setError('');
    } catch (err) {
      setError('Failed to load profile data');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLanguageToggle = (lang) => {
    setSelectedLanguages(prev =>
      prev.includes(lang)
        ? prev.filter(l => l !== lang)
        : [...prev, lang]
    );
  };

  const handleSavePreferences = async () => {
    try {
      await api.post('/profile/preferences', {
        preferred_languages: selectedLanguages,
        preferred_genres: preferences.preferred_genres || []
      });
      setPreferences({
        ...preferences,
        preferred_languages: selectedLanguages
      });
      setError('');
    } catch (err) {
      setError('Failed to save preferences');
    }
  };

  const handleUnlikeSong = async (songId) => {
    try {
      await api.delete(`/profile/liked-songs/${songId}`);
      setLikedSongs(likedSongs.filter(song => song.song_id !== songId));
    } catch (err) {
      setError('Failed to unlike song');
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-lg">Loading profile...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg">
        <div className="container mx-auto px-4 py-6 flex justify-between items-center">
          <Link to="/home" className="text-3xl font-bold hover:opacity-80 transition">
            🎵 Music Vibe
          </Link>
          <div className="space-x-4">
            <button
              onClick={() => navigate('/home')}
              className="px-4 py-2 hover:bg-purple-600 transition rounded-lg"
            >
              Back to Home
            </button>
            <button
              onClick={logout}
              className="bg-white text-purple-500 font-semibold py-2 px-4 rounded-lg hover:bg-gray-100 transition"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Profile Container */}
      <main className="container mx-auto px-4 py-8 max-w-4xl">
        {error && (
          <div className="mb-6 bg-red-100 border-l-4 border-red-500 text-red-700 px-4 py-3 rounded">
            <p>{error}</p>
          </div>
        )}

        {/* User Info Card */}
        {userInfo && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">👤 Your Profile</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p className="text-gray-600 text-sm">Email</p>
                <p className="text-lg font-semibold text-gray-800">{userInfo.email}</p>
              </div>
              <div>
                <p className="text-gray-600 text-sm">Member Since</p>
                <p className="text-lg font-semibold text-gray-800">
                  {new Date(userInfo.created_at).toLocaleDateString()}
                </p>
              </div>
              {userInfo.last_login && (
                <div>
                  <p className="text-gray-600 text-sm">Last Login</p>
                  <p className="text-lg font-semibold text-gray-800">
                    {new Date(userInfo.last_login).toLocaleString()}
                  </p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          {/* Tab Navigation */}
          <div className="flex border-b border-gray-200">
            <button
              onClick={() => setActiveTab('languages')}
              className={`flex-1 py-4 px-4 font-semibold transition ${
                activeTab === 'languages'
                  ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              🌍 Languages & Preferences
            </button>
            <button
              onClick={() => setActiveTab('liked')}
              className={`flex-1 py-4 px-4 font-semibold transition ${
                activeTab === 'liked'
                  ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              ❤️ Liked Songs ({likedSongs.length})
            </button>
            <button
              onClick={() => setActiveTab('history')}
              className={`flex-1 py-4 px-4 font-semibold transition ${
                activeTab === 'history'
                  ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              📋 History
            </button>
          </div>

          {/* Tab Content */}
          <div className="p-6">
            {/* Languages Tab */}
            {activeTab === 'languages' && (
              <div>
                <h3 className="text-xl font-bold text-gray-800 mb-4">Select Your Preferred Languages</h3>
                <p className="text-gray-600 mb-6">Choose languages to see recommendations from those regions:</p>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
                  {languages.map(lang => (
                    <label key={lang} className="flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        checked={selectedLanguages.includes(lang)}
                        onChange={() => handleLanguageToggle(lang)}
                        className="mr-2 w-4 h-4 text-purple-600 rounded"
                      />
                      <span className="text-gray-700">{languageNames[lang]}</span>
                    </label>
                  ))}
                </div>
                <button
                  onClick={handleSavePreferences}
                  className="bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold py-2 px-6 rounded-lg hover:opacity-90 transition"
                >
                  Save Preferences
                </button>
              </div>
            )}

            {/* Liked Songs Tab */}
            {activeTab === 'liked' && (
              <div>
                <h3 className="text-xl font-bold text-gray-800 mb-4">Your Liked Songs</h3>
                {likedSongs.length === 0 ? (
                  <p className="text-gray-600">No liked songs yet. Start liking songs to build your collection!</p>
                ) : (
                  <div className="space-y-4">
                    {likedSongs.map(liked => (
                      <div key={liked.id} className="bg-gray-50 p-4 rounded-lg flex justify-between items-start">
                        <div className="flex-1">
                          <p className="font-semibold text-gray-800">{liked.song?.name}</p>
                          <p className="text-gray-600 text-sm">{liked.song?.artist}</p>
                          <p className="text-xs text-gray-500 mt-1">
                            Liked on {new Date(liked.liked_at).toLocaleDateString()}
                          </p>
                        </div>
                        <button
                          onClick={() => handleUnlikeSong(liked.song_id)}
                          className="ml-4 px-4 py-2 bg-red-100 text-red-600 font-semibold rounded-lg hover:bg-red-200 transition"
                        >
                          Unlike
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* History Tab */}
            {activeTab === 'history' && (
              <div>
                <h3 className="text-xl font-bold text-gray-800 mb-4">Recommendation History</h3>
                {recommendationHistory.length === 0 ? (
                  <p className="text-gray-600">No recommendation history yet.</p>
                ) : (
                  <div className="space-y-4">
                    {recommendationHistory.map(record => (
                      <div key={record.id} className="bg-gray-50 p-4 rounded-lg">
                        <div className="flex justify-between items-start mb-2">
                          <div>
                            <p className="font-semibold text-gray-800">
                              Moods: {record.moods_queried.join(', ')}
                            </p>
                            {record.filters_applied && (
                              <p className="text-sm text-gray-600">
                                Filters: {JSON.stringify(record.filters_applied)}
                              </p>
                            )}
                          </div>
                          <span className="text-sm bg-purple-100 text-purple-700 px-3 py-1 rounded-full">
                            {record.results_count} results
                          </span>
                        </div>
                        <p className="text-xs text-gray-500">
                          {new Date(record.query_timestamp).toLocaleString()}
                        </p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-gray-300 text-center py-4 mt-12">
        <p>🎵 Music Vibe - Discover music that matches your mood</p>
      </footer>
    </div>
  );
}
