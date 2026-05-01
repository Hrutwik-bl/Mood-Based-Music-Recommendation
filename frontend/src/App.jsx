import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './hooks/useAuth';
import Login from './components/Auth/Login';
import Signup from './components/Auth/Signup';
import MoodSelector from './components/Recommender/MoodSelector';
import SongList from './components/SongList/SongList';

function Home() {
  const { user, logout } = useAuth();
  const [songs, setSongs] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg">
        <div className="container mx-auto px-4 py-6 flex justify-between items-center">
          <h1 className="text-3xl font-bold">🎵 Music Vibe</h1>
          <button
            onClick={logout}
            className="bg-white text-purple-500 font-semibold py-2 px-4 rounded-lg hover:bg-gray-100 transition"
          >
            Logout
          </button>
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

function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Loading...</p>
      </div>
    );
  }

  return user ? children : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
}
