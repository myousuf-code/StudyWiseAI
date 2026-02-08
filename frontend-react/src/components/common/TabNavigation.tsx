import React from 'react';
import { useTheme } from '../../context/ThemeContext';

interface TabNavProps {
  activeTab: 'home' | 'study' | 'chat' | 'progress' | 'planner' | 'nlp';
  onTabChange: (tab: 'home' | 'study' | 'chat' | 'progress' | 'planner' | 'nlp') => void;
  onLogout?: () => void;
}

const TabNavigation: React.FC<TabNavProps> = ({ activeTab, onTabChange, onLogout }) => {
  const { theme, toggleTheme } = useTheme();
  const tabs = [
    { id: 'home' as const, label: '🏠 Home', icon: '🏠' },
    { id: 'study' as const, label: '⚡ Quick Study', icon: '⚡' },
    { id: 'chat' as const, label: '💬 AI Assistant', icon: '💬' },
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
              onClick={toggleTheme}
              className="px-3 py-2 rounded-lg text-white hover:bg-white/20 transition-colors text-xl"
              title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
            >
              {theme === 'light' ? '🌙' : '☀️'}
            </button>
            {onLogout && (
              <button
                onClick={onLogout}
                className="px-4 py-2 bg-red-500 rounded-lg hover:bg-red-600 transition-colors font-semibold"
              >
                🚪 Logout
              </button>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default TabNavigation;
