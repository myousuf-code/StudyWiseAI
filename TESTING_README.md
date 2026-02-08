# 🧪 StudyWiseAI Testing Guide

## Quick Start Testing

### Option 1: Fully Automated (Recommended)
```powershell
cd C:\Code\StudyWiseAI
.\venv\Scripts\Activate.ps1
python run_tests.py
```
Choose option 1 for complete automated testing.

### Option 2: Manual Testing
```powershell
# Terminal 1: Start server
cd C:\Code\StudyWiseAI
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Run tests
cd C:\Code\StudyWiseAI
.\venv\Scripts\Activate.ps1
python quick_test.py
```

## Test Files Overview

| File | Purpose | Duration |
|------|---------|----------|
| `run_tests.py` | Automated test runner with server management | 3-5 min |
| `quick_test.py` | Comprehensive feature testing | 2-3 min |
| `test_ai_direct.py` | AI features testing | 1-2 min |
| `test_direct_auth.py` | Authentication testing | 30 sec |
| `test_fastapi_direct.py` | API endpoint testing | 30 sec |
| `TEST_PLAN.md` | Detailed manual testing guide | 15-30 min |

## Expected Results

### ✅ Success Indicators
- "All tests passed!" messages
- AI model loads successfully
- Authentication works
- Website loads at http://localhost:8000
- Success rate > 90%

### ⚠️ Common Issues
- **Port 8000 in use**: Use `run_tests.py` (auto-kills existing servers)
- **AI model slow**: First download takes ~5 minutes
- **Memory usage**: AI model needs ~2GB RAM

## Test Categories

1. **Authentication** - User registration/login
2. **AI Features** - Chat, study plans, quizzes
3. **Frontend** - Website functionality
4. **API Endpoints** - Backend services
5. **Database** - Data persistence

## Manual Testing (Website)

1. Go to http://localhost:8000
2. Register new account
3. Login with credentials
4. Click "Ask AI Assistant"
5. Chat with AI: "Help me study Python"
6. Verify AI responds appropriately

## Troubleshooting

### Server Won't Start
```powershell
netstat -ano | findstr :8000
Stop-Process -Id [PID] -Force
```

### AI Model Issues
- Ensure 2GB+ free disk space
- Check internet connection for first download
- AI responses take 5-15 seconds (normal)

### Database Problems
```powershell
rm studywiseai.db
python test_direct_auth.py
```

## Test Reports

Results saved to console output. Look for:
- **Authentication**: ✅ All direct authentication tests passed!
- **AI Features**: ✅ Test user authenticated successfully
- **Overall**: Success rate 90%+

## Next Steps After Testing

If tests pass (>90% success rate):
- ✅ Application is ready for use
- ✅ AI features fully functional
- ✅ Can deploy for students

If tests fail:
- 🔧 Check TEST_PLAN.md troubleshooting section
- 🔧 Review error messages
- 🔧 Ensure all prerequisites installed

## Production Checklist

- [ ] All tests pass
- [ ] AI responses appropriate
- [ ] Website loads correctly
- [ ] User registration works
- [ ] Data persists between sessions
- [ ] Performance acceptable

Ready to help students learn with AI! 🎓