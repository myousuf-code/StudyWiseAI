import React, { useState } from 'react';

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

const WeeklyPlannerModal: React.FC<WeeklyPlannerModalProps> = ({ onClose }) => {
  const [events, setEvents] = useState<StudyEvent[]>([]);
  const [selectedDay, setSelectedDay] = useState('Monday');
  const [subject, setSubject] = useState('');
  const [time, setTime] = useState('09:00');
  const [duration, setDuration] = useState(30);
  const [color, setColor] = useState('blue');

  const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  const colors = {
    blue: 'bg-blue-100 border-l-4 border-blue-500',
    green: 'bg-green-100 border-l-4 border-green-500',
    orange: 'bg-orange-100 border-l-4 border-orange-500',
    purple: 'bg-purple-100 border-l-4 border-purple-500',
    red: 'bg-red-100 border-l-4 border-red-500',
  };

  const handleAddEvent = () => {
    if (!subject || !time) {
      alert('Please fill in subject and time');
      return;
    }

    const newEvent: StudyEvent = {
      id: Date.now().toString(),
      subject,
      time,
      duration,
      day: selectedDay,
      color,
    };

    setEvents([...events, newEvent]);
    setSubject('');
    setTime('09:00');
    setDuration(30);
    setColor('blue');
  };

  const handleDeleteEvent = (id: string) => {
    setEvents(events.filter((e) => e.id !== id));
  };

  const handleSaveWeek = () => {
    localStorage.setItem('studyPlan', JSON.stringify(events));
    alert('📅 Study plan saved successfully!');
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="bg-gradient-to-r from-orange-600 to-yellow-600 text-white p-6 flex justify-between items-center sticky top-0">
          <h2 className="text-2xl font-bold">📅 Weekly Study Planner</h2>
          <button
            onClick={onClose}
            className="text-2xl hover:bg-white/20 rounded-full w-10 h-10 flex items-center justify-center transition-colors"
          >
            ×
          </button>
        </div>

        <div className="p-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Add Event Form */}
            <div className="lg:col-span-1 bg-gray-50 p-4 rounded-lg border border-gray-200">
              <h3 className="font-bold text-lg mb-4">Add Study Event</h3>

              <div className="mb-4">
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  📚 Subject
                </label>
                <input
                  type="text"
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                  placeholder="e.g., Calculus, Biology"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-orange-500"
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  📍 Day
                </label>
                <select
                  value={selectedDay}
                  onChange={(e) => setSelectedDay(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-orange-500"
                >
                  {days.map((day) => (
                    <option key={day} value={day}>
                      {day}
                    </option>
                  ))}
                </select>
              </div>

              <div className="mb-4">
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  🕐 Time
                </label>
                <input
                  type="time"
                  value={time}
                  onChange={(e) => setTime(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-orange-500"
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  ⏱️ Duration (minutes)
                </label>
                <select
                  value={duration}
                  onChange={(e) => setDuration(parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-orange-500"
                >
                  <option value="30">30 min</option>
                  <option value="45">45 min</option>
                  <option value="60">1 hour</option>
                  <option value="90">1.5 hours</option>
                  <option value="120">2 hours</option>
                </select>
              </div>

              <div className="mb-6">
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  🎨 Color
                </label>
                <div className="flex gap-2">
                  {Object.keys(colors).map((c) => (
                    <button
                      key={c}
                      onClick={() => setColor(c)}
                      className={`w-8 h-8 rounded-full border-2 ${
                        color === c ? 'border-gray-800' : 'border-gray-300'
                      } bg-${c}-300`}
                    ></button>
                  ))}
                </div>
              </div>

              <button
                onClick={handleAddEvent}
                className="w-full bg-orange-600 text-white py-2 rounded-lg font-semibold hover:bg-orange-700 transition-colors mb-2"
              >
                ➕ Add Event
              </button>

              <button
                onClick={handleSaveWeek}
                className="w-full bg-green-600 text-white py-2 rounded-lg font-semibold hover:bg-green-700 transition-colors"
              >
                💾 Save Week
              </button>
            </div>

            {/* Calendar View */}
            <div className="lg:col-span-2">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {days.map((day) => (
                  <div key={day} className="border border-gray-200 rounded-lg p-4">
                    <h4 className="font-bold text-lg text-gray-800 mb-3">{day}</h4>
                    <div className="space-y-2">
                      {events
                        .filter((e) => e.day === day)
                        .sort((a, b) => a.time.localeCompare(b.time))
                        .map((event) => (
                          <div
                            key={event.id}
                            className={`p-3 rounded-lg ${
                              colors[event.color as keyof typeof colors]
                            }`}
                          >
                            <div className="flex justify-between items-start">
                              <div>
                                <p className="font-semibold text-sm">{event.subject}</p>
                                <p className="text-xs text-gray-600">
                                  {event.time} • {event.duration}min
                                </p>
                              </div>
                              <button
                                onClick={() => handleDeleteEvent(event.id)}
                                className="text-red-500 hover:text-red-700 font-bold text-lg"
                              >
                                ×
                              </button>
                            </div>
                          </div>
                        ))}
                      {events.filter((e) => e.day === day).length === 0 && (
                        <p className="text-gray-400 text-sm italic">No events planned</p>
                      )}
                    </div>
                  </div>
                ))}
              </div>

              {/* Summary */}
              {events.length > 0 && (
                <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <p className="text-sm text-gray-700">
                    <span className="font-bold">📊 Weekly Summary:</span> {events.length} study
                    sessions planned •{' '}
                    {Math.round(events.reduce((sum, e) => sum + e.duration, 0) / 60 * 10) / 10}
                    h total
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
