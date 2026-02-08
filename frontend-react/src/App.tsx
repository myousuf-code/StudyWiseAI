import React, { useState } from 'react';
import { AuthProvider } from './context/AuthContext';
import Navigation from './components/common/Navigation';
import Hero from './components/common/Hero';
import QuickActions from './components/common/QuickActions';
import LoginForm from './components/auth/LoginForm';
import RegisterForm from './components/auth/RegisterForm';
import ChatModal from './components/chat/ChatModal';
import Notification from './components/common/Notification';
import type { Notification as NotificationType } from './types/index';

function App() {
  const [showLogin, setShowLogin] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [showChat, setShowChat] = useState(false);
  const [notifications, setNotifications] = useState<NotificationType[]>([]);

  const addNotification = (message: string, type: NotificationType['type']) => {
    const notification: NotificationType = {
      id: Date.now().toString(),
      message,
      type,
    };
    setNotifications((prev) => [...prev, notification]);
  };

  const removeNotification = (id: string) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id));
  };

  const handleSwitchToRegister = () => {
    setShowLogin(false);
    setShowRegister(true);
  };

  const handleSwitchToLogin = () => {
    setShowRegister(false);
    setShowLogin(true);
  };

  const handleStartLearning = () => {
    addNotification('Feature coming soon! Opening study session setup...', 'info');
  };

  const handleViewProgress = () => {
    addNotification('Progress dashboard coming soon!', 'info');
  };

  const handleCreatePlan = () => {
    addNotification('Study planner coming soon!', 'info');
  };

  return (
    <AuthProvider>
      <div className="min-h-screen bg-gray-50">
        <Navigation
          onLoginClick={() => setShowLogin(true)}
          onRegisterClick={() => setShowRegister(true)}
        />

        <Hero
          onStartLearning={handleStartLearning}
          onAskAI={() => setShowChat(true)}
        />

        <QuickActions
          onStartSession={handleStartLearning}
          onAskAI={() => setShowChat(true)}
          onViewProgress={handleViewProgress}
          onCreatePlan={handleCreatePlan}
        />

        {/* Modals */}
        {showLogin && (
          <LoginForm
            onClose={() => setShowLogin(false)}
            onSwitchToRegister={handleSwitchToRegister}
            onSuccess={(msg) => addNotification(msg, 'success')}
            onError={(msg) => addNotification(msg, 'error')}
          />
        )}

        {showRegister && (
          <RegisterForm
            onClose={() => setShowRegister(false)}
            onSwitchToLogin={handleSwitchToLogin}
            onSuccess={(msg) => addNotification(msg, 'success')}
            onError={(msg) => addNotification(msg, 'error')}
          />
        )}

        {showChat && <ChatModal onClose={() => setShowChat(false)} />}

        {/* Notifications */}
        <div className="fixed top-4 right-4 z-50 space-y-2">
          {notifications.map((notification) => (
            <Notification
              key={notification.id}
              notification={notification}
              onClose={removeNotification}
            />
          ))}
        </div>
      </div>
    </AuthProvider>
  );
}

export default App;

