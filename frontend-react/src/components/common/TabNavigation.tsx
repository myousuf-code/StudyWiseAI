import React from 'react';
import { useTheme } from '../../context/ThemeContext';
import { useAuth } from '../../context/AuthContext';

interface TabNavProps {
  activeTab: 'home' | 'study' | 'chat' | 'progress' | 'planner' | 'nlp' | 'career';
  onTabChange: (tab: 'home' | 'study' | 'chat' | 'progress' | 'planner' | 'nlp' | 'career') => void;
  onLoginClick?: () => void;
  onRegisterClick?: () => void;
  onA11yClick?: () => void;
}

const TabNavigation: React.FC<TabNavProps> = ({ activeTab, onTabChange, onLoginClick, onRegisterClick, onA11yClick }) => {
  const { theme, toggleTheme } = useTheme();
  const { isAuthenticated, user, logout } = useAuth();
  const tabs = [
    { id: 'home' as const, label: '🏠 Home', icon: '🏠' },
    { id: 'study' as const, label: '⚡ Quick Study', icon: '⚡' },
    { id: 'chat' as const, label: '💬 AI Assistant', icon: '💬' },
    { id: 'career' as const, label: '🎯 Career Counseling', icon: '🎯' },
    { id: 'nlp' as const, label: '🤖 NLP Tools', icon: '🤖' },
    { id: 'progress' as const, label: '📈 Progress', icon: '📈' },
    { id: 'planner' as const, label: '📅 Planner', icon: '📅' },
  ];

  return (
    <nav className="bg-gradient-to-r from-purple-600 to-indigo-700 text-white">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between">
          {/* Logo/Brand */}
          <div className="flex items-center py-4">
            <h1 className="text-2xl font-bold">📚 StudyWise AI</h1>
          </div>

          {/* Tabs */}
          <div className="flex space-x-1">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => onTabChange(tab.id)}
                className={`px-4 py-2 rounded-t-lg font-semibold transition-colors whitespace-nowrap ${
                  activeTab === tab.id
                    ? 'bg-white text-purple-600 border-b-4 border-white'
                    : 'text-purple-100 hover:bg-white/10'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Right Actions */}
          <div className="flex items-center space-x-4">
            <button
              onClick={onA11yClick}
              className="px-3 py-2 rounded-lg text-white hover:bg-white/20 transition-colors text-xl"
              title="Accessibility Settings"
              aria-label="Open accessibility settings"
            >
              ♿
            </button>
            <button
              onClick={toggleTheme}
              className="px-3 py-2 rounded-lg text-white hover:bg-white/20 transition-colors text-xl"
              title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
            >
              {theme === 'light' ? '🌙' : '☀️'}
            </button>
            {isAuthenticated && user ? (
              <>
                <span className="text-white text-sm">
                  {user.full_name || user.username}
                </span>
                <button
                  onClick={logout}
                  className="px-4 py-2 bg-red-500 rounded-lg hover:bg-red-600 transition-colors font-semibold text-white"
                >
                  🚪 Logout
                </button>
              </>
            ) : (
              <>
                <button
                  onClick={onLoginClick}
                  className="px-4 py-2 bg-blue-500 rounded-lg hover:bg-blue-600 transition-colors font-semibold text-white"
                >
                  Login
                </button>
                <button
                  onClick={onRegisterClick}
                  className="px-4 py-2 bg-green-500 rounded-lg hover:bg-green-600 transition-colors font-semibold text-white"
                >
                  Register
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default TabNavigation;
