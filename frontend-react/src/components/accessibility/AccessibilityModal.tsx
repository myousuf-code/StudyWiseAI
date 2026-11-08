import React, { useState, useEffect, useRef } from 'react';
import { useAccessibility } from '../../context/AccessibilityContext';

interface AccessibilityModalProps {
  onClose: () => void;
  initialText?: string;
}

const Toggle: React.FC<{
  checked: boolean;
  onChange: () => void;
  label: string;
  description: string;
}> = ({ checked, onChange, label, description }) => (
  <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/60 rounded-lg">
    <div>
      <p className="font-semibold text-gray-800 dark:text-white">{label}</p>
      <p className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">{description}</p>
    </div>
    <button
      role="switch"
      aria-checked={checked}
      aria-label={label}
      onClick={onChange}
      className={`relative inline-flex h-7 w-14 flex-shrink-0 items-center rounded-full transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 ${
        checked ? 'bg-indigo-600' : 'bg-gray-300 dark:bg-gray-500'
      }`}
    >
      <span
        className={`inline-block h-5 w-5 transform rounded-full bg-white shadow-md transition-transform ${
          checked ? 'translate-x-8' : 'translate-x-1'
        }`}
      />
    </button>
  </div>
);

const AccessibilityModal: React.FC<AccessibilityModalProps> = ({ onClose, initialText = '' }) => {
  const { settings, updateSetting, resetSettings } = useAccessibility();
  const [ttsText, setTtsText] = useState(initialText);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const ttsSupported = useRef('speechSynthesis' in window).current;

  // Sync speaking state with the browser synthesis engine
  useEffect(() => {
    const id = setInterval(() => {
      if (ttsSupported) {
        const speaking = window.speechSynthesis.speaking && !window.speechSynthesis.paused;
        setIsSpeaking(speaking);
        setIsPaused(window.speechSynthesis.paused);
      }
    }, 300);
    return () => clearInterval(id);
  }, [ttsSupported]);

  // Stop speech when modal unmounts
  useEffect(() => {
    return () => { if (ttsSupported) window.speechSynthesis.cancel(); };
  }, [ttsSupported]);

  const handleSpeak = () => {
    if (!ttsSupported || !ttsText.trim()) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(ttsText);
    utterance.rate = settings.ttsRate;
    utterance.onend = () => { setIsSpeaking(false); setIsPaused(false); };
    utterance.onerror = () => { setIsSpeaking(false); setIsPaused(false); };
    window.speechSynthesis.speak(utterance);
  };

  const handleStop = () => {
    window.speechSynthesis.cancel();
    setIsSpeaking(false);
    setIsPaused(false);
  };

  const handlePauseResume = () => {
    if (window.speechSynthesis.paused) {
      window.speechSynthesis.resume();
    } else {
      window.speechSynthesis.pause();
    }
  };

  return (
    <div
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
      role="dialog"
      aria-modal="true"
      aria-label="Accessibility Settings"
    >
      <div className="bg-white dark:bg-gray-800 rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto shadow-2xl">
        {/* Header */}
        <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-6 flex justify-between items-center sticky top-0 rounded-t-xl z-10">
          <div>
            <h2 className="text-2xl font-bold">♿ Accessibility Settings</h2>
            <p className="text-indigo-100 text-sm mt-1">Customize your experience for easier reading and interaction</p>
          </div>
          <button
            onClick={onClose}
            className="text-2xl hover:bg-white/20 rounded-full w-10 h-10 flex items-center justify-center transition-colors"
            aria-label="Close accessibility settings"
          >
            ×
          </button>
        </div>

        <div className="p-6 space-y-8">

          {/* ── Vision ── */}
          <section aria-label="Vision settings">
            <h3 className="text-lg font-bold text-gray-800 dark:text-white mb-4">👁️ Vision</h3>
            <div className="space-y-4">

              {/* Font Size */}
              <div>
                <p className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Text Size</p>
                <div className="flex gap-2">
                  {(['normal', 'large', 'xl'] as const).map((size, i) => (
                    <button
                      key={size}
                      onClick={() => updateSetting('fontSize', size)}
                      aria-pressed={settings.fontSize === size}
                      className={`flex-1 py-2 rounded-lg border-2 font-semibold transition-all ${
                        ['text-base', 'text-lg', 'text-xl'][i]
                      } ${
                        settings.fontSize === size
                          ? 'border-indigo-600 bg-indigo-50 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300'
                          : 'border-gray-200 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:border-indigo-300'
                      }`}
                    >
                      {['Normal', 'Large', 'Extra Large'][i]}
                    </button>
                  ))}
                </div>
              </div>

              <Toggle
                checked={settings.highContrast}
                onChange={() => updateSetting('highContrast', !settings.highContrast)}
                label="High Contrast Mode"
                description="Inverts colours for maximum contrast — ideal for low-vision users"
              />
            </div>
          </section>

          {/* ── Reading ── */}
          <section aria-label="Reading assistance settings">
            <h3 className="text-lg font-bold text-gray-800 dark:text-white mb-4">📖 Reading Assistance</h3>
            <div className="space-y-3">
              <Toggle
                checked={settings.dyslexicFont}
                onChange={() => updateSetting('dyslexicFont', !settings.dyslexicFont)}
                label="Dyslexia-Friendly Font"
                description="Switches to Verdana with wider letter & word spacing for easier decoding"
              />
              <Toggle
                checked={settings.lineSpacing}
                onChange={() => updateSetting('lineSpacing', !settings.lineSpacing)}
                label="Increased Line & Letter Spacing"
                description="Adds extra space between lines and letters to reduce crowding"
              />
            </div>
          </section>

          {/* ── Motion ── */}
          <section aria-label="Motion settings">
            <h3 className="text-lg font-bold text-gray-800 dark:text-white mb-4">🎬 Motion</h3>
            <Toggle
              checked={settings.reducedMotion}
              onChange={() => updateSetting('reducedMotion', !settings.reducedMotion)}
              label="Reduce Motion"
              description="Disables animations and transitions (helps with vestibular / seizure disorders)"
            />
          </section>

          {/* ── Text-to-Speech ── */}
          <section aria-label="Text to speech">
            <h3 className="text-lg font-bold text-gray-800 dark:text-white mb-4">🔊 Text-to-Speech</h3>

            {!ttsSupported ? (
              <div className="p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-300 dark:border-yellow-700 rounded-lg text-yellow-800 dark:text-yellow-300 text-sm">
                Text-to-Speech is not supported in your browser. Try Chrome, Edge, or Safari.
              </div>
            ) : (
              <div className="space-y-4">
                <div>
                  <label htmlFor="a11y-tts-text" className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">
                    Text to read aloud
                    <span className="font-normal text-gray-400 dark:text-gray-500 ml-2">
                      — highlight text on the page before opening this panel to auto-fill
                    </span>
                  </label>
                  <textarea
                    id="a11y-tts-text"
                    value={ttsText}
                    onChange={(e) => setTtsText(e.target.value)}
                    placeholder="Paste or type text here…"
                    className="w-full h-28 px-3 py-2 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-lg focus:outline-none focus:border-indigo-500 resize-none text-sm"
                  />
                </div>

                {/* Speed slider */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">
                    Reading Speed:{' '}
                    <span className="text-indigo-600 dark:text-indigo-400">{settings.ttsRate.toFixed(1)}×</span>
                  </label>
                  <input
                    type="range"
                    min={0.5}
                    max={2.0}
                    step={0.1}
                    value={settings.ttsRate}
                    onChange={(e) => updateSetting('ttsRate', parseFloat(e.target.value))}
                    className="w-full accent-indigo-600"
                    aria-label="Reading speed"
                  />
                  <div className="flex justify-between text-xs text-gray-400 mt-1 select-none">
                    <span>0.5× Slow</span><span>1.0× Normal</span><span>2.0× Fast</span>
                  </div>
                </div>

                {/* Controls */}
                <div className="flex gap-3">
                  <button
                    onClick={isSpeaking ? handleStop : handleSpeak}
                    disabled={!ttsText.trim()}
                    className={`flex-1 py-2 rounded-lg font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 ${
                      isSpeaking
                        ? 'bg-red-500 hover:bg-red-600 text-white'
                        : 'bg-indigo-600 hover:bg-indigo-700 text-white'
                    }`}
                  >
                    {isSpeaking ? '⏹ Stop' : '▶ Read Aloud'}
                  </button>
                  {(isSpeaking || isPaused) && (
                    <button
                      onClick={handlePauseResume}
                      className="px-4 py-2 bg-gray-200 dark:bg-gray-600 text-gray-800 dark:text-white rounded-lg hover:bg-gray-300 dark:hover:bg-gray-500 transition-colors font-semibold"
                    >
                      {isPaused ? '▶ Resume' : '⏸ Pause'}
                    </button>
                  )}
                </div>
              </div>
            )}
          </section>

          {/* Footer */}
          <div className="flex justify-between items-center pt-4 border-t border-gray-200 dark:border-gray-700">
            <button
              onClick={resetSettings}
              className="px-4 py-2 text-sm border border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-400 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
            >
              Reset to Defaults
            </button>
            <button
              onClick={onClose}
              className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-semibold"
            >
              Done
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AccessibilityModal;
