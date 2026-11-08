// User Types
export interface User {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  full_name?: string;
}

export interface RegisterResponse {
  message: string;
  email: string;
  verification_required: boolean;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// Study Plan Types
export interface StudyPlanMaterials {
  subjects?: string[];
  skills?: string[];
  resources?: string[];
  career_source?: { session_id: number; target_profession: string; generated_from: string };
}

export interface StudyPlanSchedule {
  weekly_tasks?: { task: string; subject: string; duration: string; priority: string; timeline: string }[];
  daily_activities?: { activity: string; duration: string; type: string }[];
}

export interface StudyPlanMilestones {
  short_term?: string[];
  medium_term?: string[];
  long_term?: string[];
}

export interface StudyPlan {
  id: number;
  user_id: number;
  title: string;
  subject: string;
  difficulty_level: 'beginner' | 'intermediate' | 'advanced';
  estimated_duration: number;
  description?: string;
  created_at: string;
  study_materials?: StudyPlanMaterials;
  schedule?: StudyPlanSchedule;
  milestones?: StudyPlanMilestones;
}

export interface CreateStudyPlanRequest {
  title: string;
  subject: string;
  difficulty_level: 'beginner' | 'intermediate' | 'advanced';
  estimated_duration: number;
  description?: string;
  study_materials?: Record<string, unknown>;
  schedule?: Record<string, unknown>;
  milestones?: Record<string, unknown>;
}

// Study Session Types
export interface StudySession {
  id: number;
  user_id: number;
  study_plan_id?: number;
  title: string;
  subject: string;
  planned_duration: number;
  actual_duration?: number;
  start_time: string;
  end_time?: string;
  notes?: string;
  completed: boolean;
}

// Progress Types — matches backend ProgressSummary response
export interface ProgressStats {
  total_study_time: number;      // minutes
  total_sessions: number;
  subjects_studied: string[];
  average_accuracy: number;
  current_streak: number;        // days
  weekly_progress: Array<{
    week_start: string;
    time_spent: number;
    sessions: number;
    subjects_count: number;
  }>;
  learning_trends: {
    most_studied_subjects?: Array<[string, number]>;
    study_consistency?: number;
    average_session_length?: number;
    total_subjects?: number;
  };
}

// Chat Types
export interface ChatMessage {
  id?: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface ChatRequest {
  message: string;
  context?: Record<string, unknown>;  // matches backend Optional[Dict]
}

// Notification Types
export type NotificationType = 'success' | 'error' | 'info' | 'warning';

export interface Notification {
  id: string;
  type: NotificationType;
  message: string;
}
