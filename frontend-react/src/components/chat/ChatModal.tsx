import React, { useState, useRef, useEffect, useCallback } from 'react';
import type { ChatMessage } from '../../types';
import { apiService } from '../../services/api';

interface ChatModalProps {
  onClose: () => void;
}

const CHAT_STORAGE_KEY = 'studywiseai_chat_history';
const API_BASE = import.meta.env.VITE_API_URL || '/api';

function loadHistory(): ChatMessage[] {
  try {
    const raw = sessionStorage.getItem(CHAT_STORAGE_KEY);
    if (raw) return JSON.parse(raw) as ChatMessage[];
  } catch { /* ignore */ }
  return [{
    role: 'assistant',
    content: "Hello! I'm your AI study assistant. How can I help you today?",
    timestamp: new Date().toISOString(),
    id: 'init',
  }];
}

const ChatModal: React.FC<ChatModalProps> = ({ onClose }) => {
  const [messages, setMessages] = useState<ChatMessage[]>(loadHistory);
  const [input, setInput] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [modelStatus, setModelStatus] = useState<'checking' | 'loading' | 'ready' | 'failed'>('checking');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const abortRef = useRef<AbortController | null>(null);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => { scrollToBottom(); }, [messages, scrollToBottom]);

  useEffect(() => {
    sessionStorage.setItem(CHAT_STORAGE_KEY, JSON.stringify(messages));
  }, [messages]);

  // Poll AI status while loading
  useEffect(() => {
    let timer: ReturnType<typeof setTimeout>;
    const checkStatus = () => {
      apiService.getAiStatus()
        .then((s) => {
          if (s.model_loaded) {
            setModelStatus('ready');
          } else if (s.model_loading) {
            setModelStatus('loading');
            timer = setTimeout(checkStatus, 5000);
          } else {
            setModelStatus('failed');
          }
        })
        .catch(() => setModelStatus('failed'));
    };
    checkStatus();
    return () => clearTimeout(timer);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isStreaming) return;

    const userText = input.trim();
    const aiMsgId = `ai-${Date.now()}`;

    setMessages((prev) => [
      ...prev,
      { role: 'user', content: userText, timestamp: new Date().toISOString(), id: `user-${Date.now()}` },
      { role: 'assistant', content: '', timestamp: new Date().toISOString(), id: aiMsgId },
    ]);
    setInput('');
    setIsStreaming(true);

    const abort = new AbortController();
    abortRef.current = abort;

    try {
      const token = sessionStorage.getItem('authToken');
      const res = await fetch(`${API_BASE}/ai/chat/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({ message: userText }),
        signal: abort.signal,
      });

      if (!res.ok || !res.body) {
        throw new Error(`HTTP ${res.status}`);
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() ?? '';

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue;
          const raw = line.slice(6).trim();
          if (!raw) continue;
          try {
            const parsed = JSON.parse(raw);
            if (parsed.token) {
              setMessages((prev) =>
                prev.map((m) =>
                  m.id === aiMsgId ? { ...m, content: m.content + parsed.token } : m
                )
              );
            }
          } catch { /* skip malformed SSE */ }
        }
      }
    } catch (err: unknown) {
      if (err instanceof Error && err.name === 'AbortError') return;
      setMessages((prev) =>
        prev.map((m) =>
          m.id === aiMsgId
            ? { ...m, content: m.content || 'Sorry, an error occurred. Please try again.' }
            : m
        )
      );
    } finally {
      setIsStreaming(false);
      abortRef.current = null;
    }
  };

  const handleStop = () => {
    abortRef.current?.abort();
    setIsStreaming(false);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" role="dialog" aria-modal="true" aria-label="AI Study Assistant Chat">
      <div className="bg-white dark:bg-gray-800 rounded-lg w-full max-w-2xl h-[600px] mx-4 flex flex-col">

        <div className="p-4 border-b dark:border-gray-700 flex justify-between items-center flex-shrink-0">
          <div className="flex items-center gap-2">
            <h3 className="text-xl font-semibold dark:text-white">💬 AI Study Assistant</h3>
            {modelStatus === 'ready' && (
              <span className="text-xs px-2 py-0.5 bg-green-100 dark:bg-green-900/40 text-green-700 dark:text-green-400 rounded-full">ready</span>
            )}
          </div>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 text-2xl leading-none" aria-label="Close chat">×</button>
        </div>

        {modelStatus === 'loading' && (
          <div className="px-4 py-2 bg-blue-50 dark:bg-blue-900/30 border-b border-blue-200 dark:border-blue-700 text-sm text-blue-800 dark:text-blue-300 flex items-center gap-2 flex-shrink-0">
            <span className="inline-block w-2 h-2 rounded-full bg-blue-500 animate-pulse" />
            AI model loading — first response may take a moment.
          </div>
        )}
        {modelStatus === 'failed' && (
          <div className="px-4 py-2 bg-amber-50 dark:bg-amber-900/30 border-b border-amber-200 dark:border-amber-700 text-sm text-amber-800 dark:text-amber-300 flex-shrink-0">
            ⚠️ AI unavailable — add <code className="font-mono bg-amber-100 dark:bg-amber-800 px-1 rounded">GROQ_API_KEY</code> to .env and restart.
          </div>
        )}

        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {messages.map((message) => (
            <div key={message.id ?? message.timestamp} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[80%] px-4 py-2.5 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap ${
                message.role === 'user'
                  ? 'bg-blue-600 text-white rounded-br-sm'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-100 rounded-bl-sm'
              }`}>
                {message.content}
                {isStreaming && message.role === 'assistant' && message === messages[messages.length - 1] && (
                  <span className="inline-block w-0.5 h-4 bg-current ml-0.5 align-middle animate-pulse" />
                )}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        <form onSubmit={handleSubmit} className="p-4 border-t dark:border-gray-700 flex gap-2 flex-shrink-0">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question..."
            className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600 disabled:opacity-50"
            disabled={isStreaming}
            autoFocus
          />
          {isStreaming ? (
            <button type="button" onClick={handleStop} className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors text-sm">
              Stop
            </button>
          ) : (
            <button type="submit" disabled={!input.trim()} className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:bg-blue-300 disabled:cursor-not-allowed">
              Send
            </button>
          )}
        </form>
      </div>
    </div>
  );
};

export default ChatModal;
