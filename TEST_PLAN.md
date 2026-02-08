# StudyWiseAI - Comprehensive Test Plan

## 📋 Overview
This test plan will guide you through testing all features of your StudyWiseAI application systematically.

## 🚀 Prerequisites

### 1. Start the Server
```powershell
cd C:\Code\StudyWiseAI
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 2. Verify Server is Running
- Open browser: http://localhost:8000
- Should see StudyWiseAI homepage
- Check terminal shows: "Application startup complete"

---

## ✅ Test Categories

## 1. AUTHENTICATION TESTING

### Test 1.1: Direct Authentication Test
```powershell
python test_direct_auth.py
```
**Expected Results:**
- ✅ Database initialized
- ✅ Password hashed successfully 
- ✅ Password verification: True
- ✅ Database connected
- ✅ User created successfully
- ✅ Test user cleaned up
- 🎉 All direct authentication tests passed!

### Test 1.2: API Authentication Test
```powershell
python test_fastapi_direct.py
```
**Expected Results:**
- ✅ Root endpoint works
- ✅ Registration successful!
- Response Status: 200

### Test 1.3: Manual Website Registration
1. Go to http://localhost:8000
2. Click "Register" button
3. Fill in registration form:
   - Full Name: Fresh Test User
   - Username: fresh1234
   - Email: fresh1234@example.com
   - Password:     
4. Click "Register"
5. Should see success message
6. Try logging in with same credentials (Email: fresh1234@example.com, Password: freshpass123)

### Test 1.4: Comprehensive Login Security Test
```powershell
python test_login_comprehensive.py
```
**Expected Results:**
- ✅ Server is running
- ✅ Test user registered successfully  
- ✅ Valid login test passed
- ✅ Invalid email format test passed (correctly rejected)
- ✅ Wrong password test passed (correctly rejected)
- ✅ Non-existent user test passed (correctly rejected)
- ✅ Empty credentials test passed (correctly rejected)
- ✅ Malformed JSON test passed (correctly rejected)
- ✅ SQL injection protection test passed
- ✅ Case sensitivity test passed
- ✅ Token validity test passed
- 📊 Success Rate: 90%+

**What This Test Covers:**
- Valid login with correct credentials
- Invalid email formats and edge cases
- Wrong password attempts
- Non-existent user login attempts  
- Empty/missing credential handling
- Malformed JSON request handling
- SQL injection attack prevention
- Email case sensitivity behavior
- JWT token validity for protected endpoints

---

## 2. AI FEATURES TESTING

### Test 2.1: Comprehensive AI Features Test
```powershell
python test_ai_direct.py
```
**Expected Results:**
- ✅ Test user authenticated successfully
- ✅ AI Chat Assistant: 4/4 responses received
- ✅ Study Plan Generation: Generated for subjects
- ✅ Quiz Generation: Generated for topics  
- ✅ Progress Insights: Generated successfully
- ✅ Chat History: Retrieved messages
- ✅ Frontend Website: Home page loads
- 📊 Overall Integration: 90%+ success rate
- ⏱️ Response Times: 10-25 seconds per AI request (normal for local AI)

### Test 2.2: Manual AI Chat Testing
1. Open website: http://localhost:8000
2. Log in with test account
3. Click "Ask AI Assistant" button
4. Test these questions:
   - "How can I improve my study habits?"
   - "Create a study plan for Python programming"
   - "Generate quiz questions about mathematics"
   - "What's the best way to stay focused?"
5. Verify AI responses are helpful and relevant

**⚠️ TROUBLESHOOTING "Stuck on Thinking":**
- AI responses typically take 10-15 seconds (normal for local CPU processing)
- If stuck longer than 30 seconds, refresh page and try simpler questions
- Test with shorter questions first (e.g., "Hi" or "What is 2+2?")

### Test 2.3: AI Response Speed Test
```powershell
python test_ai_speed.py
```
**Expected Results:**
- ✅ Server is running
- ✅ Logged in successfully
- ✅ Simple questions: 5-10 seconds
- ✅ Complex questions: 15-25 seconds
- 📊 Average Response Time: 10-20s (acceptable for local AI)

**What This Test Covers:**
- AI response time measurement
- Different question complexities
- Timeout detection (>30s indicates issues)
- Performance benchmarking for user expectations

---

## 3. FRONTEND TESTING

### Test 3.1: Homepage Features
- [ ] Navigation bar displays correctly
- [ ] Hero section loads with proper styling
- [ ] Quick action buttons are clickable
- [ ] Features section shows all AI capabilities
- [ ] Footer contains proper links

### Test 3.2: User Interface
- [ ] Login modal opens and closes
- [ ] Registration modal opens and closes  
- [ ] Chat modal opens and closes
- [ ] Forms accept input properly
- [ ] Buttons respond to clicks
- [ ] Mobile responsiveness works

### Test 3.3: User Flow
1. **New User Registration:**
   - Register → Login → Use AI Chat → Logout
2. **Returning User:**
   - Login → View Progress → Set Reminder → Use AI Features
3. **Study Session:**
   - Start Quick Study → Chat with AI → Complete Session

---

## 4. API ENDPOINTS TESTING

### Test 4.1: Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - User profile (requires auth)

### Test 4.2: AI Endpoints  
- `POST /api/ai/chat` - AI chat assistant
- `POST /api/ai/generate-study-plan` - Study plan creation
- `POST /api/ai/generate-quiz` - Quiz generation
- `GET /api/ai/progress-insights` - Progress analysis
- `GET /api/ai/chat-history` - Chat history retrieval

### Test 4.3: Study Management Endpoints
- `POST /api/study-plans/` - Create study plan
- `GET /api/study-plans/` - List study plans
- `POST /api/study-plans/sessions` - Start study session
- `GET /api/progress/summary` - Progress summary

---

## 5. DATABASE TESTING

### Test 5.1: Data Persistence
```powershell
# Check database file exists
ls studywiseai.db

# Verify tables were created
python -c "from app.models.database import *; from app.core.database import engine; print(engine.table_names())"
```

### Test 5.2: User Data Storage
1. Register new user
2. Log in and use AI features
3. Log out and log back in
4. Verify chat history is preserved
5. Verify user preferences are saved

---

## 6. AI MODEL TESTING

### Test 6.1: Model Loading
**First Run (Model Download):**
- Should see: "Loading local AI model (this may take a few minutes on first run)..."
- Download progress for Orca Mini model (~2GB)
- Eventually: "✅ Local AI model loaded successfully!"

**Subsequent Runs:**
- Should load much faster
- Model cached locally in `~/.cache/gpt4all/`

### Test 6.2: AI Response Quality
Test various question types:
- [ ] **Study Help:** "How do I memorize vocabulary better?"
- [ ] **Subject Questions:** "Explain photosynthesis simply"
- [ ] **Study Planning:** "Create a 4-week math study plan"
- [ ] **Motivation:** "I'm struggling to stay focused, help me"

---

## 7. PERFORMANCE TESTING

### Test 7.1: Response Times
- Homepage load: < 2 seconds
- AI chat response: 5-15 seconds (normal for local AI)
- User registration: < 3 seconds
- Database queries: < 1 second

### Test 7.2: Memory Usage
Monitor system resources during:
- AI model loading
- Multiple AI conversations
- Extended usage sessions

---

## 8. ERROR HANDLING TESTING

### Test 8.1: Invalid Inputs
- Try invalid email formats
- Use very short passwords
- Send empty messages to AI
- Access protected endpoints without auth

### Test 8.2: Network Issues
- Stop server during chat session
- Test with slow internet connection
- Verify proper error messages displayed

---

## 🎯 QUICK TEST SEQUENCE (5 minutes)

For a rapid functionality check:

```powershell
# 1. Start server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# 2. Run comprehensive tests (new terminal)
python test_ai_direct.py
python test_login_comprehensive.py
python test_ai_speed.py

# 3. Check website manually
# Open: http://localhost:8000
# Register → Login → Chat with AI

# 4. Verify core features work
```

---

## 📊 SUCCESS CRITERIA

### ✅ PASS CONDITIONS
- [ ] All test scripts complete without errors
- [ ] AI responses are generated successfully  
- [ ] User authentication works properly
- [ ] Website loads and functions correctly
- [ ] Database operations succeed
- [ ] AI model loads and responds

### ❌ FAIL CONDITIONS
- Authentication errors prevent login
- AI model fails to load or respond
- Database connection issues
- Frontend doesn't load properly
- API endpoints return 500 errors

---

## 🔧 TROUBLESHOOTING

### Common Issues & Solutions

**Server Won't Start:**
```powershell
# Check if port 8000 is in use
netstat -ano | findstr :8000
# Kill processes using port 8000
Stop-Process -Id [PID] -Force
```

**AI Model Won't Load:**
- Ensure ~2GB free disk space
- Check internet connection for initial download
- Delete `~/.cache/gpt4all/` and retry

**Authentication Errors:**
```powershell
# Reset database
rm studywiseai.db
python test_direct_auth.py
```

**Frontend Issues:**
- Clear browser cache
- Check browser console for JavaScript errors
- Verify all static files are accessible

---

## 📝 TEST EXECUTION LOG

Use this checklist to track your testing:

### Authentication Tests
- [ ] test_direct_auth.py - PASS/FAIL
- [ ] test_fastapi_direct.py - PASS/FAIL  
- [ ] Manual website login - PASS/FAIL
- [ ] test_login_comprehensive.py - PASS/FAIL

### AI Features Tests
- [ ] test_ai_direct.py - PASS/FAIL
- [ ] test_ai_speed.py - PASS/FAIL
- [ ] Manual AI chat - PASS/FAIL
- [ ] Study plan generation - PASS/FAIL
- [ ] Quiz generation - PASS/FAIL

### Frontend Tests
- [ ] Homepage loads - PASS/FAIL
- [ ] User registration - PASS/FAIL
- [ ] Navigation works - PASS/FAIL
- [ ] Mobile responsive - PASS/FAIL

### Overall Assessment
- **Total Tests:** ___/14
- **Success Rate:** ___%
- **Ready for Production:** YES/NO

---

## 🚀 POST-TESTING

After completing all tests:

1. **Document Issues:** Note any failures or unexpected behaviors
2. **Performance Notes:** Record response times and resource usage
3. **User Experience:** Rate the overall usability (1-10)
4. **Production Readiness:** Decide if ready for deployment

## 🎉 Congratulations!

If all tests pass, your StudyWiseAI application is fully functional with:
- ✅ Complete AI-powered study assistance
- ✅ User authentication and data persistence  
- ✅ Modern web interface
- ✅ Local AI (no API costs)
- ✅ Production-ready features

Your AI study assistant is ready to help students learn more effectively!