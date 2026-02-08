// Study session manager utility
export interface StudySession {
  id: string;
  subject: string;
  duration: number; // minutes
  timeSpent: number; // minutes
  goal?: string;
  completedAt: string;
  completed: boolean;
}

export interface StudyStats {
  totalSessions: number;
  totalStudyTime: number; // minutes
  currentStreak: number;
  completedTasks: number;
  lastSessionDate?: string;
}

const SESSIONS_KEY = 'studyWise_sessions';
const STATS_KEY = 'studyWise_stats';

export const studySessionManager = {
  // Save a completed session
  saveSession(session: StudySession): void {
    const sessions = this.getAllSessions();
    sessions.push({
      ...session,
      id: Date.now().toString(),
      completedAt: new Date().toISOString(),
    });
    localStorage.setItem(SESSIONS_KEY, JSON.stringify(sessions));
    this.updateStats(session);
  },

  // Get all sessions
  getAllSessions(): StudySession[] {
    try {
      const data = localStorage.getItem(SESSIONS_KEY);
      return data ? JSON.parse(data) : [];
    } catch {
      return [];
    }
  },

  // Get stats
  getStats(): StudyStats {
    try {
      const data = localStorage.getItem(STATS_KEY);
      if (data) return JSON.parse(data);
    } catch {
      // Fall through to default
    }

    return {
      totalSessions: 0,
      totalStudyTime: 0,
      currentStreak: 0,
      completedTasks: 0,
    };
  },

  // Update stats based on completed session
  updateStats(session: StudySession): void {
    const stats = this.getStats();
    stats.totalSessions += 1;
    stats.totalStudyTime += session.timeSpent;
    stats.completedTasks += 1;
    stats.lastSessionDate = session.completedAt;

    // Calculate streak
    const today = new Date().toDateString();
    const lastSessionDate = stats.lastSessionDate
      ? new Date(stats.lastSessionDate).toDateString()
      : null;

    if (lastSessionDate === today) {
      // Same day, keep streak
      stats.currentStreak = stats.currentStreak || 1;
    } else if (
      lastSessionDate &&
      new Date(lastSessionDate).getTime() === new Date(today).getTime() - 86400000
    ) {
      // Yesterday, increment streak
      stats.currentStreak = (stats.currentStreak || 0) + 1;
    } else {
      // Reset streak
      stats.currentStreak = 1;
    }

    localStorage.setItem(STATS_KEY, JSON.stringify(stats));
  },

  // Clear all data (for testing)
  clearAll(): void {
    localStorage.removeItem(SESSIONS_KEY);
    localStorage.removeItem(STATS_KEY);
  },
};
