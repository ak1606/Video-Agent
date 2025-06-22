# AI Video Agent - Real-time Voice Chat with Video Responses

A modern, full-stack web application that enables natural voice conversations with an AI agent featuring real-time speech-to-text, intelligent responses powered by Google Gemini 2.0 Flash, and talking video avatars generated with D-ID API.

![Project Demo](https://img.shields.io/badge/Status-Working-brightgreen) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![React](https://img.shields.io/badge/React-19.1.0-blue) ![Django](https://img.shields.io/badge/Django-4.2.7-green)


## 🌟 Features

### 🎤 Voice Input
- **One-click voice activation** with microphone button
- **Real-time speech-to-text** using Web Speech API
- **Visual feedback** with pulsing animations during recording
- **Cross-browser compatibility** (Chrome, Edge, Firefox)

### 🤖 AI Intelligence
- **Google Gemini 2.0 Flash** integration for natural conversations
- **Context-aware responses** maintaining conversation history
- **Fast response times** optimized for real-time interaction
- **Conversation persistence** with SQLite database

### 🎬 Video Responses
- **Talking avatar videos** generated with D-ID API
- **Custom Midjourney avatar** support for personalized experience
- **Automatic video playback** synchronized with text responses
- **Fallback system** with multiple avatar options
- **Real-time video generation** (30-60 seconds)

### 💬 Modern Chat Interface
- **WhatsApp-style message bubbles** for familiar UX
- **Real-time conversation flow** with timestamps
- **Auto-scroll** to latest messages
- **Loading states** and error handling
- **Responsive design** for desktop and mobile

## 🚀 Live Demo

Experience the AI video agent in action:
- **Frontend**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000/api/`
- **API Health Check**: `http://localhost:8000/api/health/`
- **D-ID Credits**: `http://localhost:8000/api/credits/`

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │────│  Django Backend │────│  External APIs  │
│                 │    │                 │    │                 │
│ • Voice Input   │    │ • REST API      │    │ • Google Gemini │
│ • Video Player  │    │ • Conversation  │    │ • D-ID Talking  │
│ • Chat UI       │    │ • AI Integration│    │ • Web Speech    │
│ • Web Speech    │    │ • Video Gen     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 Prerequisites

- **Node.js** 16.0+ and npm
- **Python** 3.8+ and pip
- **Google AI Studio API Key** ([Get one here](https://makersuite.google.com/app/apikey))
- **D-ID API Key** ([Sign up at d-id.com](https://studio.d-id.com/))

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/ak1606/Video-Agent.git
cd Video-Agent
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd talking-agent-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment variables file
# Create .env file with your API keys:
# GOOGLE_API_KEY=your_google_gemini_api_key
# DID_API_KEY=your_did_api_key
# DJANGO_SECRET_KEY=your_django_secret_key
# DEBUG=True

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Start Django server
python manage.py runserver
```

### 3. Frontend Setup
```bash
# Open new terminal and navigate to frontend
cd talking-agent-frontend

# Install dependencies
npm install

# Start React development server
npm start
```

### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin

## 🔧 Configuration

### Environment Variables

Create `.env` file in the backend directory:

```env
# Django Configuration
DJANGO_SECRET_KEY=your_super_secret_key_here
DEBUG=True

# API Keys
GOOGLE_API_KEY=your_google_gemini_api_key
DID_API_KEY=your_did_api_key

# D-ID Configuration
DID_BASE_URL=https://api.d-id.com
```

### Custom Avatar Setup

Replace the default avatar with your custom Midjourney-generated image:

1. Upload your avatar to GitHub or image hosting service
2. Update `default_avatar` in `agent_api/services/did_service.py`:

```python
self.default_avatar = "https://raw.githubusercontent.com/yourusername/yourrepo/main/your-avatar.jpg"
```

## 📁 Project Structure

```
Video-Agent/
├── talking-agent-backend/          # Django Backend
│   ├── talking_agent_backend/      # Main Django project
│   │   ├── settings.py            # Django configuration
│   │   ├── urls.py                # URL routing
│   │   └── wsgi.py                # WSGI config
│   ├── agent_api/                 # Main API app
│   │   ├── models.py              # Database models (Conversation, Message)
│   │   ├── views.py               # API endpoints
│   │   ├── urls.py                # API routes
│   │   ├── admin.py               # Django admin interface
│   │   └── services/              # Business logic
│   │       ├── gemini_service.py  # Google Gemini 2.0 Flash integration
│   │       └── did_service.py     # D-ID video generation service
│   ├── requirements.txt           # Python dependencies
│   ├── manage.py                  # Django management script
│   ├── .env                       # Environment variables (not in repo)
│   └── db.sqlite3                 # SQLite database (generated)
├── talking-agent-frontend/         # React Frontend
│   ├── src/
│   │   ├── components/            # React components
│   │   │   ├── TalkingAgent.js    # Main container component
│   │   │   ├── VoiceInput.js      # Voice recording & speech-to-text
│   │   │   ├── VideoPlayer.js     # D-ID video playback
│   │   │   ├── ChatInterface.js   # Chat messages & history
│   │   │   └── *.css              # Component styling
│   │   ├── App.js                 # Root component
│   │   └── index.js               # Entry point
│   ├── package.json               # Node dependencies
│   ├── public/                    # Static assets
│   └── build/                     # Production build (generated)
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

## 🔌 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/process-voice/` | Process voice input and generate AI response |
| `GET` | `/api/health/` | Health check endpoint |
| `GET` | `/api/credits/` | Check D-ID API credits remaining |

### Request/Response Examples

**Process Voice Input:**
```bash
curl -X POST http://localhost:8000/api/process-voice/ \
  -H "Content-Type: application/json" \
  -d '{
    "transcript": "Hello, how are you today?",
    "session_id": "session_123"
  }'
```

**Response:**
```json
{
  "session_id": "session_123",
  "agent_response": "Hello! I'm doing great, thank you for asking. How can I help you today?",
  "video_url": "https://d-id-talks-prod.s3.amazonaws.com/...",
  "video_generation_success": true,
  "timestamp": "2025-06-04T08:15:30.123456+00:00"
}
```

## 🎯 Usage Guide

### Basic Conversation Flow

1. **Click the microphone button** to start recording
2. **Speak your message** - you'll see real-time transcription
3. **Wait for AI processing** - loading indicator shows progress
4. **Watch the AI respond** - both text and video will appear
5. **Continue the conversation** - full history is maintained

### Voice Input Tips

- **Speak clearly** for better speech recognition
- **Use Chrome or Edge** for best Web Speech API support
- **Grant microphone permissions** when prompted
- **Keep sentences concise** for faster processing

### Troubleshooting

| Issue | Solution |
|-------|----------|
| No microphone access | Check browser permissions and HTTPS |
| Speech not recognized | Ensure microphone is working, try Chrome/Edge |
| Video not generating | Check D-ID credits and API key |
| Slow responses | Check internet connection and API quotas |

## 🔬 Technical Details

### Frontend Technologies
- **React 19.1.0** - Latest React with improved performance
- **Web Speech API** - Browser-native speech recognition
- **CSS Grid/Flexbox** - Modern responsive layout system
- **Lucide React** - Modern icon library
- **Create React App** - Zero-config React setup

### Backend Technologies
- **Django 4.2.7** - Robust Python web framework
- **Django REST Framework 3.14.0** - API development toolkit
- **Google Generative AI 0.3.1** - Gemini 2.0 Flash integration
- **SQLite** - Lightweight development database
- **CORS Headers** - Cross-origin request handling

### External APIs
- **Google Gemini 2.0 Flash** - Advanced conversational AI
- **D-ID Talking Heads API** - Real-time video avatar generation
- **Web Speech API** - Browser speech-to-text conversion

## 🚀 Deployment

### Production Deployment

1. **Environment Setup:**
   - Set `DEBUG=False` in production
   - Use PostgreSQL instead of SQLite
   - Configure proper CORS settings
   - Set secure Django secret key

2. **Frontend Build:**
   ```bash
   cd talking-agent-frontend
   npm run build
   ```

3. **Backend Deployment:**
   ```bash
   pip install gunicorn
   gunicorn talking_agent_backend.wsgi:application
   ```

### Docker Deployment (Optional)

```dockerfile
# Dockerfile example for backend
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "talking_agent_backend.wsgi:application"]
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**: `https://github.com/ak1606/Video-Agent`
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint for JavaScript code
- Write descriptive commit messages
- Add tests for new features
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Google AI** for Gemini 2.0 Flash API
- **D-ID** for talking avatar technology
- **OpenAI** for inspiring conversational AI interfaces
- **React Team** for the amazing frontend framework
- **Django Team** for the robust backend framework

## 📞 Support

Having issues? Here's how to get help:

- **Check the [Issues](https://github.com/ak1606/Video-Agent/issues)** page
- **Read the troubleshooting guide** above
- **Create a new issue** with detailed description
- **Join our community** discussions

## 🔮 Roadmap

### Upcoming Features
- [ ] **Multi-language support** for global accessibility
- [ ] **Voice cloning** for personalized AI voices
- [ ] **Mobile app** for iOS and Android
- [ ] **Real-time translation** for cross-language conversations
- [ ] **Conversation analytics** and insights
- [ ] **Custom AI personalities** and character selection
- [ ] **Group conversations** with multiple participants
- [ ] **Voice commands** for hands-free operation

### Version History
- **v1.0.0** - Initial release with voice chat and video responses
- **v0.9.0** - Beta release with D-ID integration
- **v0.8.0** - Alpha release with Gemini AI integration
- **v0.5.0** - Basic voice input and text responses

---

**Built with ❤️ by [ak1606](https://github.com/ak1606)**

*Star ⭐ this repo if you found it helpful!*

## 🔗 Repository

- **GitHub**: https://github.com/ak1606/Video-Agent
- **Issues**: https://github.com/ak1606/Video-Agent/issues
- **Discussions**: https://github.com/ak1606/Video-Agent/discussions

