import { useState, useEffect, useCallback } from 'react';
import { AuthProvider } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import { apiService } from './services/api';
import type { StudyPlan } from './types/index';
import TabNavigation from './components/common/TabNavigation';
import HomePage from './components/common/HomePage';
import LoginForm from './components/auth/LoginForm';
import RegisterForm from './components/auth/RegisterForm';
import ChatModal from './components/chat/ChatModal';
import ProgressModal from './components/dashboard/ProgressModal';
import PomodoroModal from './components/study/PomodoroModal';
import WeeklyPlannerModal from './components/study/WeeklyPlannerModal';
import NLPModal from './components/ai/NLPModal';
import CareerCounselingModal from './components/career/CareerCounselingModal';
import StudyPlanDetailModal from './components/study/StudyPlanDetailModal';
import Notification from './components/common/Notification';
import type { Notification as NotificationType } from './types/index';

type ActiveTab = 'home' | 'study' | 'chat' | 'progress' | 'planner' | 'nlp' | 'career';

function App() {
  const [activeTab, setActiveTab] = useState<ActiveTab>('home');
  const [showLogin, setShowLogin] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [showChat, setShowChat] = useState(false);
  const [showProgress, setShowProgress] = useState(false);
  const [showPomodoro, setShowPomodoro] = useState(false);
  const [showPlanner, setShowPlanner] = useState(false);
  const [showNLP, setShowNLP] = useState(false);
  const [showCareerCounseling, setShowCareerCounseling] = useState(false);
  const [notifications, setNotifications] = useState<NotificationType[]>([]);
  const [studyPlans, setStudyPlans] = useState<StudyPlan[]>([]);
  const [studyPlansLoading, setStudyPlansLoading] = useState(false);
  const [studyPlansError, setStudyPlansError] = useState('');
  const [deletingPlanId, setDeletingPlanId] = useState<number | null>(null);
  const [selectedPlan, setSelectedPlan] = useState<StudyPlan | null>(null);

  const loadStudyPlans = useCallback(async () => {
    setStudyPlansLoading(true);
    setStudyPlansError('');
    try {
      const plans = await apiService.getStudyPlans();
      setStudyPlans(plans);
    } catch (e: any) {
      setStudyPlansError('Failed to load study plans. Please log in first.');
    } finally {
      setStudyPlansLoading(false);
    }
  }, []);

  const deleteStudyPlan = async (id: number) => {
    if (!confirm('Delete this study plan?')) return;
    setDeletingPlanId(id);
    try {
      await apiService.deleteStudyPlan(id);
      setStudyPlans(prev => prev.filter(p => p.id !== id));
    } catch (e: any) {
      setStudyPlansError('Failed to delete study plan.');
    } finally {
      setDeletingPlanId(null);
    }
  };

  useEffect(() => {
    if (activeTab === 'study') {
      loadStudyPlans();
    }
  }, [activeTab, loadStudyPlans]);

  const addNotification = (message: string, type: NotificationType['type']) => {
    const notification: NotificationType = {
      id: Date.now().toString(),
      message,
      type,
    };
    setNotifications((prev) => [...prev, notification]);
  };

  const removeNotification = (id: string) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id));
  };

  const handleSwitchToRegister = () => {
    setShowLogin(false);
    setShowRegister(true);
  };

  const handleSwitchToLogin = () => {
    setShowRegister(false);
    setShowLogin(true);
  };

  return (
    <ThemeProvider>
      <AuthProvider>
        {selectedPlan && <StudyPlanDetailModal plan={selectedPlan} onClose={() => setSelectedPlan(null)} />}
        <div className="min-h-screen bg-white dark:bg-gray-900 transition-colors">
        {/* Tab Navigation */}
        <TabNavigation 
          activeTab={activeTab} 
          onTabChange={setActiveTab}
          onLoginClick={() => setShowLogin(true)}
          onRegisterClick={() => setShowRegister(true)}
        />

        {/* Main Content based on Active Tab */}
        <main>
          {activeTab === 'home' && (
            <HomePage
              onAskAI={() => setActiveTab('chat')}
              onStartStudy={() => setActiveTab('study')}
            />
          )}

          {activeTab === 'study' && (
            <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white dark:from-gray-900 dark:to-gray-800">
              <div className="max-w-7xl mx-auto px-4 py-12">
                <h2 className="text-4xl font-bold text-gray-800 dark:text-white mb-4">⚡ Quick Study Sessions</h2>
                <p className="text-lg text-gray-600 dark:text-gray-300 mb-12">Start focused Pomodoro study sessions with customizable durations and track your progress.</p>

                {/* ── My Study Plans ── */}
                <div className="mb-14">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-2xl font-bold text-gray-800 dark:text-white">📚 My Study Plans</h3>
                    <button
                      onClick={loadStudyPlans}
                      disabled={studyPlansLoading}
                      className="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
                    >
                      {studyPlansLoading ? '⟳ Loading...' : '↺ Refresh'}
                    </button>
                  </div>

                  {studyPlansError && (
                    <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">{studyPlansError}</div>
                  )}

                  {studyPlansLoading ? (
                    <div className="text-center py-8 text-gray-500 dark:text-gray-400">Loading your study plans...</div>
                  ) : studyPlans.length === 0 ? (
                    <div className="bg-white dark:bg-gray-800 rounded-xl border-2 border-dashed border-gray-200 dark:border-gray-600 p-10 text-center">
                      <div className="text-5xl mb-3">📭</div>
                      <p className="text-gray-500 dark:text-gray-400 font-medium">No study plans yet.</p>
                      <p className="text-sm text-gray-400 dark:text-gray-500 mt-1">Use Career Counseling to generate a personalised plan, or create one below.</p>
                    </div>
                  ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
                      {studyPlans.map(plan => (
                        <div key={plan.id} className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-5 flex flex-col gap-3">
                          <div className="flex items-start justify-between gap-2">
                            <div>
                              <span className="text-xs font-semibold uppercase tracking-wide text-blue-600 dark:text-blue-400">{plan.subject}</span>
                              <h4 className="font-bold text-gray-800 dark:text-white mt-0.5 leading-tight">{plan.title}</h4>
                            </div>
                            <span className={`shrink-0 text-xs px-2 py-1 rounded-full font-medium ${
                              plan.difficulty_level === 'beginner' ? 'bg-green-100 text-green-700' :
                              plan.difficulty_level === 'advanced' ? 'bg-red-100 text-red-700' :
                              'bg-yellow-100 text-yellow-700'
                            }`}>{plan.difficulty_level}</span>
                          </div>

                          {plan.description && (
                            <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-2">{plan.description}</p>
                          )}

                          <div className="flex items-center gap-4 text-xs text-gray-500 dark:text-gray-400 mt-auto">
                            {plan.estimated_duration > 0 && (
                              <span>⏱ {plan.estimated_duration} hrs est.</span>
                            )}
                            <span>📅 {new Date(plan.created_at).toLocaleDateString()}</span>
                          </div>

                          <div className="flex items-center gap-3 mt-1">
                            <button
                              onClick={() => setSelectedPlan(plan)}
                              className="text-xs text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-200 transition-colors"
                            >
                              👁 View full plan
                            </button>
                            <button
                              onClick={() => deleteStudyPlan(plan.id)}
                              disabled={deletingPlanId === plan.id}
                              className="text-xs text-red-500 hover:text-red-700 disabled:opacity-50 transition-colors"
                            >
                              {deletingPlanId === plan.id ? 'Deleting...' : '🗑 Delete'}
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
                
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                  {/* Main CTA */}
                  <div className="lg:col-span-1">
                    <div className="bg-gradient-to-br from-blue-600 to-blue-700 text-white rounded-xl p-8 shadow-lg">
                      <div className="text-5xl mb-4">⚡</div>
                      <h3 className="text-2xl font-bold mb-4">Start Now</h3>
                      <p className="mb-6">Begin a focused 25-minute study session with our Pomodoro timer</p>
                      <button
                        onClick={() => setShowPomodoro(true)}
                        className="w-full bg-white text-blue-600 px-6 py-3 rounded-lg font-bold hover:bg-gray-100 transition-all"
                      >
                        🚀 Start Session
                      </button>
                    </div>
                  </div>

                  {/* Info Cards */}
                  <div className="lg:col-span-2 space-y-4">
                    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border-l-4 border-blue-600 shadow">
                      <h4 className="font-bold text-lg mb-2 text-gray-800 dark:text-white">🎯 What is Pomodoro?</h4>
                      <p className="text-gray-700 dark:text-gray-300">The Pomodoro Technique is a time management method that uses 25-minute focused work intervals followed by short breaks to maximize productivity.</p>
                    </div>
                    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border-l-4 border-green-600 shadow">
                      <h4 className="font-bold text-lg mb-2 text-gray-800 dark:text-white">✅ Why It Works</h4>
                      <p className="text-gray-700 dark:text-gray-300">Studies show that focused 25-minute sessions prevent burnout and improve concentration. Our timer removes distractions and keeps you on track.</p>
                    </div>
                    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border-l-4 border-orange-600 shadow">
                      <h4 className="font-bold text-lg mb-2 text-gray-800 dark:text-white">📊 Track Your Growth</h4>
                      <p className="text-gray-700 dark:text-gray-300">Every session you complete is automatically saved. View your progress in the Progress tab to see how much you've accomplished.</p>
                    </div>
                  </div>
                </div>

                {/* Features Grid */}
                <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow text-center">
                    <div className="text-4xl mb-3">⏱️</div>
                    <h4 className="font-bold mb-2 text-gray-800 dark:text-white">Customizable Duration</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Choose 25, 30, 45, 60 minutes or longer</p>
                  </div>
                  <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow text-center">
                    <div className="text-4xl mb-3">📝</div>
                    <h4 className="font-bold mb-2 text-gray-800 dark:text-white">Set Goals</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Define what you want to accomplish</p>
                  </div>
                  <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow text-center">
                    <div className="text-4xl mb-3">💾</div>
                    <h4 className="font-bold mb-2 text-gray-800 dark:text-white">Auto-Save</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Sessions saved automatically to your account</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'chat' && (
            <div className="min-h-screen bg-gradient-to-b from-green-50 to-white dark:from-gray-900 dark:to-gray-800">
              <div className="max-w-7xl mx-auto px-4 py-12">
                <h2 className="text-4xl font-bold text-gray-800 dark:text-white mb-4">💬 AI Study Assistant</h2>
                <p className="text-lg text-gray-600 dark:text-gray-300 mb-12">Chat with your intelligent study companion powered by advanced AI technology.</p>
                
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                  {/* Main CTA */}
                  <div className="lg:col-span-1">
                    <div className="bg-gradient-to-br from-green-600 to-green-700 text-white rounded-xl p-8 shadow-lg">
                      <div className="text-5xl mb-4">💬</div>
                      <h3 className="text-2xl font-bold mb-4">Start Chatting</h3>
                      <p className="mb-6">Ask questions, get explanations, and receive personalized study tips.</p>
                      <button
                        onClick={() => setShowChat(true)}
                        className="w-full bg-white text-green-600 px-6 py-3 rounded-lg font-bold hover:bg-gray-100 transition-all"
                      >
                        💬 Open Chat
                      </button>
                    </div>
                  </div>

                  {/* Info Cards */}
                  <div className="lg:col-span-2 space-y-4">
                    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border-l-4 border-green-600 shadow">
                      <h4 className="font-bold text-lg mb-2 text-gray-800 dark:text-white">🤖 AI-Powered Learning</h4>
                      <p className="text-gray-700 dark:text-gray-300">Our AI assistant understands complex topics and explains them in a way that makes sense for you. Available 24/7 for questions.</p>
                    </div>
                    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border-l-4 border-blue-600 shadow">
                      <h4 className="font-bold text-lg mb-2 text-gray-800 dark:text-white">📚 Multiple Subjects</h4>
                      <p className="text-gray-700 dark:text-gray-300">Ask about math, science, languages, history, programming, and more. The AI can help with any subject you're studying.</p>
                    </div>
                    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border-l-4 border-purple-600 shadow">
                      <h4 className="font-bold text-lg mb-2 text-gray-800 dark:text-white">💡 Smart Explanations</h4>
                      <p className="text-gray-700 dark:text-gray-300">Get detailed explanations, practice problems, tips for remembering concepts, and study strategies tailored to your needs.</p>
                    </div>
                  </div>
                </div>

                {/* Features Grid */}
                <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow text-center">
                    <div className="text-4xl mb-3">⚡</div>
                    <h4 className="font-bold mb-2 text-gray-800 dark:text-white">Instant Response</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Get answers in seconds</p>
                  </div>
                  <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow text-center">
                    <div className="text-4xl mb-3">🔄</div>
                    <h4 className="font-bold mb-2 text-gray-800 dark:text-white">Continuous Learning</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Chat history saved for later reference</p>
                  </div>
                  <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow text-center">
                    <div className="text-4xl mb-3">📖</div>
                    <h4 className="font-bold mb-2 text-gray-800 dark:text-white">Deep Explanations</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Not just answers, but understanding</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'progress' && (
            <div className="min-h-screen bg-gradient-to-b from-orange-50 to-white dark:from-gray-900 dark:to-gray-800">
              <div className="max-w-7xl mx-auto px-4 py-12">
                <h2 className="text-4xl font-bold text-gray-800 dark:text-white mb-4">📈 Your Learning Progress</h2>
                <p className="text-lg text-gray-600 dark:text-gray-300 mb-12">Track your study sessions, streaks, and overall progress in one place.</p>
                
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                  {/* Main CTA */}
                  <div className="lg:col-span-1">
                    <div className="bg-gradient-to-br from-orange-600 to-red-700 text-white rounded-xl p-8 shadow-lg">
                      <div className="text-5xl mb-4">📈</div>
                      <h3 className="text-2xl font-bold mb-4">View Stats</h3>
                      <p className="mb-6">See detailed analytics about your study habits and progress.</p>
                      <button
                        onClick={() => setShowProgress(true)}
                        className="w-full bg-white text-orange-600 px-6 py-3 rounded-lg font-bold hover:bg-gray-100 transition-all"
                      >
                        📊 View Stats
                      </button>
                    </div>
                  </div>

                  {/* Info Cards */}
                  <div className="lg:col-span-2 space-y-4">
                    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border-l-4 border-orange-600 shadow">
                      <h4 className="font-bold text-lg mb-2 text-gray-800 dark:text-white">📊 Comprehensive Dashboard</h4>
                      <p className="text-gray-700 dark:text-gray-300">View all your learning metrics in one dashboard: total sessions, study time, daily streaks, and completed tasks.</p>
                    </div>
                    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border-l-4 border-red-600 shadow">
                      <h4 className="font-bold text-lg mb-2 text-gray-800 dark:text-white">🔥 Streak Counter</h4>
                      <p className="text-gray-700 dark:text-gray-300">Maintain your daily study streak and stay motivated. Our streak counter tracks consecutive days of studious behavior.</p>
                    </div>
                    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border-l-4 border-yellow-600 shadow">
                      <h4 className="font-bold text-lg mb-2 text-gray-800 dark:text-white">📝 Session History</h4>
                      <p className="text-gray-700 dark:text-gray-300">Every session is automatically recorded. Track which subjects you studied, duration, and when you studied them.</p>
                    </div>
                  </div>
                </div>

                {/* Features Grid */}
                <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow text-center">
                    <div className="text-4xl mb-3">⏱️</div>
                    <h4 className="font-bold mb-2 text-gray-800 dark:text-white">Total Study Time</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Track hours spent studying</p>
                  </div>
                  <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow text-center">
                    <div className="text-4xl mb-3">🎯</div>
                    <h4 className="font-bold mb-2 text-gray-800 dark:text-white">Session Count</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Number of sessions completed</p>
                  </div>
                  <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow text-center">
                    <div className="text-4xl mb-3">🏆</div>
                    <h4 className="font-bold mb-2 text-gray-800 dark:text-white">Achievements</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Earn badges for milestones</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'planner' && (
            <div className="min-h-screen bg-gradient-to-b from-purple-50 to-white dark:from-gray-900 dark:to-gray-800">
              <div className="max-w-7xl mx-auto px-4 py-12">
                <h2 className="text-4xl font-bold text-gray-800 dark:text-white mb-4">📅 Weekly Study Planner</h2>
                <p className="text-lg text-gray-600 dark:text-gray-300 mb-12">Organize your study time with a visual weekly calendar and color-coded events.</p>
                
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                  {/* Main CTA */}
                  <div className="lg:col-span-1">
                    <div className="bg-gradient-to-br from-purple-600 to-pink-700 text-white rounded-xl p-8 shadow-lg">
                      <div className="text-5xl mb-4">📅</div>
                      <h3 className="text-2xl font-bold mb-4">Plan Now</h3>
                      <p className="mb-6">Create your personalized weekly study schedule.</p>
                      <button
                        onClick={() => setShowPlanner(true)}
                        className="w-full bg-white text-purple-600 px-6 py-3 rounded-lg font-bold hover:bg-gray-100 transition-all"
                      >
                        📅 Open Planner
                      </button>
                    </div>
                  </div>

                  {/* Info Cards */}
                  <div className="lg:col-span-2 space-y-4">
                    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border-l-4 border-purple-600 shadow">
                      <h4 className="font-bold text-lg mb-2 text-gray-800 dark:text-white">📋 Weekly Organization</h4>
                      <p className="text-gray-700 dark:text-gray-300">Plan your studies across all 7 days of the week. See at a glance when you're studying each subject and for how long.</p>
                    </div>
                    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border-l-4 border-pink-600 shadow">
                      <h4 className="font-bold text-lg mb-2 text-gray-800 dark:text-white">🎨 Color Coding</h4>
                      <p className="text-gray-700 dark:text-gray-300">Assign different colors to different subjects for easy visual identification and better organization.</p>
                    </div>
                    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border-l-4 border-indigo-600 shadow">
                      <h4 className="font-bold text-lg mb-2 text-gray-800 dark:text-white">💾 Auto-Save Plan</h4>
                      <p className="text-gray-700 dark:text-gray-300">Your study plan is automatically saved. Adjust it anytime and keep track of your weekly study schedule.</p>
                    </div>
                  </div>
                </div>

                {/* Features Grid */}
                <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow text-center">
                    <div className="text-4xl mb-3">📍</div>
                    <h4 className="font-bold mb-2 text-gray-800 dark:text-white">Flexible Scheduling</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Add events anytime, adjust duration</p>
                  </div>
                  <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow text-center">
                    <div className="text-4xl mb-3">⏰</div>
                    <h4 className="font-bold mb-2 text-gray-800 dark:text-white">Time Slots</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Set specific times for studying</p>
                  </div>
                  <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow text-center">
                    <div className="text-4xl mb-3">📊</div>
                    <h4 className="font-bold mb-2 text-gray-800 dark:text-white">Weekly Progress</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">See total hours planned per week</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'nlp' && (
            <div className="min-h-screen bg-gradient-to-b from-cyan-50 to-white dark:from-gray-900 dark:to-gray-800">
              <div className="max-w-7xl mx-auto px-4 py-12">
                <h2 className="text-4xl font-bold text-gray-800 dark:text-white mb-4">🤖 Natural Language Processing Tools</h2>
                <p className="text-lg text-gray-600 dark:text-gray-300 mb-12">Use AI-powered NLP tools to analyze, improve, and transform your study materials.</p>
                
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                  {/* Main CTA */}
                  <div className="lg:col-span-1">
                    <div className="bg-gradient-to-br from-cyan-600 to-blue-700 text-white rounded-xl p-8 shadow-lg">
                      <div className="text-5xl mb-4">🤖</div>
                      <h3 className="text-2xl font-bold mb-4">Open Tools</h3>
                      <p className="mb-6">Access 4 powerful NLP tools to optimize your study materials.</p>
                      <button
                        onClick={() => setShowNLP(true)}
                        className="w-full bg-white text-cyan-600 px-6 py-3 rounded-lg font-bold hover:bg-gray-100 transition-all"
                      >
                        🤖 Open NLP Tools
                      </button>
                    </div>
                  </div>

                  {/* Info Cards */}
                  <div className="lg:col-span-2 space-y-4">
                    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border-l-4 border-cyan-600 shadow">
                      <h4 className="font-bold text-lg mb-2 text-gray-800 dark:text-white">📝 Text Summarization</h4>
                      <p className="text-gray-700 dark:text-gray-300">Reduce long notes and articles into concise summaries. Extract key points and essential information to study more efficiently.</p>
                    </div>
                    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border-l-4 border-blue-600 shadow">
                      <h4 className="font-bold text-lg mb-2 text-gray-800 dark:text-white">😊 Sentiment & Grammar</h4>
                      <p className="text-gray-700 dark:text-gray-300">Analyze the tone of texts and check grammar. Improve your writing quality and understand emotional context better.</p>
                    </div>
                    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border-l-4 border-indigo-600 shadow">
                      <h4 className="font-bold text-lg mb-2 text-gray-800 dark:text-white">🔄 Paraphrasing</h4>
                      <p className="text-gray-700 dark:text-gray-300">Rephrase content in different ways for better understanding. Compare multiple interpretations of the same concept.</p>
                    </div>
                  </div>
                </div>

                {/* Features Grid */}
                <div className="mt-12 grid grid-cols-1 md:grid-cols-4 gap-6">
                  <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow text-center">
                    <div className="text-4xl mb-3">📝</div>
                    <h4 className="font-bold mb-2 text-gray-800 dark:text-white">Summarize</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Condense key points</p>
                  </div>
                  <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow text-center">
                    <div className="text-4xl mb-3">😊</div>
                    <h4 className="font-bold mb-2 text-gray-800 dark:text-white">Sentiment</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Analyze tone & emotion</p>
                  </div>
                  <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow text-center">
                    <div className="text-4xl mb-3">✏️</div>
                    <h4 className="font-bold mb-2 text-gray-800 dark:text-white">Grammar</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Check & improve writing</p>
                  </div>
                  <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow text-center">
                    <div className="text-4xl mb-3">🔄</div>
                    <h4 className="font-bold mb-2 text-gray-800 dark:text-white">Paraphrase</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Rephrase content</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'career' && (
            <div className="min-h-screen bg-gradient-to-b from-green-50 to-white dark:from-gray-900 dark:to-gray-800">
              <div className="max-w-7xl mx-auto px-4 py-12">
                <h2 className="text-4xl font-bold text-gray-800 dark:text-white mb-4">🎯 Career Counseling</h2>
                <p className="text-lg text-gray-600 dark:text-gray-300 mb-12">Get personalized career guidance with AI-powered assessment and action planning.</p>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                  {/* Main CTA */}
                  <div className="lg:col-span-1">
                    <div className="bg-gradient-to-br from-green-600 to-green-700 text-white rounded-xl p-8 shadow-lg">
                      <div className="text-5xl mb-4">🎯</div>
                      <h3 className="text-2xl font-bold mb-4">Start Your Journey</h3>
                      <p className="mb-6">Begin your personalized career counseling session with our AI career advisor</p>
                      <button
                        onClick={() => setShowCareerCounseling(true)}
                        className="w-full bg-white text-green-600 px-6 py-3 rounded-lg font-bold hover:bg-gray-100 transition-all"
                      >
                        🚀 Start Counseling
                      </button>
                    </div>
                  </div>

                  {/* Info Cards */}
                  <div className="lg:col-span-2 space-y-4">
                    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border-l-4 border-green-600 shadow">
                      <h4 className="font-bold text-lg mb-2 text-gray-800 dark:text-white">📋 Career Assessment</h4>
                      <p className="text-gray-700 dark:text-gray-300">Our AI counselor will ask targeted questions about your background, interests, and goals to understand your career aspirations.</p>
                    </div>

                    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border-l-4 border-blue-600 shadow">
                      <h4 className="font-bold text-lg mb-2 text-gray-800 dark:text-white">🎓 Personalized Action Plan</h4>
                      <p className="text-gray-700 dark:text-gray-300">Receive a comprehensive career development plan with specific subjects to study, activities to participate in, and milestones to achieve your target profession.</p>
                    </div>

                    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border-l-4 border-purple-600 shadow">
                      <h4 className="font-bold text-lg mb-2 text-gray-800 dark:text-white">📚 Academic Guidance</h4>
                      <p className="text-gray-700 dark:text-gray-300">Get recommendations for key subjects, courses, and educational pathways that will prepare you for your chosen career field.</p>
                    </div>
                  </div>
                </div>

                {/* Features Grid */}
                <div className="mt-12 grid grid-cols-1 md:grid-cols-4 gap-6">
                  <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow text-center">
                    <div className="text-4xl mb-3">🎓</div>
                    <h4 className="font-bold mb-2 text-gray-800 dark:text-white">Subject Focus</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Key academic subjects</p>
                  </div>
                  <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow text-center">
                    <div className="text-4xl mb-3">🚀</div>
                    <h4 className="font-bold mb-2 text-gray-800 dark:text-white">Activities</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Practical experiences</p>
                  </div>
                  <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow text-center">
                    <div className="text-4xl mb-3">📈</div>
                    <h4 className="font-bold mb-2 text-gray-800 dark:text-white">Skill Building</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Technical & soft skills</p>
                  </div>
                  <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow text-center">
                    <div className="text-4xl mb-3">🎯</div>
                    <h4 className="font-bold mb-2 text-gray-800 dark:text-white">Milestones</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Career progression</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </main>

        {/* Modals */}
        {showLogin && (
          <LoginForm
            onClose={() => setShowLogin(false)}
            onSwitchToRegister={handleSwitchToRegister}
            onSuccess={(msg) => addNotification(msg, 'success')}
            onError={(msg) => addNotification(msg, 'error')}
          />
        )}

        {showRegister && (
          <RegisterForm
            onClose={() => setShowRegister(false)}
            onSwitchToLogin={handleSwitchToLogin}
            onSuccess={(msg) => addNotification(msg, 'success')}
            onError={(msg) => addNotification(msg, 'error')}
          />
        )}

        {showChat && <ChatModal onClose={() => setShowChat(false)} />}

        {showProgress && <ProgressModal onClose={() => setShowProgress(false)} />}

        {showPomodoro && <PomodoroModal onClose={() => setShowPomodoro(false)} />}

        {showPlanner && <WeeklyPlannerModal onClose={() => setShowPlanner(false)} />}

        {showNLP && <NLPModal onClose={() => setShowNLP(false)} />}

        {showCareerCounseling && <CareerCounselingModal isOpen={showCareerCounseling} onClose={() => setShowCareerCounseling(false)} />}

        {/* Notifications */}
        <div className="fixed top-4 right-4 z-50 space-y-2">
          {notifications.map((notification) => (
            <Notification
              key={notification.id}
              notification={notification}
              onClose={removeNotification}
            />
          ))}
        </div>
      </div>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;

