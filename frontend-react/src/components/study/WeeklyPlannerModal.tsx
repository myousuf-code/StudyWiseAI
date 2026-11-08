import React, { useState, useEffect } from 'react';
import { apiService } from '../../services/api';

interface StudyEvent {
  id: string;
  subject: string;
  time: string;
  duration: number; // in minutes
  day: string;
  color: string;
}

interface WeeklyPlannerModalProps {
  onClose: () => void;
}

// Static color map — full class names so Tailwind never purges them
const COLOR_CLASSES: Record<string, { btn: string; event: string }> = {
  blue:   { btn: 'bg-blue-300',   event: 'bg-blue-100 border-l-4 border-blue-500' },
  green:  { btn: 'bg-green-300',  event: 'bg-green-100 border-l-4 border-green-500' },
  orange: { btn: 'bg-orange-300', event: 'bg-orange-100 border-l-4 border-orange-500' },
  purple: { btn: 'bg-purple-300', event: 'bg-purple-100 border-l-4 border-purple-500' },
  red:    { btn: 'bg-red-300',    event: 'bg-red-100 border-l-4 border-red-500' },
};

const PLAN_TITLE = '__weekly_planner__';

const WeeklyPlannerModal: React.FC<WeeklyPlannerModalProps> = ({ onClose }) => {
  const [events, setEvents] = useState<StudyEvent[]>([]);
  const [selectedDay, setSelectedDay] = useState('Monday');
  const [subject, setSubject] = useState('');
  const [time, setTime] = useState('09:00');
  const [duration, setDuration] = useState(30);
  const [color, setColor] = useState('blue');
  const [saveStatus, setSaveStatus] = useState('');
  const [inputError, setInputError] = useState('');
  const [planId, setPlanId] = useState<number | null>(null);

  const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

  // Load persisted plan on mount
  useEffect(() => {
    const load = async () => {
      try {
        const plans = await apiService.getStudyPlans();
        const existing = (plans as any[]).find((p: any) => p.title === PLAN_TITLE);
        if (existing) {
          setPlanId(existing.id);
          const savedEvents = existing.schedule?.events ?? [];
          setEvents(savedEvents);
        }
      } catch {
        // Network error — fall back gracefully, no alert
      }
    };
    load();
  }, []);

  const persist = async (updatedEvents: StudyEvent[]) => {
    try {
      if (planId) {
        await apiService.updateStudyPlan(planId, {
          title: PLAN_TITLE,
          description: 'Weekly planner data',
          subject: 'General',
          difficulty_level: 'beginner',
          estimated_duration: 0,
          schedule: { events: updatedEvents },
        });
      } else {
        const created = await apiService.createStudyPlan({
          title: PLAN_TITLE,
          description: 'Weekly planner data',
          subject: 'General',
          difficulty_level: 'beginner',
          estimated_duration: 0,
          schedule: { events: updatedEvents },
        });
        setPlanId((created as any).id);
      }
      setSaveStatus('Saved');
      setTimeout(() => setSaveStatus(''), 2000);
    } catch {
      setSaveStatus('Save failed');
      setTimeout(() => setSaveStatus(''), 3000);
    }
  };

  const handleAddEvent = () => {
    if (!subject.trim()) {
      setInputError('Please enter a subject');
      return;
    }
    if (!time) {
      setInputError('Please enter a time');
      return;
    }
    setInputError('');

    const newEvent: StudyEvent = {
      id: Date.now().toString(),
      subject: subject.trim(),
      time,
      duration,
      day: selectedDay,
      color,
    };

    const updated = [...events, newEvent];
    setEvents(updated);
    persist(updated);
    setSubject('');
    setTime('09:00');
    setDuration(30);
    setColor('blue');
  };

  const handleDeleteEvent = (id: string) => {
    const updated = events.filter((e) => e.id !== id);
    setEvents(updated);
    persist(updated);
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" role="dialog" aria-modal="true" aria-label="Weekly Study Planner">
      <div className="bg-white dark:bg-gray-800 rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="bg-gradient-to-r from-orange-600 to-yellow-600 text-white p-6 flex justify-between items-center sticky top-0">
          <h2 className="text-2xl font-bold">📅 Weekly Study Planner</h2>
          <div className="flex items-center gap-3">
            {saveStatus && (
              <span className={`text-sm font-medium ${saveStatus === 'Saved' ? 'text-green-200' : 'text-red-200'}`}>
                {saveStatus}
              </span>
            )}
            <button
              onClick={onClose}
              className="text-2xl hover:bg-white/20 rounded-full w-10 h-10 flex items-center justify-center transition-colors"
              aria-label="Close weekly planner"
            >
              ×
            </button>
          </div>
        </div>

        <div className="p-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Add Event Form */}
            <div className="lg:col-span-1 bg-gray-50 dark:bg-gray-700 p-4 rounded-lg border border-gray-200 dark:border-gray-600">
              <h3 className="font-bold text-lg mb-4 dark:text-white">Add Study Event</h3>

              {inputError && (
                <p className="text-red-500 text-sm mb-3">{inputError}</p>
              )}

              <div className="mb-4">
                <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">📚 Subject</label>
                <input
                  type="text"
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                  placeholder="e.g., Calculus, Biology"
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 dark:bg-gray-600 dark:text-white rounded-lg focus:outline-none focus:border-orange-500"
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">📍 Day</label>
                <select
                  value={selectedDay}
                  onChange={(e) => setSelectedDay(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 dark:bg-gray-600 dark:text-white rounded-lg focus:outline-none focus:border-orange-500"
                >
                  {days.map((day) => <option key={day} value={day}>{day}</option>)}
                </select>
              </div>

              <div className="mb-4">
                <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">🕐 Time</label>
                <input
                  type="time"
                  value={time}
                  onChange={(e) => setTime(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 dark:bg-gray-600 dark:text-white rounded-lg focus:outline-none focus:border-orange-500"
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">⏱️ Duration (minutes)</label>
                <select
                  value={duration}
                  onChange={(e) => setDuration(parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 dark:bg-gray-600 dark:text-white rounded-lg focus:outline-none focus:border-orange-500"
                >
                  <option value="30">30 min</option>
                  <option value="45">45 min</option>
                  <option value="60">1 hour</option>
                  <option value="90">1.5 hours</option>
                  <option value="120">2 hours</option>
                </select>
              </div>

              <div className="mb-6">
                <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">🎨 Color</label>
                <div className="flex gap-2">
                  {Object.keys(COLOR_CLASSES).map((c) => (
                    <button
                      key={c}
                      onClick={() => setColor(c)}
                      aria-label={`Select ${c} color`}
                      className={`w-8 h-8 rounded-full border-2 ${color === c ? 'border-gray-800' : 'border-gray-300'} ${COLOR_CLASSES[c].btn}`}
                    />
                  ))}
                </div>
              </div>

              <button
                onClick={handleAddEvent}
                className="w-full bg-orange-600 text-white py-2 rounded-lg font-semibold hover:bg-orange-700 transition-colors"
              >
                ➕ Add Event
              </button>
            </div>

            {/* Calendar View */}
            <div className="lg:col-span-2">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {days.map((day) => (
                  <div key={day} className="border border-gray-200 dark:border-gray-600 rounded-lg p-4">
                    <h4 className="font-bold text-lg text-gray-800 dark:text-white mb-3">{day}</h4>
                    <div className="space-y-2">
                      {events
                        .filter((e) => e.day === day)
                        .sort((a, b) => a.time.localeCompare(b.time))
                        .map((event) => (
                          <div key={event.id} className={`p-3 rounded-lg ${COLOR_CLASSES[event.color]?.event ?? COLOR_CLASSES.blue.event}`}>
                            <div className="flex justify-between items-start">
                              <div>
                                <p className="font-semibold text-sm">{event.subject}</p>
                                <p className="text-xs text-gray-600">{event.time} • {event.duration}min</p>
                              </div>
                              <button
                                onClick={() => handleDeleteEvent(event.id)}
                                className="text-red-500 hover:text-red-700 font-bold text-lg"
                                aria-label={`Remove ${event.subject} from ${event.day}`}
                              >
                                ×
                              </button>
                            </div>
                          </div>
                        ))}
                      {events.filter((e) => e.day === day).length === 0 && (
                        <p className="text-gray-400 dark:text-gray-500 text-sm italic">No events planned</p>
                      )}
                    </div>
                  </div>
                ))}
              </div>

              {events.length > 0 && (
                <div className="mt-6 bg-blue-50 dark:bg-blue-900/30 border border-blue-200 dark:border-blue-700 rounded-lg p-4">
                  <p className="text-sm text-gray-700 dark:text-gray-300">
                    <span className="font-bold">📊 Weekly Summary:</span> {events.length} study sessions planned •{' '}
                    {Math.round(events.reduce((sum, e) => sum + e.duration, 0) / 60 * 10) / 10}h total
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WeeklyPlannerModal;
