import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';

interface NavigationProps {
  onLoginClick: () => void;
  onRegisterClick: () => void;
}

const Navigation: React.FC<NavigationProps> = ({ onLoginClick, onRegisterClick }) => {
  const { isAuthenticated, user, logout } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav className="bg-white dark:bg-gray-800 shadow-md">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <div className="text-2xl font-bold text-blue-600">StudyWise AI</div>

          {/* Desktop nav */}
          <div className="hidden sm:flex items-center gap-4">
            {isAuthenticated && user ? (
              <>
                <span className="text-gray-700 dark:text-gray-300">Welcome, {user.full_name || user.username}!</span>
                <button
                  onClick={logout}
                  className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <button
                  onClick={onLoginClick}
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold"
                >
                  Login
                </button>
                <button
                  onClick={onRegisterClick}
                  className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-semibold"
                >
                  Register
                </button>
              </>
            )}
          </div>

          {/* Mobile hamburger */}
          <button
            className="sm:hidden p-2 rounded-lg text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            onClick={() => setMenuOpen((o) => !o)}
            aria-label={menuOpen ? 'Close menu' : 'Open menu'}
            aria-expanded={menuOpen}
          >
            {menuOpen ? (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            ) : (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            )}
          </button>
        </div>

        {/* Mobile dropdown */}
        {menuOpen && (
          <div className="sm:hidden pb-4 border-t border-gray-200 dark:border-gray-700 pt-3 space-y-2">
            {isAuthenticated && user ? (
              <>
                <p className="px-2 text-sm text-gray-600 dark:text-gray-400">
                  Signed in as <span className="font-semibold">{user.full_name || user.username}</span>
                </p>
                <button
                  onClick={() => { logout(); setMenuOpen(false); }}
                  className="w-full px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors text-left"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <button
                  onClick={() => { onLoginClick(); setMenuOpen(false); }}
                  className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold text-left"
                >
                  Login
                </button>
                <button
                  onClick={() => { onRegisterClick(); setMenuOpen(false); }}
                  className="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-semibold text-left"
                >
                  Register
                </button>
              </>
            )}
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navigation;
