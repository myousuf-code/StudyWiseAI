import React, { useState } from 'react';

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
        case 'summarize':
          result = await processSummarization();
          break;
        case 'sentiment':
          result = await processSentiment();
          break;
        case 'grammar':
          result = await processGrammarCheck();
          break;
        case 'paraphrase':
          result = await processParaphrase();
          break;
      }

      setOutputText(result);
    } catch (err) {
      setError('Error processing text. Please try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const processSummarization = async () => {
    // For now, return mock response
    // Later this will call: apiService.summarizeText({ text: inputText })
    return `Summary: This is a concise summary of your text. Key points include the main topics and important information from the original content.`;
  };

  const processSentiment = async () => {
    // For now, return mock response
    // Later this will call: apiService.analyzeSentiment({ text: inputText })
    return `Sentiment Analysis:\n- Overall Sentiment: Positive\n- Confidence: 85%\n- Tone: Professional and informative`;
  };

  const processGrammarCheck = async () => {
    // For now, return mock response
    // Later this will call: apiService.checkGrammar({ text: inputText })
    return `Grammar Check:\n✓ Spelling: Correct\n✓ Punctuation: Good\n✓ Grammar: No major issues found\n- Suggestions: Consider varying sentence structure for better readability`;
  };

  const processParaphrase = async () => {
    // For now, return mock response
    // Later this will call: apiService.paraphraseText({ text: inputText })
    return `Paraphrase: In an alternative form of expression, the key ideas from your original text can be restated as follows. This rephrasing maintains the core meaning while using different vocabulary and sentence structures.`;
  };

  const features = [
    { id: 'summarize' as const, label: '📝 Summarization', description: 'Condense text into key points' },
    { id: 'sentiment' as const, label: '😊 Sentiment Analysis', description: 'Analyze emotional tone' },
    { id: 'grammar' as const, label: '✏️ Grammar Check', description: 'Check writing quality' },
    { id: 'paraphrase' as const, label: '🔄 Paraphrase', description: 'Rephrase text differently' },
  ];

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
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
                    ? 'border-blue-600 bg-blue-50'
                    : 'border-gray-200 hover:border-blue-300'
                }`}
              >
                <p className="font-semibold text-sm">{feature.label}</p>
                <p className="text-xs text-gray-600 mt-1">{feature.description}</p>
              </button>
            ))}
          </div>

          {/* Main Content */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Input */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                📥 Input Text
              </label>
              <textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Paste or type text here..."
                className="w-full h-64 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 resize-none"
              />
              <p className="text-xs text-gray-500 mt-2">
                {inputText.length} characters
              </p>
            </div>

            {/* Output */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                📤 Output
              </label>
              <textarea
                value={outputText}
                readOnly
                placeholder="Results will appear here..."
                className="w-full h-64 px-4 py-3 border border-gray-300 rounded-lg bg-gray-50 resize-none"
              />
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg text-sm">
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
              className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-semibold"
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
          <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <p className="text-sm text-blue-800">
              <span className="font-semibold">💡 Tip:</span> Copy and paste any text from your study materials to analyze or improve it using these NLP tools.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NLPModal;
