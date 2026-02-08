import React from 'react';

interface HomePageProps {
  onAskAI: () => void;
  onStartStudy: () => void;
}

const HomePage: React.FC<HomePageProps> = ({ onAskAI, onStartStudy }) => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-purple-600 via-indigo-600 to-blue-600 text-white py-24">
        <div className="max-w-6xl mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            {/* Left Content */}
            <div>
              <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
                Learn Smarter,<br />Not Harder
              </h1>
              <p className="text-xl text-blue-100 mb-8">
                AI-powered study tools, Pomodoro timers, progress tracking, and personalized learning plans—all in one place.
              </p>
              <div className="flex gap-4 flex-wrap">
                <button
                  onClick={onStartStudy}
                  className="px-8 py-4 bg-white text-purple-600 rounded-lg font-semibold hover:bg-gray-100 transition-all transform hover:scale-105 text-lg"
                >
                  ⚡ Start Studying
                </button>
                <button
                  onClick={onAskAI}
                  className="px-8 py-4 border-2 border-white text-white rounded-lg font-semibold hover:bg-white hover:text-purple-600 transition-all transform hover:scale-105 text-lg"
                >
                  💬 Chat with AI
                </button>
              </div>
            </div>

            {/* Right Visual */}
            <div className="hidden md:flex flex-col gap-4">
              <div className="bg-white/10 backdrop-blur rounded-lg p-6 border border-white/20">
                <div className="text-4xl mb-3">⚡</div>
                <p className="text-blue-100">Quick 25-min focused study sessions</p>
              </div>
              <div className="bg-white/10 backdrop-blur rounded-lg p-6 border border-white/20">
                <div className="text-4xl mb-3">🤖</div>
                <p className="text-blue-100">AI-powered learning assistance</p>
              </div>
              <div className="bg-white/10 backdrop-blur rounded-lg p-6 border border-white/20">
                <div className="text-4xl mb-3">📈</div>
                <p className="text-blue-100">Real-time progress tracking</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 text-center border-t-4 border-blue-600">
              <div className="text-4xl font-bold text-blue-600 mb-2">25min</div>
              <p className="text-gray-600 dark:text-gray-300">Optimal Session Length</p>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 text-center border-t-4 border-green-600">
              <div className="text-4xl font-bold text-green-600 mb-2">∞</div>
              <p className="text-gray-600 dark:text-gray-300">AI Questions Answered</p>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 text-center border-t-4 border-purple-600">
              <div className="text-4xl font-bold text-purple-600 mb-2">6</div>
              <p className="text-gray-600 dark:text-gray-300">AI-Powered Tools</p>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 text-center border-t-4 border-orange-600">
              <div className="text-4xl font-bold text-orange-600 mb-2">2x</div>
              <p className="text-gray-600 dark:text-gray-300">Faster Learning</p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="text-4xl font-bold text-center text-gray-800 dark:text-white mb-16">
            Powerful Features at Your Fingertips
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Quick Study */}
            <div className="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-gray-800 dark:to-gray-700 p-8 rounded-xl border-l-4 border-blue-600 hover:shadow-lg transition-shadow">
              <div className="text-5xl mb-4">⚡</div>
              <h3 className="text-2xl font-semibold mb-3 text-gray-800 dark:text-white">Quick Study</h3>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                Start focused Pomodoro sessions with customizable durations. Perfect for maintaining concentration and building productive study habits.
              </p>
            </div>

            {/* AI Chat */}
            <div className="bg-gradient-to-br from-green-50 to-green-100 dark:from-gray-800 dark:to-gray-700 p-8 rounded-xl border-l-4 border-green-600 hover:shadow-lg transition-shadow">
              <div className="text-5xl mb-4">💬</div>
              <h3 className="text-2xl font-semibold mb-3 text-gray-800 dark:text-white">AI Assistant</h3>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                Get instant answers, study tips, and personalized guidance from your intelligent study companion available 24/7.
              </p>
            </div>

            {/* NLP Tools */}
            <div className="bg-gradient-to-br from-cyan-50 to-cyan-100 dark:from-gray-800 dark:to-gray-700 p-8 rounded-xl border-l-4 border-cyan-600 hover:shadow-lg transition-shadow">
              <div className="text-5xl mb-4">🤖</div>
              <h3 className="text-2xl font-semibold mb-3 text-gray-800 dark:text-white">NLP Tools</h3>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                Summarize notes, check grammar, analyze sentiment, and paraphrase text to enhance your study materials.
              </p>
            </div>

            {/* Progress Tracking */}
            <div className="bg-gradient-to-br from-orange-50 to-orange-100 dark:from-gray-800 dark:to-gray-700 p-8 rounded-xl border-l-4 border-orange-600 hover:shadow-lg transition-shadow">
              <div className="text-5xl mb-4">📈</div>
              <h3 className="text-2xl font-semibold mb-3 text-gray-800 dark:text-white">Track Progress</h3>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                Monitor your learning stats, maintain daily streaks, and visualize your improvement over time with detailed analytics.
              </p>
            </div>

            {/* Weekly Planner */}
            <div className="bg-gradient-to-br from-purple-50 to-purple-100 dark:from-gray-800 dark:to-gray-700 p-8 rounded-xl border-l-4 border-purple-600 hover:shadow-lg transition-shadow">
              <div className="text-5xl mb-4">📅</div>
              <h3 className="text-2xl font-semibold mb-3 text-gray-800 dark:text-white">Study Planner</h3>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                Create and manage personalized weekly study schedules with color-coded events for better organization.
              </p>
            </div>

            {/* Progress Saving */}
            <div className="bg-gradient-to-br from-pink-50 to-pink-100 dark:from-gray-800 dark:to-gray-700 p-8 rounded-xl border-l-4 border-pink-600 hover:shadow-lg transition-shadow">
              <div className="text-5xl mb-4">💾</div>
              <h3 className="text-2xl font-semibold mb-3 text-gray-800 dark:text-white">Auto-Save Progress</h3>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                Your study sessions and progress are automatically saved locally, ensuring you never lose your learning data.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-gradient-to-r from-indigo-50 to-blue-50 dark:from-gray-800 dark:to-gray-900">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-4xl font-bold text-center text-gray-800 dark:text-white mb-16">
            How StudyWise Works
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="relative">
              <div className="bg-white dark:bg-gray-800 rounded-lg p-8 text-center shadow-lg">
                <div className="bg-blue-600 text-white rounded-full w-16 h-16 flex items-center justify-center text-2xl font-bold mx-auto mb-4">1</div>
                <h3 className="text-lg font-semibold mb-2 text-gray-800 dark:text-white">Create Account</h3>
                <p className="text-gray-600 dark:text-gray-300 text-sm">Sign up and set up your profile</p>
              </div>
              <div className="hidden md:block absolute top-1/2 -right-3 w-6 h-6 bg-blue-600 rounded-full"></div>
            </div>
            <div className="relative">
              <div className="bg-white dark:bg-gray-800 rounded-lg p-8 text-center shadow-lg">
                <div className="bg-blue-600 text-white rounded-full w-16 h-16 flex items-center justify-center text-2xl font-bold mx-auto mb-4">2</div>
                <h3 className="text-lg font-semibold mb-2 text-gray-800 dark:text-white">Choose Your Tool</h3>
                <p className="text-gray-600 dark:text-gray-300 text-sm">Pick from 6+ AI-powered features</p>
              </div>
              <div className="hidden md:block absolute top-1/2 -right-3 w-6 h-6 bg-blue-600 rounded-full"></div>
            </div>
            <div className="relative">
              <div className="bg-white dark:bg-gray-800 rounded-lg p-8 text-center shadow-lg">
                <div className="bg-blue-600 text-white rounded-full w-16 h-16 flex items-center justify-center text-2xl font-bold mx-auto mb-4">3</div>
                <h3 className="text-lg font-semibold mb-2 text-gray-800 dark:text-white">Study & Learn</h3>
                <p className="text-gray-600 dark:text-gray-300 text-sm">Use tools to study effectively</p>
              </div>
              <div className="hidden md:block absolute top-1/2 -right-3 w-6 h-6 bg-blue-600 rounded-full"></div>
            </div>
            <div>
              <div className="bg-white dark:bg-gray-800 rounded-lg p-8 text-center shadow-lg">
                <div className="bg-blue-600 text-white rounded-full w-16 h-16 flex items-center justify-center text-2xl font-bold mx-auto mb-4">4</div>
                <h3 className="text-lg font-semibold mb-2 text-gray-800 dark:text-white">Track Progress</h3>
                <p className="text-gray-600 text-sm">Watch your improvement grow</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-purple-600 to-indigo-700 dark:from-purple-900 dark:to-indigo-900 text-white">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold mb-6">Ready to Transform Your Learning?</h2>
          <p className="text-xl text-purple-100 mb-8">
            Start using StudyWise AI today and experience smarter, more effective studying.
          </p>
          <button
            onClick={onStartStudy}
            className="px-10 py-4 bg-white text-purple-600 rounded-lg font-bold text-lg hover:bg-gray-100 transition-all transform hover:scale-105"
          >
            🚀 Start Your Journey Now
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
            <div>
              <h3 className="text-xl font-bold mb-4">StudyWise AI</h3>
              <p className="text-gray-400">Empowering students to learn smarter, not harder.</p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Features</h4>
              <ul className="text-gray-400 space-y-2 text-sm">
                <li>Quick Study Sessions</li>
                <li>AI Assistant</li>
                <li>NLP Tools</li>
                <li>Progress Tracking</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">About</h4>
              <ul className="text-gray-400 space-y-2 text-sm">
                <li>© 2026 StudyWise AI</li>
                <li>All rights reserved</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-700 pt-8 text-center text-gray-400">
            <p>Made with ❤️ to help students succeed</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
