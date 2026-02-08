import React, { useState, useEffect } from 'react';
import { studySessionManager } from '../../utils/studySessionManager';
import type { StudyStats } from '../../utils/studySessionManager';

interface ProgressModalProps {
  onClose: () => void;
}

const ProgressModal: React.FC<ProgressModalProps> = ({ onClose }) => {
  const [stats, setStats] = useState<StudyStats>(studySessionManager.getStats());

  // Refresh stats when modal opens
  useEffect(() => {
    const refreshStats = () => {
      setStats(studySessionManager.getStats());
    };

    // Refresh on mount
    refreshStats();

    // Also listen for storage changes (in case another tab/window updated it)
    window.addEventListener('storage', refreshStats);
    
    return () => {
      window.removeEventListener('storage', refreshStats);
    };
  }, []);

  const hours = Math.floor((stats.totalStudyTime || 0) / 60);
  const minutes = (stats.totalStudyTime || 0) % 60;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-96 overflow-y-auto">
        {/* Header */}
        <div className="bg-gradient-to-r from-purple-600 to-indigo-700 text-white p-6 flex justify-between items-center sticky top-0">
          <h2 className="text-2xl font-bold">Your Learning Progress</h2>
          <button
            onClick={onClose}
            className="text-2xl hover:bg-white/20 rounded-full w-10 h-10 flex items-center justify-center transition-colors"
          >
            ×
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {/* Study Sessions */}
            <div className="bg-blue-50 p-4 rounded-lg text-center border-l-4 border-blue-600">
              <div className="text-3xl font-bold text-blue-600">
                {stats.totalSessions || 0}
              </div>
              <p className="text-sm text-gray-600 mt-2">Study Sessions</p>
            </div>

            {/* Study Time */}
            <div className="bg-green-50 p-4 rounded-lg text-center border-l-4 border-green-600">
              <div className="text-3xl font-bold text-green-600">
                {hours}h {minutes}m
              </div>
              <p className="text-sm text-gray-600 mt-2">Total Study Time</p>
            </div>

            {/* Current Streak */}
            <div className="bg-orange-50 p-4 rounded-lg text-center border-l-4 border-orange-600">
              <div className="text-3xl font-bold text-orange-600">
                {stats.currentStreak || 0}
              </div>
              <p className="text-sm text-gray-600 mt-2">Day Streak 🔥</p>
            </div>

            {/* Tasks Completed */}
            <div className="bg-purple-50 p-4 rounded-lg text-center border-l-4 border-purple-600">
              <div className="text-3xl font-bold text-purple-600">
                {stats.completedTasks || 0}
              </div>
              <p className="text-sm text-gray-600 mt-2">Tasks Completed</p>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="mt-6 flex gap-3 justify-end">
            <button
              onClick={onClose}
              className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProgressModal;
