import React, { useState } from 'react';
import { apiService } from '../../services/api';
import { useAuth } from '../../context/AuthContext';

interface CareerCounselingModalProps {
  isOpen: boolean;
  onClose: () => void;
}

interface CareerSession {
  session_id: number;
  target_profession: string;
  session_status: string;
  created_at: string;
  has_action_plan: boolean;
  initial_questions?: string;
  action_plan?: string;
}

const CareerCounselingModal: React.FC<CareerCounselingModalProps> = ({ isOpen, onClose }) => {
  const { isAuthenticated } = useAuth();
  const [targetProfession, setTargetProfession] = useState('');
  const [currentStep, setCurrentStep] = useState<'input' | 'questions' | 'responses' | 'plan'>('input');
  const [questions, setQuestions] = useState('');
  const [userResponses, setUserResponses] = useState('');
  const [actionPlan, setActionPlan] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [sessions, setSessions] = useState<CareerSession[]>([]);
  const [showHistory, setShowHistory] = useState(false);
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [convertingToPlan, setConvertingToPlan] = useState(false);
  const [conversionSuccess, setConversionSuccess] = useState('');

  // Extract just the profession name from free-form input like "want to become a doctor"
  const extractProfession = (input: string): string => {
    let cleaned = input.trim();
    // Remove common lead-in phrases
    cleaned = cleaned.replace(/^(i\s+)?(want|would like|hope|plan|am trying|aspire)\s+(to\s+)?(become|be|work as|pursue|study to be|get into)\s+(a\s+|an\s+)?/i, '');
    cleaned = cleaned.replace(/^(how to become|career as|career in|become a|become an|be a|be an)\s+/i, '');
    cleaned = cleaned.replace(/^(a|an)\s+/i, '');
    // Capitalize each word
    return cleaned.trim().replace(/\b\w/g, c => c.toUpperCase()) || input.trim();
  };

  const startCareerCounseling = async () => {
    if (!targetProfession.trim()) {
      setError('Please enter a profession');
      return;
    }

    const profession = extractProfession(targetProfession);
    setTargetProfession(profession); // update state to cleaned value
    console.log('Starting career counseling for:', profession);
    setLoading(true);
    setError('');
    try {
      const response = await apiService.startCareerCounseling({ target_profession: profession });
      console.log('Career counseling response:', response);
      setQuestions(response.initial_questions);
      setCurrentStep('questions');
    } catch (error: any) {
      console.error('Error starting career counseling:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to start career counseling session';
      setError(`Error: ${errorMessage}`);
    } finally {
      setLoading(false);
    }
  };

  const generateActionPlan = async () => {
    if (!userResponses.trim()) {
      setError('Please provide responses to the questions');
      return;
    }

    console.log('Generating action plan for:', targetProfession);
    setLoading(true);
    setError('');
    try {
      const response = await apiService.generateCareerActionPlan({
        target_profession: targetProfession,
        user_responses: userResponses
      });
      console.log('Action plan response:', response);
      setActionPlan(response.action_plan);
      setSessionId(response.session_id);
      setCurrentStep('plan');
    } catch (error: any) {
      console.error('Error generating action plan:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to generate career action plan';
      setError(`Error: ${errorMessage}`);
    } finally {
      setLoading(false);
    }
  };

  const loadCareerHistory = async () => {
    console.log('Loading career history...');
    setLoading(true);
    setError('');
    try {
      const response = await apiService.getCareerCounselingHistory();
      console.log('Career history response:', response);
      setSessions(response);
      setShowHistory(true);
    } catch (error: any) {
      console.error('Error loading career history:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to load career counseling history';
      setError(`Error: ${errorMessage}`);
    } finally {
      setLoading(false);
    }
  };

  const convertToStudyPlan = async () => {
    if (!sessionId) {
      setError('No session ID available for conversion');
      return;
    }

    console.log('Converting career plan to study plan...');
    setConvertingToPlan(true);
    setError('');
    setConversionSuccess('');
    try {
      const response = await apiService.convertCareerToStudyPlan({
        session_id: sessionId,
        plan_title: `Career Path: ${targetProfession}`
      });
      console.log('Conversion response:', response);
      if (response.success) {
        setConversionSuccess(`✅ ${response.message}
        
📅 Your career action plan has been converted to a study plan! 
📚 Study Plan ID: ${response.study_plan_id}
🎯 ${response.tasks_created} study tasks created
        
💡 Next Steps:
• Access your study plan from the main dashboard
• Use the Weekly Planner to schedule these tasks
• Track your progress toward your career goals`);
      }
    } catch (error: any) {
      console.error('Error converting to study plan:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to convert career plan to study plan';
      setError(`Error: ${errorMessage}`);
    } finally {
      setConvertingToPlan(false);
    }
  };

  const resetSession = () => {
    setTargetProfession('');
    setCurrentStep('input');
    setQuestions('');
    setUserResponses('');
    setActionPlan('');
    setShowHistory(false);
    setSessionId(null);
    setConvertingToPlan(false);
    setConversionSuccess('');
    setError('');
  };

  if (!isOpen) return null;

  if (!isAuthenticated) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-6 w-full max-w-md">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Login Required</h2>
          <p className="text-gray-600 mb-4">You need to be logged in to use the career counseling feature.</p>
          <div className="flex gap-4">
            <button
              onClick={onClose}
              className="flex-1 px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold text-gray-800">Career Counseling</h2>
          <div className="flex gap-2">
            <button
              onClick={loadCareerHistory}
              disabled={loading}
              className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-gray-300 transition-colors"
            >
              View History
            </button>
            <button
              onClick={onClose}
              disabled={loading}
              className="text-gray-500 hover:text-gray-700 text-xl disabled:opacity-50"
            >
              ×
            </button>
          </div>
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            <p className="font-semibold">Error</p>
            <p className="text-sm">{error}</p>
            {error.includes('timeout') && (
              <p className="text-sm mt-2">The AI model is processing your request. This may take 1-2 minutes. Please wait...</p>
            )}
          </div>
        )}

        {conversionSuccess && (
          <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg text-green-700">
            <p className="font-semibold">Success</p>
            <p className="text-sm">{conversionSuccess}</p>
          </div>
        )}

        {loading && (
          <div className="mb-4 p-4 bg-blue-50 border border-blue-200 rounded-lg text-blue-700">
            <p className="font-semibold">Processing...</p>
            <p className="text-sm">The AI model is generating your response. This may take a moment.</p>
          </div>
        )}

        {showHistory ? (
          <div>
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-semibold">Career Counseling History</h3>
              <button
                onClick={() => setShowHistory(false)}
                className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors"
              >
                Back to Counseling
              </button>
            </div>
            <div className="space-y-4">
              {sessions.length === 0 ? (
                <p className="text-gray-600">No career counseling sessions found.</p>
              ) : (
                sessions.map((session) => (
                  <div key={session.session_id} className="border rounded-lg p-4 bg-gray-50">
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="font-semibold text-lg">{session.target_profession}</h4>
                      <span className={`px-2 py-1 rounded text-sm ${
                        session.session_status === 'completed' ? 'bg-green-100 text-green-800' :
                        session.session_status === 'active' ? 'bg-blue-100 text-blue-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {session.session_status}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mb-2">
                      Started: {new Date(session.created_at).toLocaleDateString()}
                    </p>
                    {session.has_action_plan && session.action_plan && (
                      <div className="mt-4">
                        <h5 className="font-medium mb-2">Action Plan:</h5>
                        <div className="bg-white p-3 rounded border text-sm whitespace-pre-wrap max-h-40 overflow-y-auto">
                          {session.action_plan}
                        </div>
                        <div className="mt-3">
                          <button
                            onClick={async () => {
                              setConvertingToPlan(true);
                              try {
                                const response = await apiService.convertCareerToStudyPlan({
                                  session_id: session.session_id,
                                  plan_title: `Career Path: ${session.target_profession}`
                                });
                                if (response.success) {
                                  setConversionSuccess(`✅ ${response.message}
                                  
📅 Career plan converted to study plan!
📚 Study Plan ID: ${response.study_plan_id}
🎯 ${response.tasks_created} study tasks created

💡 Access your new study plan from the dashboard!`);
                                }
                              } catch (error: any) {
                                const errorMessage = error.response?.data?.detail || error.message || 'Failed to convert';
                                setError(`Conversion error: ${errorMessage}`);
                              } finally {
                                setConvertingToPlan(false);
                              }
                            }}
                            disabled={convertingToPlan}
                            className="px-3 py-1 bg-purple-500 text-white rounded text-sm hover:bg-purple-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                          >
                            {convertingToPlan ? 'Converting...' : '📅 Add to Study Planner'}
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                ))
              )}
            </div>
          </div>
        ) : (
          <>
            {currentStep === 'input' && (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    What profession are you interested in pursuing?
                  </label>
                  <input
                    type="text"
                    value={targetProfession}
                    onChange={(e) => setTargetProfession(e.target.value)}
                    placeholder="e.g., Software Engineer, Doctor, Teacher, Data Scientist..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div className="flex gap-4">
                  <button
                    onClick={startCareerCounseling}
                    disabled={!targetProfession.trim() || loading}
                    className="px-6 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                  >
                    {loading ? 'Starting...' : 'Start Career Counseling'}
                  </button>
                  <button
                    onClick={resetSession}
                    className="px-6 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors"
                  >
                    Reset
                  </button>
                </div>
              </div>
            )}

            {currentStep === 'questions' && (
              <div className="space-y-4">
                <div>
                  <h3 className="text-lg font-semibold mb-2">Career Assessment Questions</h3>
                  <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-400">
                    <pre className="whitespace-pre-wrap text-gray-800">{questions}</pre>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Your responses to these questions:
                  </label>
                  <textarea
                    value={userResponses}
                    onChange={(e) => setUserResponses(e.target.value)}
                    placeholder="Please answer the questions above in detail..."
                    rows={8}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div className="flex gap-4">
                  <button
                    onClick={generateActionPlan}
                    disabled={!userResponses.trim() || loading}
                    className="px-6 py-2 bg-green-500 text-white rounded hover:bg-green-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                  >
                    {loading ? 'Generating Plan...' : 'Generate Action Plan'}
                  </button>
                  <button
                    onClick={() => setCurrentStep('input')}
                    className="px-6 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors"
                  >
                    Back
                  </button>
                </div>
              </div>
            )}

            {currentStep === 'plan' && (
              <div className="space-y-4">
                <div>
                  <h3 className="text-lg font-semibold mb-2">Your Career Action Plan for {targetProfession}</h3>
                  <div className="bg-green-50 p-4 rounded-lg border-l-4 border-green-400 max-h-96 overflow-y-auto">
                    <pre className="whitespace-pre-wrap text-gray-800">{actionPlan}</pre>
                  </div>
                </div>
                <div className="flex gap-4">
                  <button
                    onClick={convertToStudyPlan}
                    disabled={convertingToPlan || !sessionId}
                    className="px-6 py-2 bg-purple-500 text-white rounded hover:bg-purple-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                  >
                    {convertingToPlan ? 'Converting...' : '📅 Add to Study Planner'}
                  </button>
                  <button
                    onClick={resetSession}
                    className="px-6 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
                  >
                    Start New Session
                  </button>
                  <button
                    onClick={() => setCurrentStep('input')}
                    className="px-6 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors"
                  >
                    Back
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default CareerCounselingModal;