import React from 'react';

interface HeroProps {
  onStartLearning: () => void;
  onAskAI: () => void;
}

const Hero: React.FC<HeroProps> = ({ onStartLearning, onAskAI }) => {
  return (
    <section className="bg-gradient-to-r from-purple-600 to-indigo-700 text-white py-20">
      <div className="max-w-4xl mx-auto px-4 text-center">
        <h1 className="text-5xl font-bold mb-6">Welcome to StudyWise AI</h1>
        <p className="text-xl mb-8">
          Transform your learning journey with AI-powered study plans
        </p>
        <div className="flex justify-center gap-4 flex-wrap">
          <button
            onClick={onStartLearning}
            className="px-8 py-3 bg-white text-purple-600 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
          >
            🚀 Start Learning
          </button>
          <button
            onClick={onAskAI}
            className="px-8 py-3 border-2 border-white text-white rounded-lg font-semibold hover:bg-white hover:text-purple-600 transition-colors"
          >
            💬 Ask AI Assistant
          </button>
        </div>
      </div>
    </section>
  );
};

export default Hero;
