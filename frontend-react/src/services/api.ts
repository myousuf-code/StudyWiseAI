import axios, { AxiosInstance, AxiosError } from 'axios';
import type {
  AuthResponse,
  LoginRequest,
  RegisterRequest,
  User,
  StudyPlan,
  CreateStudyPlanRequest,
  ProgressStats,
  ChatRequest,
} from '../types/index';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor to include auth token
    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('authToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Add response interceptor for error handling
    this.api.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          // Unauthorized - clear token and redirect to login
          localStorage.removeItem('authToken');
          localStorage.removeItem('user');
          window.location.href = '/';
        }
        return Promise.reject(error);
      }
    );
  }

  // Authentication
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response = await this.api.post<AuthResponse>('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  }

  async register(data: RegisterRequest): Promise<User> {
    const response = await this.api.post<User>('/auth/register', data);
    return response.data;
  }

  async getCurrentUser(): Promise<User> {
    const response = await this.api.get<User>('/auth/me');
    return response.data;
  }

  // Study Plans
  async getStudyPlans(): Promise<StudyPlan[]> {
    const response = await this.api.get<StudyPlan[]>('/study-plans/');
    return response.data;
  }

  async createStudyPlan(data: CreateStudyPlanRequest): Promise<StudyPlan> {
    const response = await this.api.post<StudyPlan>('/study-plans/', data);
    return response.data;
  }

  async deleteStudyPlan(id: number): Promise<void> {
    await this.api.delete(`/study-plans/${id}`);
  }

  // Progress
  async getProgressSummary(): Promise<ProgressStats> {
    const response = await this.api.get<ProgressStats>('/progress/summary');
    return response.data;
  }

  // AI Assistant
  async sendChatMessage(data: ChatRequest): Promise<{ response: string }> {
    const response = await this.api.post<{ response: string }>('/ai/chat', data);
    return response.data;
  }

  // Study Sessions
  async startStudySession(data: {
    title: string;
    subject: string;
    planned_duration: number;
  }) {
    const response = await this.api.post('/study-plans/sessions', data);
    return response.data;
  }

  async completeSession(sessionId: number) {
    const response = await this.api.post(`/study-plans/sessions/${sessionId}/complete`);
    return response.data;
  }
}

export const apiService = new ApiService();
