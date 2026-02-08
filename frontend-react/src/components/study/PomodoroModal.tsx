import React, { useState, useEffect } from 'react';
import { studySessionManager } from '../../utils/studySessionManager';

interface PomodoroModalProps {
  onClose: () => void;
}

const PomodoroModal: React.FC<PomodoroModalProps> = ({ onClose }) => {
  const [subject, setSubject] = useState('');
  const [duration, setDuration] = useState(25);
  const [goal, setGoal] = useState('');
  const [sessionStarted, setSessionStarted] = useState(false);
  const [timeRemaining, setTimeRemaining] = useState(25 * 60);
  const [isRunning, setIsRunning] = useState(false);

  // Timer interval effect
  useEffect(() => {
    let interval: number | null = null;

    if (isRunning && timeRemaining > 0 && sessionStarted) {
      interval = window.setInterval(() => {
        setTimeRemaining((prev) => {
          if (prev <= 1) {
            setIsRunning(false);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isRunning, sessionStarted, timeRemaining]);

  // Auto-save when timer completes
  useEffect(() => {
    if (timeRemaining === 0 && sessionStarted && subject) {
      studySessionManager.saveSession({
        id: Date.now().toString(),
        subject,
        duration,
        timeSpent: duration,
        goal,
        completedAt: new Date().toISOString(),
        completed: true,
      });
    }
  }, [timeRemaining, sessionStarted, subject, duration, goal]);

  const handleStartSession = () => {
    if (!subject) {
      alert('Please select a subject!');
      return;
    }
    setTimeRemaining(duration * 60);
    setSessionStarted(true);
    setIsRunning(true);
  };

  const handlePauseResume = () => {
    setIsRunning(!isRunning);
  };

  const handleStop = () => {
    if (confirm('Stop this study session? Progress will be saved.')) {
      const timeSpent = duration - Math.floor(timeRemaining / 60);
      studySessionManager.saveSession({
        id: Date.now().toString(),
        subject,
        duration,
        timeSpent,
        goal,
        completedAt: new Date().toISOString(),
        completed: false,
      });
      setSessionStarted(false);
      setIsRunning(false);
      setTimeRemaining(duration * 60);
    }
  };

  const handleAddTime = () => {
    setTimeRemaining((prev) => prev + 300); // Add 5 minutes
  };

  const minutes = Math.floor(timeRemaining / 60);
  const seconds = timeRemaining % 60;

  if (sessionStarted) {
    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-lg max-w-md w-full p-8">
          {/* Header */}
          <div className="text-center mb-8">
            <h2 className="text-2xl font-bold text-gray-800">📚 Study Session</h2>
            <p className="text-gray-600 mt-2">{subject}</p>
            {goal && <p className="text-sm text-gray-500 mt-1">Goal: {goal}</p>}
          </div>

          {/* Timer Display */}
          <div className="bg-gradient-to-r from-blue-600 to-indigo-700 rounded-lg p-8 text-center mb-8">
            <div className="text-6xl font-bold text-white font-mono">
              {minutes.toString().padStart(2, '0')}:{seconds.toString().padStart(2, '0')}
            </div>
            <p className="text-blue-100 mt-4">Stay focused!</p>
          </div>

          {/* Progress Bar */}
          <div className="mb-8">
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{
                  width: `${(1 - timeRemaining / (duration * 60)) * 100}%`,
                }}
              ></div>
            </div>
            <p className="text-sm text-gray-500 mt-2 text-center">
              {Math.round((1 - timeRemaining / (duration * 60)) * 100)}% complete
            </p>
          </div>

          {/* Controls */}
          <div className="flex gap-3 mb-4">
            <button
              onClick={handlePauseResume}
              className="flex-1 bg-yellow-500 text-white py-3 rounded-lg font-semibold hover:bg-yellow-600 transition-colors"
            >
              {isRunning ? '⏸️ Pause' : '▶️ Resume'}
            </button>
            <button
              onClick={handleAddTime}
              className="flex-1 bg-green-500 text-white py-3 rounded-lg font-semibold hover:bg-green-600 transition-colors"
            >
              ➕ +5min
            </button>
          </div>

          <button
            onClick={handleStop}
            className="w-full bg-red-500 text-white py-3 rounded-lg font-semibold hover:bg-red-600 transition-colors"
          >
            ⏹️ Stop Session
          </button>

          {timeRemaining === 0 && (
            <div className="mt-4 bg-green-100 border border-green-400 rounded-lg p-4 text-center">
              <p className="text-green-800 font-semibold">🎉 Session Complete!</p>
              <p className="text-sm text-green-700 mt-2">Great job staying focused!</p>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-md w-full max-h-96 overflow-y-auto">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white p-6 flex justify-between items-center sticky top-0">
          <h2 className="text-2xl font-bold">⚡ Quick Study Session</h2>
          <button
            onClick={onClose}
            className="text-2xl hover:bg-white/20 rounded-full w-10 h-10 flex items-center justify-center transition-colors"
          >
            ×
          </button>
        </div>

        {/* Form */}
        <div className="p-6">
          <div className="mb-4">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              📚 Subject
            </label>
            <select
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
            >
              <option value="">Choose a subject...</option>
              <option value="Mathematics">📐 Mathematics</option>
              <option value="Science">🔬 Science</option>
              <option value="Language">📚 Language Arts</option>
              <option value="History">🏛️ History</option>
              <option value="Programming">💻 Programming</option>
              <option value="Other">🎓 Other</option>
            </select>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              ⏱️ Duration
            </label>
            <select
              value={duration}
              onChange={(e) => setDuration(parseInt(e.target.value))}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
            >
              <option value="25">25 minutes (Pomodoro)</option>
              <option value="30">30 minutes</option>
              <option value="45">45 minutes</option>
              <option value="60">1 hour</option>
              <option value="90">1.5 hours</option>
              <option value="120">2 hours</option>
            </select>
          </div>

          <div className="mb-6">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              🎯 Study Goal (optional)
            </label>
            <textarea
              value={goal}
              onChange={(e) => setGoal(e.target.value)}
              placeholder="What do you want to accomplish in this session?"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
              rows={3}
            ></textarea>
          </div>

          <button
            onClick={handleStartSession}
            className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
          >
            🚀 Start Session
          </button>
        </div>
      </div>
    </div>
  );
};

export default PomodoroModal;
