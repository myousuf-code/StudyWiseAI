import React, { useState } from 'react';
import axios from 'axios';
import { apiService } from '../../services/api';

interface NLPModalProps {
  onClose: () => void;
}

type NLPFeature = 'summarize' | 'sentiment' | 'grammar' | 'paraphrase';

const NLPModal: React.FC<NLPModalProps> = ({ onClose }) => {
  const [activeFeature, setActiveFeature] = useState<NLPFeature>('summarize');
  const [inputText, setInputText] = useState('');
  const [outputText, setOutputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleProcess = async () => {
    if (!inputText.trim()) {
      setError('Please enter some text');
      return;
    }

    setIsLoading(true);
    setError('');
    setOutputText('');

    try {
      let result = '';

      switch (activeFeature) {
        case 'summarize': {
          const res = await apiService.summarizeText({ text: inputText });
          result = res.summary;
          break;
        }
        case 'sentiment': {
          const res = await apiService.analyzeSentiment({ text: inputText });
          result = res.sentiment;
          break;
        }
        case 'grammar': {
          const res = await apiService.checkGrammar({ text: inputText });
          result = res.result;
          break;
        }
        case 'paraphrase': {
          const res = await apiService.paraphraseText({ text: inputText });
          result = res.paraphrase;
          break;
        }
      }

      setOutputText(result);
    } catch (err: unknown) {
      if (axios.isAxiosError(err)) {
        if (err.response?.status === 401) {
          setError('Session expired. Please log in again.');
        } else if (err.response?.status === 422) {
          setError('Invalid input. Please check your text and try again.');
        } else if (err.response?.data?.detail) {
          setError(`Error: ${err.response.data.detail}`);
        } else if (err.code === 'ECONNABORTED') {
          setError('Request timed out. Please try again.');
        } else {
          setError(`Error: ${err.message}`);
        }
      } else {
        setError('Error processing text. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const features = [
    { id: 'summarize' as const, label: '📝 Summarization', description: 'Condense text into key points' },
    { id: 'sentiment' as const, label: '😊 Sentiment Analysis', description: 'Analyze emotional tone' },
    { id: 'grammar' as const, label: '✏️ Grammar Check', description: 'Check writing quality' },
    { id: 'paraphrase' as const, label: '🔄 Paraphrase', description: 'Rephrase text differently' },
  ];

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" role="dialog" aria-modal="true" aria-label="Natural Language Processing Tools">
      <div className="bg-white dark:bg-gray-800 rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-cyan-600 text-white p-6 flex justify-between items-center sticky top-0">
          <h2 className="text-2xl font-bold">🤖 Natural Language Processing</h2>
          <button
            onClick={onClose}
            className="text-2xl hover:bg-white/20 rounded-full w-10 h-10 flex items-center justify-center transition-colors"
          >
            ×
          </button>
        </div>

        <div className="p-6">
          {/* Feature Selection */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-8">
            {features.map((feature) => (
              <button
                key={feature.id}
                onClick={() => {
                  setActiveFeature(feature.id);
                  setOutputText('');
                  setError('');
                }}
                className={`p-3 rounded-lg border-2 transition-all ${
                  activeFeature === feature.id
                    ? 'border-blue-600 bg-blue-50 dark:bg-blue-900/30'
                    : 'border-gray-200 dark:border-gray-600 hover:border-blue-300'
                }`}
              >
                <p className="font-semibold text-sm dark:text-white">{feature.label}</p>
                <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">{feature.description}</p>
              </button>
            ))}
          </div>

          {/* Main Content */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Input */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                📥 Input Text
              </label>
              <textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Paste or type text here..."
                className="w-full h-64 px-4 py-3 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-lg focus:outline-none focus:border-blue-500 resize-none"
              />
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
                {inputText.length} characters
              </p>
            </div>

            {/* Output */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                📤 Output
              </label>
              <textarea
                value={outputText}
                readOnly
                placeholder="Results will appear here..."
                className="w-full h-64 px-4 py-3 border border-gray-300 dark:border-gray-600 dark:bg-gray-900 dark:text-gray-100 rounded-lg bg-gray-50 resize-none"
              />
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mt-4 p-3 bg-red-100 dark:bg-red-900/30 border border-red-400 dark:border-red-600 text-red-700 dark:text-red-300 rounded-lg text-sm">
              {error}
            </div>
          )}

          {/* Action Buttons */}
          <div className="mt-6 flex gap-3 justify-end">
            <button
              onClick={() => {
                setInputText('');
                setOutputText('');
                setError('');
              }}
              className="px-6 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors font-semibold"
            >
              Clear
            </button>
            <button
              onClick={handleProcess}
              disabled={!inputText.trim() || isLoading}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {isLoading ? (
                <>
                  <span className="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-white"></span>
                  Processing...
                </>
              ) : (
                <>⚡ Process</>
              )}
            </button>
          </div>

          {/* Info Box */}
          <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
            <p className="text-sm text-blue-800 dark:text-blue-300">
              <span className="font-semibold">💡 Tip:</span> Copy and paste any text from your study materials to analyze or improve it using these NLP tools.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NLPModal;
