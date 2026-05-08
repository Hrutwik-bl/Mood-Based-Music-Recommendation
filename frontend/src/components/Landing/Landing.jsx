import { Link } from 'react-router-dom';

export default function Landing() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-600 to-pink-600 text-white">
      {/* Navigation */}
      <nav className="container mx-auto px-4 py-4 flex justify-between items-center">
        <h1 className="text-3xl font-bold">🎵 Music Vibe</h1>
        <div className="space-x-4">
          <Link
            to="/login"
            className="px-4 py-2 rounded-lg hover:bg-purple-700 transition"
          >
            Sign In
          </Link>
          <Link
            to="/signup"
            className="px-4 py-2 bg-white text-purple-600 font-semibold rounded-lg hover:bg-gray-100 transition"
          >
            Sign Up
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-16 text-center">
        <h2 className="text-5xl font-bold mb-6">Discover Music That Matches Your Mood</h2>
        <p className="text-xl mb-8 text-purple-100">
          Let AI-powered recommendations guide you to the perfect songs for any moment
        </p>
        <Link
          to="/login"
          className="inline-block px-8 py-4 bg-white text-purple-600 font-bold text-lg rounded-lg hover:bg-gray-100 transition shadow-lg"
        >
          Get Started
        </Link>
      </section>

      {/* Features Section */}
      <section className="bg-white text-gray-800 py-16">
        <div className="container mx-auto px-4">
          <h3 className="text-3xl font-bold text-center mb-12">Why Choose Music Vibe?</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="text-center p-6 bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg shadow-md">
              <div className="text-5xl mb-4">🎯</div>
              <h4 className="text-xl font-bold mb-3">Mood-Based Recommendations</h4>
              <p className="text-gray-600">
                Simply select your current mood (happy, sad, energetic, chill, etc.) and get personalized song recommendations instantly.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="text-center p-6 bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg shadow-md">
              <div className="text-5xl mb-4">🌍</div>
              <h4 className="text-xl font-bold mb-3">Multi-Language Support</h4>
              <p className="text-gray-600">
                Enjoy songs in 17+ languages including English, Hindi, Kannada, Tamil, Telugu, and many more. Explore music from around the world.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="text-center p-6 bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg shadow-md">
              <div className="text-5xl mb-4">❤️</div>
              <h4 className="text-xl font-bold mb-3">Save Your Favorites</h4>
              <p className="text-gray-600">
                Like and save your favorite songs to your personal library. Build your perfect playlist over time.
              </p>
            </div>

            {/* Feature 4 */}
            <div className="text-center p-6 bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg shadow-md">
              <div className="text-5xl mb-4">🤖</div>
              <h4 className="text-xl font-bold mb-3">AI-Powered Matching</h4>
              <p className="text-gray-600">
                Our machine learning algorithm analyzes audio features like energy, danceability, and acousticness for perfect matches.
              </p>
            </div>

            {/* Feature 5 */}
            <div className="text-center p-6 bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg shadow-md">
              <div className="text-5xl mb-4">👤</div>
              <h4 className="text-xl font-bold mb-3">Your Profile</h4>
              <p className="text-gray-600">
                Manage your preferences, view your music history, and track all your favorite recommendations in one place.
              </p>
            </div>

            {/* Feature 6 */}
            <div className="text-center p-6 bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg shadow-md">
              <div className="text-5xl mb-4">🎨</div>
              <h4 className="text-xl font-bold mb-3">Artist Discovery</h4>
              <p className="text-gray-600">
                Filter recommendations by your favorite artists and discover similar music from across the globe.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-r from-purple-600 to-pink-600 text-white py-16">
        <div className="container mx-auto px-4 text-center">
          <h3 className="text-3xl font-bold mb-6">Ready to Find Your Next Favorite Song?</h3>
          <p className="text-lg mb-8 text-purple-100">
            Join thousands of music lovers discovering songs that match their mood
          </p>
          <div className="space-x-4">
            <Link
              to="/signup"
              className="inline-block px-8 py-3 bg-white text-purple-600 font-bold rounded-lg hover:bg-gray-100 transition"
            >
              Sign Up Free
            </Link>
            <Link
              to="/login"
              className="inline-block px-8 py-3 border-2 border-white text-white font-bold rounded-lg hover:bg-purple-700 transition"
            >
              Sign In
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 text-center py-6">
        <p>🎵 Music Vibe - Get personalized song suggestions based on your mood</p>
        <p className="text-sm mt-2">© 2026 Music Vibe. All rights reserved.</p>
      </footer>
    </div>
  );
}
