import React from 'react';
import { useAuth } from '../../context/AuthContext';

interface NavigationProps {
  onLoginClick: () => void;
  onRegisterClick: () => void;
}

const Navigation: React.FC<NavigationProps> = ({ onLoginClick, onRegisterClick }) => {
  const { isAuthenticated, user, logout } = useAuth();

  return (
    <nav className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <div className="text-2xl font-bold text-blue-600">StudyWise AI</div>

          <div className="flex items-center gap-4">
            {isAuthenticated && user ? (
              <>
                <span className="text-gray-700">Welcome, {user.full_name || user.username}!</span>
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
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
