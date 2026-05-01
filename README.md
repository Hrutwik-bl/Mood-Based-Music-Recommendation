# 🎵 Music Recommendation App

An AI-powered music recommendation application that suggests songs based on your mood. Built with FastAPI, React, Vite, and scikit-learn's K-Nearest Neighbors algorithm.

## Features

- **User Authentication**: Secure signup and login with JWT tokens
- **Mood-Based Recommendations**: Get personalized song suggestions based on multiple mood selections
- **Smart Filtering**: Filter recommendations by language and artist
- **Audio Features Analysis**: Songs analyzed by energy, danceability, valence, acousticness, and tempo
- **Spotify Integration**: Pulls real songs and metadata from Spotify
- **Beautiful UI**: Modern, responsive React frontend with Tailwind CSS
- **Docker Ready**: Easy deployment with Docker and Docker Compose

## Architecture

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **ML Model**: K-Nearest Neighbors (scikit-learn)
- **API Authentication**: JWT tokens with bcrypt password hashing
- **External API**: Spotify Web API

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios with JWT interceptors
- **Routing**: React Router v6

## Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn
- Docker & Docker Compose (optional, for containerized deployment)
- Spotify Developer Account (for API credentials)

## Quick Start

### 1. Get Spotify API Credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new application
3. Accept the terms and create the app
4. Copy your `Client ID` and `Client Secret`

### 2. Setup Backend

```bash
cd backend

# Create environment file
cp .env.example .env

# Edit .env with your Spotify credentials
# SPOTIFY_CLIENT_ID=your_client_id
# SPOTIFY_CLIENT_SECRET=your_client_secret
# SECRET_KEY=your_secret_key
```

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Populate database and train ML model
python load_data.py

# Start the server
uvicorn app.main:app --reload
```

The backend will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### 3. Setup Frontend

```bash
cd frontend

# Create environment file
cp .env.example .env

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register a new user
- `POST /api/auth/login` - Login and get JWT token

### Recommendations
- `POST /api/recommend/` - Get song recommendations
  ```json
  {
    "moods": ["happy", "energetic"],
    "language": "en",
    "artist": "Drake",
    "limit": 10
  }
  ```

### Metadata
- `GET /api/metadata/moods` - List available moods
- `GET /api/metadata/languages` - List available languages
- `GET /api/metadata/artists` - List available artists

## Docker Deployment

```bash
# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Edit backend/.env with Spotify credentials

# Build and run with Docker Compose
docker-compose up --build

# On first run, populate the database:
docker exec music-rec-backend python load_data.py
```

Then access:
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

## Project Structure

```
music-recommendation-app/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI app
│   │   ├── database.py       # SQLAlchemy setup
│   │   ├── models.py         # Database models
│   │   ├── schemas.py        # Pydantic schemas
│   │   ├── auth.py           # JWT & password hashing
│   │   ├── spotify_client.py # Spotify API client
│   │   ├── ml_model.py       # KNN recommendation model
│   │   ├── utils.py          # Helper functions
│   │   └── routes/
│   │       ├── auth.py       # Auth endpoints
│   │       ├── recommend.py  # Recommendation endpoints
│   │       └── metadata.py   # Metadata endpoints
│   ├── load_data.py          # Data population & model training
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   └── .gitignore
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Auth/         # Login/Signup
│   │   │   ├── Recommender/  # Mood selector
│   │   │   └── SongList/     # Song display
│   │   ├── hooks/
│   │   │   └── useAuth.js    # Auth state management
│   │   ├── api/
│   │   │   └── client.js     # Axios instance
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── Dockerfile
│   ├── .env.example
│   └── .gitignore
├── docker-compose.yml
└── README.md
```

## How It Works

### Mood-Based Recommendations

1. **User selects moods**: Happy, Energetic, Chill, etc.
2. **Mood → Audio Features**: The app maps moods to audio features:
   - Happy: High valence, high energy
   - Chill: Low energy, high acousticness
   - Party: High danceability, high energy
3. **K-Nearest Neighbors**: The ML model finds the K closest songs in audio feature space
4. **Results displayed**: Songs are ranked by similarity and filtered by language/artist

### Audio Features Used

- **Danceability** (0-1): How suitable a track is for dancing
- **Energy** (0-1): Intensity and activity of the track
- **Valence** (0-1): Musical positiveness/happiness
- **Acousticness** (0-1): Confidence measure of acoustic instruments
- **Tempo** (BPM): Beats per minute

## Configuration

### Backend Environment Variables

```
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SECRET_KEY=your_secret_key_for_jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=30
DATABASE_URL=sqlite:///./music_recommendation.db
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_URL=http://localhost:5173
```

### Frontend Environment Variables

```
VITE_API_URL=http://localhost:8000/api
```

## Testing

### Backend Tests

```bash
cd backend

# Test auth endpoints
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Get recommendations (use token from signup/login)
curl -X POST http://localhost:8000/api/recommend/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"moods":["happy","energetic"],"limit":10}'

# Get metadata
curl http://localhost:8000/api/metadata/moods \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Frontend Tests

- Sign up with new email and password
- Log in with created account
- Select moods and get recommendations
- Filter by language and artist
- Click preview or YouTube links

## Performance Considerations

- **KNN Model**: Trained once at startup, recommendations take ~50ms
- **Spotify API**: Songs cached in database to minimize API calls
- **JWT Tokens**: 30-day expiration for security
- **Database**: SQLite suitable for development; upgrade to PostgreSQL for production

## Troubleshooting

### No songs in database
- Ensure `load_data.py` has been run
- Check Spotify credentials in `.env`
- Verify internet connection

### Recommendations not working
- Check if ML model files (ml_model.pkl, scaler.pkl) exist
- Run `python load_data.py` again to retrain

### CORS errors
- Frontend URL must be whitelisted in backend CORS config
- Check `FRONTEND_URL` environment variable

### Port conflicts
- Backend runs on 8000, Frontend on 5173 (dev) or 3000 (prod)
- Change in respective config files if needed

## Future Enhancements

- User preference history and personalization
- Playlist creation and sharing
- Social features (follow users, see friends' recommendations)
- Advanced ML models (collaborative filtering, neural networks)
- Music streaming integration (Spotify, Apple Music, YouTube Music)
- Mobile app (React Native)
- Real-time updates with WebSockets

## License

MIT License - Feel free to use this project for learning and personal use!

## Support

For issues, questions, or suggestions, please create an issue in the repository.

---

**Happy music discovering! 🎵**
