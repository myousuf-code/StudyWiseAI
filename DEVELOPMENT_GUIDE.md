# StudyWiseAI Development Setup Guide

## Quick Start

### 1. Prerequisites
- Python 3.8+ installed
- PostgreSQL database running
- Redis server running (optional for caching)
- OpenAI API key (for AI features)

### 2. Environment Setup

```bash
# Clone or navigate to the project directory
cd StudyWiseAI

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy environment template
copy .env.example .env

# Edit .env file with your actual values:
# - Set your OpenAI API key
# - Configure database connection
# - Set secure secret key
```

### 4. Database Setup

```bash
# Initialize database and create test user
python -m app.core.init_db
```

### 5. Run the Application

```bash
# Start the development server
uvicorn app.main:app --reload

# The application will be available at:
# http://localhost:8000
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Test User Credentials

- **Email**: test@studywiseai.com
- **Password**: testpassword123

## Development Workflow

### Phase 1: Setup & Testing (Current)
- [x] Project structure created
- [x] FastAPI backend configured
- [x] Database models defined
- [x] Authentication system implemented
- [x] AI service integration
- [x] Basic frontend template
- [x] Test the complete setup
- [x] **Study Plans Dashboard implemented**
- [x] **Study session timer with controls**
- [x] **Frontend user interface completed**

### Phase 2: AI Features Enhancement
- [x] Improve AI study plan generation
- [x] Add more AI conversation capabilities  
- [x] Implement learning pattern analysis
- [x] Create quiz generation system

### Phase 3: Frontend Polish (COMPLETED)
- [x] **Add interactive dashboards**
- [x] **Implement real-time features**
- [x] **Add progress visualization**
- [x] **Mobile responsive improvements**

### Phase 4: Advanced Features
- [ ] Smart notification system
- [ ] Study session timer with break reminders
- [ ] Advanced analytics and insights
- [ ] Export/import functionality

### Phase 5: Production Ready
- [ ] Add comprehensive testing
- [ ] Implement proper error handling
- [ ] Security enhancements
- [ ] Performance optimization
- [ ] Deployment configuration

## Key Features Implemented

### Backend (FastAPI)
- ✅ User authentication with JWT
- ✅ Database models for users, study plans, progress, etc.
- ✅ AI integration with OpenAI API
- ✅ RESTful API endpoints for all features
- ✅ WebSocket support for real-time chat

### Frontend (HTML/CSS/JavaScript)
- ✅ Responsive design matching original wireframe
- ✅ Interactive AI chat interface
- ✅ User authentication modals
- ✅ Modern UI with Tailwind CSS
- ✅ Real-time API integration

### AI Capabilities
- ✅ Personalized study plan generation
- ✅ AI study assistant chat
- ✅ Progress analysis and insights
- ✅ Quiz question generation
- ✅ Learning pattern recognition

## Next Steps

1. **Test the complete application**:
   ```bash  
   # Follow the comprehensive frontend test plan
   # See: FRONTEND_TEST_PLAN.md
   
   # Start server
   .\venv\Scripts\Activate.ps1
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
   
   # Open browser to http://localhost:8000
   # Test all features via web interface
   ```

2. **Complete Feature Set Available**:
   - ✅ User Registration & Authentication
   - ✅ AI-Powered Chat Assistant  
   - ✅ Study Plans Management Dashboard
   - ✅ Study Session Timer with Controls
   - ✅ Progress Tracking & Analytics
   - ✅ Responsive Web Design

3. **Testing**: Follow **FRONTEND_TEST_PLAN.md** for comprehensive web-based testing

4. **Production Ready**: All core features implemented and ready for deployment

## Troubleshooting

### Common Issues

1. **Database connection errors**:
   - Make sure PostgreSQL is running
   - Check DATABASE_URL in .env file
   - Verify database credentials

2. **AI features not working**:
   - Ensure OpenAI API key is set correctly
   - Check API key has sufficient credits
   - Verify network connectivity

3. **Frontend not loading**:
   - Check console for JavaScript errors
   - Ensure all static files are properly served
   - Verify API endpoints are responding

## Architecture Overview

```
StudyWiseAI/
├── app/                    # FastAPI backend
│   ├── api/               # API route handlers
│   ├── core/              # Core functionality (auth, config, db)
│   ├── models/            # Database models
│   ├── services/          # Business logic (AI service, etc.)
│   └── main.py           # Application entry point
├── frontend/              # Frontend assets
│   ├── static/           # CSS, JS files
│   └── templates/        # HTML templates
└── requirements.txt      # Python dependencies
```

The application follows a clean architecture with:
- **FastAPI** for the REST API and WebSocket endpoints
- **SQLAlchemy** for database ORM
- **OpenAI API** for AI capabilities
- **JWT** for authentication
- **Modern HTML/CSS/JS** for the frontend

Ready to start development! 🚀