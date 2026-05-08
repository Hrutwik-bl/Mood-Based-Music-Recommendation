import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import MoodSelector from '../Recommender/MoodSelector';
import SongList from '../SongList/SongList';

export default function Home() {
  const { user, logout } = useAuth();
  const [songs, setSongs] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg">
        <div className="container mx-auto px-4 py-6 flex justify-between items-center">
          <h1 className="text-3xl font-bold">🎵 Music Vibe</h1>
          <div className="space-x-4">
            <Link
              to="/profile"
              className="inline-block px-4 py-2 bg-white text-purple-500 font-semibold rounded-lg hover:bg-gray-100 transition"
            >
              👤 My Profile
            </Link>
            <button
              onClick={logout}
              className="bg-white text-purple-500 font-semibold py-2 px-4 rounded-lg hover:bg-gray-100 transition"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <MoodSelector
          onRecommendations={setSongs}
          isLoading={isLoading}
          setIsLoading={setIsLoading}
        />
        <SongList songs={songs} isLoading={isLoading} />
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-gray-300 text-center py-4 mt-12">
        <p>🎵 Music Recommendation App - Get personalized song suggestions based on your mood</p>
      </footer>
    </div>
  );
}
