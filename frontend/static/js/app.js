// StudyWise AI Frontend JavaScript

class StudyWiseApp {
    constructor() {
        console.log('StudyWiseApp constructor called');
        this.apiBaseUrl = '/api';
        this.authToken = localStorage.getItem('authToken');
        console.log('Auth token found:', !!this.authToken);
        this.init();
    }

    init() {
        console.log('StudyWiseApp initializing...');
        try {
            this.setupEventListeners();
            this.checkAuthStatus();
            this.initializeChat();
            console.log('StudyWiseApp initialization complete');
        } catch (error) {
            console.error('Error during initialization:', error);
        }
    }

    setupEventListeners() {
        console.log('Setting up event listeners...');
        
        // Modal controls with error handling
        const loginBtn = document.getElementById('loginBtn');
        const registerBtn = document.getElementById('registerBtn');
        
        console.log('Found buttons:', { loginBtn: !!loginBtn, registerBtn: !!registerBtn });
        
        if (loginBtn) {
            loginBtn.addEventListener('click', (e) => {
                console.log('Login button clicked');
                e.preventDefault();
                this.openAuthModal('login');
            });
        } else {
            console.error('Login button not found!');
        }
        
        if (registerBtn) {
            registerBtn.addEventListener('click', (e) => {
                console.log('Register button clicked');
                e.preventDefault();
                this.openAuthModal('register');
            });
        } else {
            console.error('Register button not found!');
        }
        
        document.getElementById('askAiBtn')?.addEventListener('click', () => this.openChatModal());
        document.getElementById('dashboardBtn')?.addEventListener('click', () => this.showDashboard());
        document.getElementById('startLearningBtn')?.addEventListener('click', () => this.showDashboard());
        document.getElementById('logoutBtn')?.addEventListener('click', () => this.logout());
        
        document.getElementById('closeChatModal')?.addEventListener('click', () => this.closeChatModal());
        document.getElementById('closeAuthModal')?.addEventListener('click', () => this.closeAuthModal());
        document.getElementById('closeStudyPlanModal')?.addEventListener('click', () => this.closeStudyPlanModal());
        
        // Auth form switching
        document.getElementById('switchToRegister')?.addEventListener('click', () => this.switchAuthMode('register'));
        document.getElementById('switchToLogin')?.addEventListener('click', () => this.switchAuthMode('login'));
        
        // Form submissions
        document.getElementById('loginForm')?.addEventListener('submit', (e) => this.handleLogin(e));
        document.getElementById('registerForm')?.addEventListener('submit', (e) => this.handleRegister(e));
        document.getElementById('studyPlanForm')?.addEventListener('submit', (e) => this.handleCreateStudyPlan(e));
        
        // Chat functionality
        document.getElementById('sendMessage')?.addEventListener('click', () => this.sendChatMessage());
        document.getElementById('chatInput')?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendChatMessage();
        });
        
        // Study Plan Management
        document.getElementById('createStudyPlanBtn')?.addEventListener('click', () => this.openStudyPlanModal());
        document.getElementById('cancelStudyPlan')?.addEventListener('click', () => this.closeStudyPlanModal());
        
        // Quick Actions
        document.getElementById('quickMathBtn')?.addEventListener('click', () => this.startQuickSession('mathematics'));
        document.getElementById('quickScienceBtn')?.addEventListener('click', () => this.startQuickSession('science'));
        document.getElementById('quickLanguageBtn')?.addEventListener('click', () => this.startQuickSession('language'));
        document.getElementById('aiTutorBtn')?.addEventListener('click', () => this.openChatModal());
        
        // Study Timer
        document.getElementById('pauseTimer')?.addEventListener('click', () => this.pauseTimer());
        document.getElementById('stopTimer')?.addEventListener('click', () => this.stopTimer());
        
        // Close modals on backdrop click
        document.getElementById('chatModal')?.addEventListener('click', (e) => {
            if (e.target.id === 'chatModal') this.closeChatModal();
        });
        document.getElementById('authModal')?.addEventListener('click', (e) => {
            if (e.target.id === 'authModal') this.closeAuthModal();
        });
        document.getElementById('studyPlanModal')?.addEventListener('click', (e) => {
            if (e.target.id === 'studyPlanModal') this.closeStudyPlanModal();
        });
    }

    // Authentication Methods
    async handleLogin(e) {
        e.preventDefault();
        
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;
        
        try {
            const formData = new FormData();
            formData.append('username', email);
            formData.append('password', password);
            
            const response = await fetch(`${this.apiBaseUrl}/auth/login`, {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                const data = await response.json();
                this.authToken = data.access_token;
                localStorage.setItem('authToken', this.authToken);
                localStorage.setItem('user', JSON.stringify(data.user));
                
                this.closeAuthModal();
                this.updateUIForLoggedInUser(data.user);
                this.showNotification('Login successful!', 'success');
            } else {
                const error = await response.json();
                this.showNotification('Login failed: ' + error.detail, 'error');
            }
        } catch (error) {
            this.showNotification('Network error during login', 'error');
        }
    }

    async handleRegister(e) {
        e.preventDefault();
        
        const userData = {
            email: document.getElementById('registerEmail').value,
            username: document.getElementById('registerUsername').value,
            password: document.getElementById('registerPassword').value,
            full_name: document.getElementById('registerFullName').value
        };
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });
            
            if (response.ok) {
                const data = await response.json();
                this.showNotification('Registration successful! Please login.', 'success');
                this.switchAuthMode('login');
            } else {
                const error = await response.json();
                this.showNotification('Registration failed: ' + error.detail, 'error');
            }
        } catch (error) {
            this.showNotification('Network error during registration', 'error');
        }
    }

    // Modal Controls
    openChatModal() {
        const modal = document.getElementById('chatModal');
        if (modal) modal.classList.remove('hidden');
    }

    closeChatModal() {
        const modal = document.getElementById('chatModal');
        if (modal) modal.classList.add('hidden');
    }

    openAuthModal(mode = 'login') {
        console.log('Opening auth modal with mode:', mode);
        const authModal = document.getElementById('authModal');
        if (authModal) {
            authModal.classList.remove('hidden');
            this.switchAuthMode(mode);
            console.log('Auth modal opened successfully');
        } else {
            console.error('Auth modal element not found!');
        }
    }

    closeAuthModal() {
        const modal = document.getElementById('authModal');
        if (modal) modal.classList.add('hidden');
    }

    switchAuthMode(mode) {
        const loginForm = document.getElementById('loginForm');
        const registerForm = document.getElementById('registerForm');
        const authTitle = document.getElementById('authTitle');
        
        if (mode === 'login') {
            loginForm.classList.remove('hidden');
            registerForm.classList.add('hidden');
            authTitle.textContent = 'Login to StudyWise AI';
        } else {
            loginForm.classList.add('hidden');
            registerForm.classList.remove('hidden');
            authTitle.textContent = 'Register for StudyWise AI';
        }
    }

    // Chat Functionality
    initializeChat() {
        this.chatMessages = [];
        this.addChatMessage('ai', 'Hello! I\'m your AI study assistant. How can I help you today?');
    }

    async sendChatMessage() {
        const chatInput = document.getElementById('chatInput');
        const message = chatInput.value.trim();
        
        if (!message) return;
        
        // Add user message to chat
        this.addChatMessage('user', message);
        chatInput.value = '';
        
        // Show typing indicator
        this.addChatMessage('ai', 'Thinking...', true);
        
        try {
            if (!this.authToken) {
                this.removeLastMessage();
                this.addChatMessage('ai', 'Please login to use the AI assistant feature.');
                return;
            }
            
            const response = await fetch(`${this.apiBaseUrl}/ai/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.authToken}`
                },
                body: JSON.stringify({
                    message: message,
                    context: null
                })
            });
            
            // Remove typing indicator
            this.removeLastMessage();
            
            if (response.ok) {
                const data = await response.json();
                this.addChatMessage('ai', data.response);
            } else {
                this.addChatMessage('ai', 'Sorry, I couldn\'t process your request right now.');
            }
        } catch (error) {
            this.removeLastMessage();
            this.addChatMessage('ai', 'Network error. Please check your connection.');
        }
    }

    addChatMessage(type, message, isTemp = false) {
        const chatMessages = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${type} p-3 mb-3 rounded-lg ${isTemp ? 'temp-message' : ''}`;
        
        if (type === 'user') {
            messageDiv.classList.add('bg-blue-600', 'text-white', 'ml-8');
        } else {
            messageDiv.classList.add('bg-gray-100', 'text-gray-800', 'mr-8');
        }
        
        messageDiv.textContent = message;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        if (!isTemp) {
            this.chatMessages.push({ type, message, timestamp: new Date() });
        }
    }

    removeLastMessage() {
        const chatMessages = document.getElementById('chatMessages');
        const tempMessage = chatMessages.querySelector('.temp-message');
        if (tempMessage) {
            tempMessage.remove();
        }
    }

    // Study Session Management
    async startQuickStudySession() {
        if (!this.authToken) {
            this.showNotification('Please login to start a study session', 'error');
            return;
        }
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/study-plans/sessions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.authToken}`
                },
                body: JSON.stringify({
                    title: 'Quick Study Session',
                    duration: 25,
                    topics_covered: []
                })
            });
            
            if (response.ok) {
                const session = await response.json();
                this.showNotification('Study session started!', 'success');
                this.startTimer(25 * 60); // 25 minutes in seconds
            } else {
                this.showNotification('Failed to start study session', 'error');
            }
        } catch (error) {
            this.showNotification('Network error', 'error');
        }
    }

    startTimer(seconds) {
        // Simple timer implementation
        let remaining = seconds;
        const timer = setInterval(() => {
            remaining--;
            
            if (remaining <= 0) {
                clearInterval(timer);
                this.showNotification('Study session completed! Great job!', 'success');
            }
        }, 1000);
    }

    // Progress Tracking
    async loadProgressData() {
        if (!this.authToken) return;
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/progress/summary`, {
                headers: {
                    'Authorization': `Bearer ${this.authToken}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                this.updateProgressUI(data);
            }
        } catch (error) {
            console.log('Failed to load progress data:', error);
        }
    }

    updateProgressUI(progressData) {
        // Update progress indicators in the UI
        // This would populate charts, stats, etc.
        console.log('Progress data:', progressData);
    }

    // Reminder Management
    async createReminder(title, message, scheduledTime) {
        if (!this.authToken) {
            this.showNotification('Please login to set reminders', 'error');
            return;
        }
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/reminders/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.authToken}`
                },
                body: JSON.stringify({
                    title: title,
                    message: message,
                    reminder_type: 'study_session',
                    scheduled_time: scheduledTime
                })
            });
            
            if (response.ok) {
                this.showNotification('Reminder set successfully!', 'success');
            } else {
                this.showNotification('Failed to set reminder', 'error');
            }
        } catch (error) {
            this.showNotification('Network error', 'error');
        }
    }

    // Utility Methods
    showNotification(message, type = 'info') {
        // Remove existing notifications
        const existingNotifications = document.querySelectorAll('.notification');
        existingNotifications.forEach(n => n.remove());
        
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type} p-4 rounded-lg shadow-lg`;
        notification.innerHTML = `
            <div class="flex items-center justify-between">
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-xl">&times;</button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Show notification
        setTimeout(() => notification.classList.add('show'), 100);
        
        // Auto hide after 5 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    }

    showUserMenu() {
        // Show user menu with profile, settings, etc.
        // This would open a dropdown or modal
        console.log('Show user menu');
    }

    // API Helper Method
    async apiCall(endpoint, options = {}) {
        const url = `${this.apiBaseUrl}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };
        
        if (this.authToken) {
            config.headers['Authorization'] = `Bearer ${this.authToken}`;
        }
        
        try {
            const response = await fetch(url, config);
            return await response.json();
        } catch (error) {
            console.error('API call failed:', error);
            throw error;
        }
    }

    // Dashboard Management
    showDashboard() {
        if (!this.authToken) {
            this.showNotification('Please login to access your dashboard', 'error');
            this.openAuthModal('login');
            return;
        }
        
        // Hide home sections, show dashboard (if elements exist)
        const heroSection = document.querySelector('.hero, .bg-gradient-to-r.from-blue-600');
        if (heroSection) {
            heroSection.classList.add('hidden');
        }
        const featuresEl = document.getElementById('features');
        if (featuresEl) featuresEl.classList.add('hidden');
        const quickActionsEl = document.querySelector('.quick-actions');
        if (quickActionsEl) quickActionsEl.classList.add('hidden');
        const dashboardEl = document.getElementById('dashboard');
        if (dashboardEl) dashboardEl.classList.remove('hidden');
        
        // Load dashboard data
        this.loadStudyPlans();
        this.loadDashboardStats();
    }

    hideDashboard() {
        // Show home sections, hide dashboard (if elements exist)
        const heroSection = document.querySelector('.hero, .bg-gradient-to-r.from-blue-600');
        if (heroSection) {
            heroSection.classList.remove('hidden');
        }
        const featuresEl = document.getElementById('features');
        if (featuresEl) featuresEl.classList.remove('hidden');
        const quickActionsEl = document.querySelector('.quick-actions');
        if (quickActionsEl) quickActionsEl.classList.remove('hidden');
        const dashboardEl = document.getElementById('dashboard');
        if (dashboardEl) dashboardEl.classList.add('hidden');
    }

    updateUIForLoggedInUser(user) {
        const guestSection = document.getElementById('guestSection');
        const userSection = document.getElementById('userSection');
        const usernameEl = document.getElementById('username');
        
        if (guestSection) guestSection.classList.add('hidden');
        if (userSection) userSection.classList.remove('hidden');
        if (usernameEl) usernameEl.textContent = `Welcome, ${user.full_name || user.username}!`;
        
        // Don't auto-show dashboard in bulletproof mode (no dashboard element)
        // Only show dashboard if dashboard element exists
        const dashboardEl = document.getElementById('dashboard');
        if (dashboardEl) {
            this.showDashboard();
        }
    }

    logout() {
        this.authToken = null;
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        
        const userSection = document.getElementById('userSection');
        const guestSection = document.getElementById('guestSection');
        if (userSection) userSection.classList.add('hidden');
        if (guestSection) guestSection.classList.remove('hidden');
        this.hideDashboard();
        this.showNotification('Logged out successfully', 'success');
    }

    // Study Plan Management
    openStudyPlanModal() {
        const modal = document.getElementById('studyPlanModal');
        if (modal) modal.classList.remove('hidden');
    }

    closeStudyPlanModal() {
        const modal = document.getElementById('studyPlanModal');
        const form = document.getElementById('studyPlanForm');
        if (modal) modal.classList.add('hidden');
        if (form) form.reset();
    }

    async handleCreateStudyPlan(e) {
        e.preventDefault();
        
        if (!this.authToken) {
            this.showNotification('Please login first', 'error');
            return;
        }

        const titleEl = document.getElementById('planTitle');
        const subjectEl = document.getElementById('planSubject');
        const difficultyEl = document.getElementById('planDifficulty');
        const durationEl = document.getElementById('planDuration');
        const descriptionEl = document.getElementById('planDescription');
        
        if (!titleEl || !subjectEl || !difficultyEl || !durationEl) {
            console.error('Study plan form elements not found');
            return;
        }

        const formData = {
            title: titleEl.value,
            subject: subjectEl.value,
            difficulty_level: difficultyEl.value,
            estimated_duration: parseInt(durationEl.value) * 60, // Convert to minutes
            description: descriptionEl ? descriptionEl.value : ''
        };

        try {
            const response = await fetch(`${this.apiBaseUrl}/study-plans/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.authToken}`
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                const studyPlan = await response.json();
                this.closeStudyPlanModal();
                this.showNotification('Study plan created successfully!', 'success');
                this.loadStudyPlans(); // Refresh the list
            } else {
                throw new Error('Failed to create study plan');
            }
        } catch (error) {
            this.showNotification('Failed to create study plan. Please try again.', 'error');
        }
    }

    async loadStudyPlans() {
        if (!this.authToken) return;

        try {
            const response = await fetch(`${this.apiBaseUrl}/study-plans/`, {
                headers: {
                    'Authorization': `Bearer ${this.authToken}`
                }
            });

            if (response.ok) {
                const studyPlans = await response.json();
                this.displayStudyPlans(studyPlans);
            }
        } catch (error) {
            console.error('Failed to load study plans:', error);
        }
    }

    displayStudyPlans(studyPlans) {
        const container = document.getElementById('studyPlansList');
        if (!container) {
            console.log('studyPlansList element not found, skipping display');
            return;
        }
        
        if (studyPlans.length === 0) {
            container.innerHTML = `
                <div class="text-center text-gray-500 py-8">
                    <div class="text-4xl mb-4">📚</div>
                    <p>No study plans yet. Create your first one to get started!</p>
                </div>
            `;
            return;
        }

        container.innerHTML = studyPlans.map(plan => `
            <div class="bg-white p-4 rounded-lg border-l-4 border-blue-500 shadow-sm">
                <div class="flex justify-between items-start">
                    <div class="flex-1">
                        <h4 class="font-semibold text-gray-800 mb-1">${plan.title}</h4>
                        <p class="text-sm text-gray-600 mb-2">${plan.description || ''}</p>
                        <div class="flex space-x-4 text-xs text-gray-500">
                            <span>📚 ${plan.subject}</span>
                            <span>⭐ ${plan.difficulty_level}</span>
                            <span>⏱️ ${Math.floor(plan.estimated_duration / 60)}h/week</span>
                        </div>
                    </div>
                    <div class="flex space-x-2">
                        <button onclick="studyWiseApp.startStudySession(${plan.id})" 
                                class="bg-green-500 text-white px-3 py-1 rounded text-sm hover:bg-green-600">
                            ▶️ Start
                        </button>
                        <button onclick="studyWiseApp.viewStudyPlan(${plan.id})" 
                                class="bg-blue-500 text-white px-3 py-1 rounded text-sm hover:bg-blue-600">
                            👁️ View
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    }

    async loadDashboardStats() {
        if (!this.authToken) return;
        
        const statsEl = document.getElementById('dashboardStats');
        if (!statsEl) {
            console.log('dashboardStats element not found, skipping stats load');
            return;
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}/progress/summary`, {
                headers: {
                    'Authorization': `Bearer ${this.authToken}`
                }
            });

            if (response.ok) {
                const stats = await response.json();
                statsEl.textContent = 
                    `📊 ${stats.total_sessions || 0} sessions completed • ⏱️ ${Math.floor((stats.total_time || 0) / 60)} hours studied`;
            }
        } catch (error) {
            statsEl.textContent = 'Welcome to your learning dashboard!';
        }
    }

    // Study Session Management
    async startQuickSession(subject) {
        if (!this.authToken) {
            this.showNotification('Please login to start a study session', 'error');
            this.openAuthModal('login');
            return;
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}/study-plans/sessions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.authToken}`
                },
                body: JSON.stringify({
                    title: `Quick ${subject.charAt(0).toUpperCase() + subject.slice(1)} Study`,
                    planned_duration: 30,
                    subject: subject
                })
            });

            if (response.ok) {
                const session = await response.json();
                this.showNotification(`Study session started! Focus on ${subject} for 30 minutes.`, 'success');
                this.startTimer(30 * 60); // 30 minutes in seconds
                this.currentSessionId = session.id;
            } else {
                throw new Error('Failed to start session');
            }
        } catch (error) {
            this.showNotification('Failed to start study session', 'error');
        }
    }

    async startStudySession(planId) {
        if (!this.authToken) {
            this.showNotification('Please login first', 'error');
            return;
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}/study-plans/${planId}/sessions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.authToken}`
                },
                body: JSON.stringify({
                    planned_duration: 60 // 1 hour default
                })
            });

            if (response.ok) {
                const session = await response.json();
                this.showNotification('Study session started!', 'success');
                this.startTimer(60 * 60); // 1 hour in seconds
                this.currentSessionId = session.id;
            }
        } catch (error) {
            this.showNotification('Failed to start study session', 'error');
        }
    }

    // Timer Management
    startTimer(seconds) {
        this.timerSeconds = seconds;
        this.timerInterval = setInterval(() => {
            this.updateTimerDisplay();
            this.timerSeconds--;
            
            if (this.timerSeconds < 0) {
                this.completeStudySession();
            }
        }, 1000);
        
        document.getElementById('studyTimer').classList.remove('hidden');
        this.updateTimerDisplay();
    }

    pauseTimer() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
            document.getElementById('pauseTimer').textContent = '▶️';
            document.getElementById('pauseTimer').onclick = () => this.resumeTimer();
        }
    }

    resumeTimer() {
        this.startTimer(this.timerSeconds);
        document.getElementById('pauseTimer').textContent = '⏸️';
        document.getElementById('pauseTimer').onclick = () => this.pauseTimer();
    }

    stopTimer() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
        document.getElementById('studyTimer').classList.add('hidden');
        this.completeStudySession();
    }

    updateTimerDisplay() {
        const minutes = Math.floor(this.timerSeconds / 60);
        const seconds = this.timerSeconds % 60;
        document.getElementById('timerDisplay').textContent = 
            `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    async completeStudySession() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
        document.getElementById('studyTimer').classList.add('hidden');
        
        this.showNotification('Study session completed! Great job!', 'success');
        
        // Update progress if we have a session ID
        if (this.currentSessionId) {
            try {
                await fetch(`${this.apiBaseUrl}/study-plans/sessions/${this.currentSessionId}/complete`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${this.authToken}`
                    }
                });
                this.loadDashboardStats(); // Refresh stats
            } catch (error) {
                console.error('Failed to complete session:', error);
            }
        }
    }

    async viewStudyPlan(planId) {
        // This could open a detailed view modal - for now, just show a notification
        this.showNotification('Detailed study plan view coming soon!', 'info');
    }

    checkAuthStatus() {
        try {
            const user = localStorage.getItem('user');
            if (this.authToken && user) {
                const userData = JSON.parse(user);
                this.updateUIForLoggedInUser(userData);
            }
        } catch (error) {
            console.error('Error checking auth status:', error);
        }
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing StudyWise App...');
    
    try {
        window.studyWiseApp = new StudyWiseApp();
        console.log('StudyWise App initialized successfully');
    } catch (error) {
        console.error('Error initializing StudyWise App:', error);
    }
});