import React, { useState, useEffect } from 'react';
import { apiService } from '../../services/api';

interface ProgressSummary {
  total_study_time: number;
  total_sessions: number;
  subjects_studied: string[];
  average_accuracy: number;
  current_streak: number;
  weekly_progress: Array<{ week_start: string; time_spent: number; sessions: number }>;
  learning_trends: {
    most_studied_subjects?: Array<[string, number]>;
    study_consistency?: number;
    average_session_length?: number;
  };
}

interface ProgressModalProps {
  onClose: () => void;
}

const ProgressModal: React.FC<ProgressModalProps> = ({ onClose }) => {
  const [summary, setSummary] = useState<ProgressSummary | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const loadSummary = async () => {
      try {
        const data = await apiService.getProgressSummary();
        setSummary(data as unknown as ProgressSummary);
      } catch {
        setError('Failed to load progress data.');
      } finally {
        setIsLoading(false);
      }
    };
    loadSummary();
  }, []);

  const hours = Math.floor((summary?.total_study_time ?? 0) / 60);
  const minutes = (summary?.total_study_time ?? 0) % 60;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" role="dialog" aria-modal="true" aria-label="Learning Progress">
      <div className="bg-white dark:bg-gray-800 rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="bg-gradient-to-r from-purple-600 to-indigo-700 text-white p-6 flex justify-between items-center sticky top-0">
          <h2 className="text-2xl font-bold">Your Learning Progress</h2>
          <button
            onClick={onClose}
            className="text-2xl hover:bg-white/20 rounded-full w-10 h-10 flex items-center justify-center transition-colors"
            aria-label="Close progress modal"
          >
            ×
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          {isLoading && (
            <div className="text-center text-gray-500 dark:text-gray-400 py-8">Loading progress data...</div>
          )}
          {error && (
            <div className="text-center text-red-500 py-8">{error}</div>
          )}
          {summary && (
            <>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="bg-blue-50 dark:bg-blue-900/30 p-4 rounded-lg text-center border-l-4 border-blue-600">
                  <div className="text-3xl font-bold text-blue-600">{summary.total_sessions}</div>
                  <p className="text-sm text-gray-600 dark:text-gray-300 mt-2">Study Sessions</p>
                </div>
                <div className="bg-green-50 dark:bg-green-900/30 p-4 rounded-lg text-center border-l-4 border-green-600">
                  <div className="text-3xl font-bold text-green-600">{hours}h {minutes}m</div>
                  <p className="text-sm text-gray-600 dark:text-gray-300 mt-2">Total Study Time</p>
                </div>
                <div className="bg-orange-50 dark:bg-orange-900/30 p-4 rounded-lg text-center border-l-4 border-orange-600">
                  <div className="text-3xl font-bold text-orange-600">{summary.current_streak}</div>
                  <p className="text-sm text-gray-600 dark:text-gray-300 mt-2">Day Streak 🔥</p>
                </div>
                <div className="bg-purple-50 dark:bg-purple-900/30 p-4 rounded-lg text-center border-l-4 border-purple-600">
                  <div className="text-3xl font-bold text-purple-600">
                    {summary.average_accuracy > 0 ? `${Math.round(summary.average_accuracy)}%` : '—'}
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-300 mt-2">Avg Accuracy</p>
                </div>
              </div>

              {summary.subjects_studied.length > 0 && (
                <div className="mt-6">
                  <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Subjects Studied</h3>
                  <div className="flex flex-wrap gap-2">
                    {summary.subjects_studied.map((s) => (
                      <span key={s} className="px-3 py-1 bg-indigo-100 dark:bg-indigo-900/40 text-indigo-700 dark:text-indigo-300 rounded-full text-xs font-medium">
                        {s}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {(summary.learning_trends?.study_consistency ?? 0) > 0 && (
                <div className="mt-4">
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Study consistency: <span className="font-semibold text-gray-800 dark:text-white">{summary.learning_trends.study_consistency}%</span>
                  </p>
                </div>
              )}
            </>
          )}

          <div className="mt-6 flex gap-3 justify-end">
            <button
              onClick={onClose}
              className="px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
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
