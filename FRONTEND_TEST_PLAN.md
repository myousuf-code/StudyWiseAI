# StudyWiseAI - Frontend Web Testing Plan

## 📋 Overview
This test plan focuses exclusively on testing all features through the web interface. No backend or API testing required - all tests are performed by interacting with the webpage directly.

## 🚀 Prerequisites

### 1. Start the Server
```powershell
cd C:\Code\StudyWiseAI
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 2. Open Web Browser
- Navigate to: **http://localhost:8000**
- Use browser developer tools (F12) to monitor console for errors

---

## ✅ **FRONTEND TEST CATEGORIES**

## **1. USER AUTHENTICATION TESTING**

### **Test 1.1: User Registration Flow**
1. **Access Registration:**
   - Click "Register" button in top navigation
   - ✅ Verify registration modal opens
   - ✅ Check all form fields are visible and labeled

2. **Complete Registration:**
   - Fill form:
     - Full Name: `Test User`
     - Username: `testuser2026`
     - Email: `testuser2026@example.com`
     - Password: `TestPass123!`
   - Click "Register" button
   - ✅ Verify success message appears
   - ✅ Verify modal closes automatically
   - ✅ Confirm navigation changes to logged-in state

### **Test 1.2: User Login Flow**
1. **Login with Existing Account:**
   - If logged in, logout first
   - Click "Login" button
   - Use existing credentials:
     - Email: `fresh1234@example.com`
     - Password: `freshpass123`
   - ✅ Verify successful login
   - ✅ Check dashboard becomes accessible

### **Test 1.3: Navigation State Changes**
1. **Logged-Out State:**
   - ✅ "Login" and "Register" buttons visible
   - ✅ Dashboard button hidden
   - ✅ "Start Learning" shows login prompt

2. **Logged-In State:**
   - ✅ Welcome message with username displayed
   - ✅ "Dashboard" and "Logout" buttons visible
   - ✅ Login/Register buttons hidden
   - ✅ Dashboard automatically opens

---

## **2. STUDY PLANS DASHBOARD TESTING**

### **Test 2.1: Dashboard Access & Layout**
1. **Dashboard Visibility:**
   - Login first if not already logged in
   - ✅ Dashboard section automatically displays after login
   - ✅ Hero section and features section are hidden
   - ✅ Welcome message shows correct username

2. **Dashboard Components:**
   - ✅ Dashboard header with welcome message and stats
   - ✅ "Create New Study Plan" button visible and styled
   - ✅ Quick action buttons (Math, Science, Language, AI Tutor) displayed
   - ✅ Study plans list section present
   - ✅ Initial empty state message if no plans exist

### **Test 2.2: Study Plan Creation**
1. **Open Creation Modal:**
   - Click "➕ Create New Study Plan" button
   - ✅ Study plan creation modal opens
   - ✅ All form fields visible and properly labeled

2. **Create Study Plan:**
   - Fill form:
     - Plan Title: `Master JavaScript Programming`
     - Subject: Select `Programming`
     - Difficulty Level: Select `Intermediate`
     - Study Duration: `8` hours per week
     - Description: `Learn modern JavaScript concepts and frameworks`
   - Click "🤖 Create with AI"
   - ✅ Verify success message appears
   - ✅ Modal closes automatically
   - ✅ New study plan appears in the list

3. **Create Multiple Study Plans:**
   - Repeat creation process for:
     - `Advanced Calculus` (Mathematics, Advanced, 10 hours/week)
     - `Spanish Conversation` (Language, Beginner, 5 hours/week)
   - ✅ Verify all plans display correctly in the list

### **Test 2.3: Study Plans Display & Management**
1. **Plans List Display:**
   - ✅ Each study plan shows title, description, subject, difficulty, duration
   - ✅ Color-coded left border for visual separation
   - ✅ Action buttons (▶️ Start, 👁️ View) present for each plan
   - ✅ Proper formatting and alignment

2. **Plan Actions:**
   - Click "▶️ Start" on a study plan
   - ✅ Success message appears
   - ✅ Study timer appears in bottom-right corner
   - Click "👁️ View" on a study plan
   - ✅ Info message appears (feature coming soon)

---

## **3. STUDY SESSION TIMER TESTING**

### **Test 3.1: Quick Study Sessions**
1. **Start Math Session:**
   - Click "Quick Math Study" button
   - ✅ Success message confirms session started
   - ✅ Timer appears in bottom-right corner
   - ✅ Timer shows "30:00" initially
   - ✅ Timer counts down every second

2. **Timer Controls:**
   - Click pause button (⏸️)
   - ✅ Timer pauses, button changes to play (▶️)
   - Click play button
   - ✅ Timer resumes countdown
   - Click stop button (⏹️)
   - ✅ Timer disappears, completion message shows

3. **Test Other Quick Actions:**
   - Try "Science Review", "Language Practice" buttons
   - ✅ Each starts appropriate 30-minute timer
   - ✅ Success messages are subject-specific

### **Test 3.2: Full Study Plan Sessions**
1. **Start From Study Plan:**
   - Click "▶️ Start" on any created study plan
   - ✅ Timer starts with 60-minute duration
   - ✅ Success message references the specific plan
   
2. **Session Completion:**
   - Let timer run down to 00:00 OR click stop
   - ✅ Completion message appears
   - ✅ Timer disappears automatically
   - ✅ Dashboard stats should update (if visible)

---

## **4. AI CHAT ASSISTANT TESTING**

### **Test 4.1: AI Chat Access**
1. **Open Chat Modal:**
   - Must be logged in first
   - Click "💬 Ask AI Assistant" or "AI Tutor" button
   - ✅ Chat modal opens with welcome message
   - ✅ Input field and send button present

2. **AI Interaction:**
   - Type: `"Help me with calculus derivatives"`
   - Click send or press Enter
   - ✅ Message appears in chat as "user" message
   - ✅ "AI is thinking..." indicator shows
   - ⏱️ Wait 10-30 seconds for AI response
   - ✅ AI response appears with helpful content
   - ✅ Conversation history preserved

3. **Study-Related Questions:**
   - Test various questions:
     - `"Create a study schedule for programming"`
     - `"What are the best memory techniques?"`
     - `"Explain photosynthesis in simple terms"`
   - ✅ Each receives relevant, helpful AI responses
   - ✅ No error messages or failures

---

## **5. NAVIGATION & UX TESTING**

### **Test 5.1: Modal Interactions**
1. **Modal Opening/Closing:**
   - Test all modals (Login/Register, Chat, Study Plan Creation)
   - ✅ Modals open with proper backdrop
   - ✅ Close button (×) works for each modal
   - ✅ Clicking outside modal closes it
   - ✅ ESC key closes modals (if implemented)

2. **Form Validation:**
   - Try submitting empty forms
   - ✅ Required field validation works
   - Try invalid email formats
   - ✅ Email validation prevents submission
   - ✅ Error messages are clear and helpful

### **Test 5.2: Responsive Design**
1. **Desktop View (1920x1080):**
   - ✅ All elements properly sized and spaced
   - ✅ Dashboard grid displays correctly (4 columns)
   - ✅ Modals are centered and appropriately sized

2. **Tablet View (768px):**
   - Resize browser window to tablet size
   - ✅ Navigation collapses appropriately
   - ✅ Dashboard maintains usability
   - ✅ Modals remain functional

3. **Mobile View (375px):**
   - Resize to mobile width
   - ✅ All content remains accessible
   - ✅ Buttons are tap-friendly
   - ✅ Text remains readable

---

## **6. ERROR HANDLING & EDGE CASES**

### **Test 6.1: Network Scenarios**
1. **Server Restart During Use:**
   - Stop the server (`Ctrl+C` in terminal)
   - Try creating a study plan or sending chat message
   - ✅ Error messages appear instead of silent failure
   - ✅ User is informed about connection issues
   - Restart server and test recovery

2. **Invalid Data Handling:**
   - Try extremely long study plan titles (500+ characters)
   - Try negative numbers in duration fields
   - ✅ Forms handle edge cases gracefully
   - ✅ No JavaScript console errors

### **Test 6.2: Authentication Edge Cases**
1. **Session Expiration:**
   - Stay logged in for extended period
   - Try performing actions after potential token expiry
   - ✅ Graceful handling of expired sessions
   - ✅ User prompted to re-login if needed

2. **Logout Behavior:**
   - Click logout button
   - ✅ Returns to homepage view
   - ✅ Dashboard becomes inaccessible
   - ✅ All user data cleared from display

---

## **7. PERFORMANCE & USABILITY**

### **Test 7.1: Load Times & Responsiveness**
1. **Page Load:**
   - Fresh browser tab to http://localhost:8000
   - ✅ Page loads within 2-3 seconds
   - ✅ All styles and scripts load properly
   - ✅ No missing images or broken elements

2. **Action Responsiveness:**
   - ✅ Button clicks respond immediately (<100ms visual feedback)
   - ✅ Form submissions show loading states
   - ✅ AI chat shows "thinking" indicator during processing

### **Test 7.2: User Experience Flow**
1. **New User Journey:**
   - Fresh browser session
   - Register → Login → Create Study Plan → Start Session → Use AI Chat
   - ✅ Smooth flow between all features
   - ✅ Clear navigation and feedback at each step
   - ✅ No confusing states or dead ends

2. **Returning User Journey:**
   - Login → Dashboard shows existing plans → Start session → Continue studying
   - ✅ Quick access to existing content
   - ✅ Progress and history preserved

---

## **8. BROWSER COMPATIBILITY**

### **Test 8.1: Cross-Browser Testing**
Test in multiple browsers:

1. **Chrome/Chromium:**
   - ✅ All features work correctly
   - ✅ No console errors

2. **Firefox:**
   - ✅ Consistent appearance and behavior
   - ✅ All modals and interactions function

3. **Edge:**
   - ✅ Complete feature compatibility
   - ✅ Timer and AI chat work properly

---

## **📊 SUCCESS CRITERIA**

### **✅ PASS CONDITIONS**
- [ ] User can register and login successfully
- [ ] Dashboard displays and functions correctly when logged in
- [ ] Study plans can be created, displayed, and managed
- [ ] Study timer works with pause/stop functionality
- [ ] AI chat provides helpful responses within reasonable time
- [ ] All modals open/close properly
- [ ] No JavaScript errors in browser console
- [ ] Responsive design works on different screen sizes
- [ ] Error handling provides clear user feedback

### **❌ FAIL CONDITIONS**
- Unable to complete user registration or login
- Dashboard doesn't appear or is non-functional after login
- Study plan creation fails or plans don't display
- Study timer doesn't start or control buttons don't work
- AI chat fails to respond or shows errors
- Modals don't open/close or overlay incorrectly
- JavaScript console shows errors during normal use
- Site is unusable on mobile or tablet sizes
- Users receive unclear error messages or system fails silently

---

## **🎯 QUICK VALIDATION CHECKLIST (5 minutes)**

For rapid functionality verification:

1. **✅ Core Flow:**
   - [ ] Register new user → Login → Dashboard opens
   - [ ] Create study plan → Plan appears in list
   - [ ] Start timer → Timer counts down correctly
   - [ ] Send AI message → Get response

2. **✅ Visual Check:**
   - [ ] All buttons and text properly styled
   - [ ] Modals display correctly
   - [ ] Dashboard layout looks professional
   - [ ] No broken layouts or missing elements

3. **✅ Interaction Check:**
   - [ ] All buttons clickable and responsive
   - [ ] Forms accept input and submit correctly
   - [ ] Navigation between states works smoothly
   - [ ] Timer controls function properly

---

## **🚀 TESTING TIPS**

### **Best Practices:**
- **Use Browser DevTools (F12)** to monitor console for errors
- **Test in private/incognito mode** to simulate fresh user experience
- **Clear browser data** between major test runs
- **Take screenshots** of any issues for debugging
- **Test with deliberate mistakes** (wrong passwords, empty forms) to verify error handling
- **Try edge cases** (very long text, special characters) to ensure robustness

### **If Tests Fail:**
1. **Check browser console** for JavaScript errors
2. **Verify server is running** and accessible at http://localhost:8000
3. **Try refreshing the page** to clear any cached issues
4. **Test in different browser** to isolate browser-specific issues
5. **Check network tab** in DevTools to see if API calls are failing

Your StudyWiseAI application should provide a smooth, complete study management experience entirely through the web interface! 🎓