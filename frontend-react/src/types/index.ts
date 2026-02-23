// User Types
export interface User {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  is_active: boolean;
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

// Progress Types
export interface ProgressStats {
  total_sessions: number;
  total_time: number;
  sessions_by_subject: Record<string, number>;
  weekly_progress: number[];
}

// Chat Types
export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface ChatRequest {
  message: string;
  context?: string;
}

// Notification Types
export type NotificationType = 'success' | 'error' | 'info' | 'warning';

export interface Notification {
  id: string;
  type: NotificationType;
  message: string;
}
