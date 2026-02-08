import React from 'react';

interface QuickActionsProps {
  onStartSession: () => void;
  onAskAI: () => void;
  onViewProgress: () => void;
  onCreatePlan: () => void;
}

const QuickActions: React.FC<QuickActionsProps> = ({
  onStartSession,
  onAskAI,
  onViewProgress,
  onCreatePlan,
}) => {
  return (
    <section className="py-12 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4">
        <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">
          Quick Study Actions
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Quick Study */}
          <div className="bg-white p-6 rounded-lg shadow-md text-center hover:shadow-lg transition-shadow">
            <div className="text-4xl mb-4">⚡</div>
            <h3 className="text-lg font-semibold mb-2">Quick Study</h3>
            <p className="text-sm text-gray-600 mb-4">
              Start a 25-minute focused session right now
            </p>
            <button
              onClick={onStartSession}
              className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Start Session
            </button>
          </div>

          {/* Ask AI */}
          <div className="bg-white p-6 rounded-lg shadow-md text-center hover:shadow-lg transition-shadow">
            <div className="text-4xl mb-4">💬</div>
            <h3 className="text-lg font-semibold mb-2">Ask AI</h3>
            <p className="text-sm text-gray-600 mb-4">
              Get instant study tips and answers
            </p>
            <button
              onClick={onAskAI}
              className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition-colors"
            >
              Ask Question
            </button>
          </div>

          {/* View Progress */}
          <div className="bg-white p-6 rounded-lg shadow-md text-center hover:shadow-lg transition-shadow">
            <div className="text-4xl mb-4">📈</div>
            <h3 className="text-lg font-semibold mb-2">View Progress</h3>
            <p className="text-sm text-gray-600 mb-4">
              Check your learning statistics
            </p>
            <button
              onClick={onViewProgress}
              className="w-full bg-purple-600 text-white py-2 rounded-lg hover:bg-purple-700 transition-colors"
            >
              View Stats
            </button>
          </div>

          {/* Study Planner */}
          <div className="bg-white p-6 rounded-lg shadow-md text-center hover:shadow-lg transition-shadow">
            <div className="text-4xl mb-4">📅</div>
            <h3 className="text-lg font-semibold mb-2">Study Planner</h3>
            <p className="text-sm text-gray-600 mb-4">
              Create personalized study schedules
            </p>
            <button
              onClick={onCreatePlan}
              className="w-full bg-orange-600 text-white py-2 rounded-lg hover:bg-orange-700 transition-colors"
            >
              Create Plan
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default QuickActions;
