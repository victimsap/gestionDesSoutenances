import { Profile, Project, Report, Defense, DefenseJuryMember, Evaluation, UserRole } from './supabase';

// =====================================================
// CONFIGURATION
// =====================================================

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// =====================================================
// TYPES
// =====================================================

export interface ApiResponse<T> {
  data: T | null;
  error: Error | null;
  status?: number;
}

export interface ApiListResponse<T> {
  data: T[];
  error: Error | null;
  status?: number;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface AuthUser {
  id: string;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  role: UserRole;
}

// =====================================================
// HELPER FUNCTIONS
// =====================================================

async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<{ data: T | null; error: Error | null; status: number }> {
  try {
    const token = localStorage.getItem('authToken');
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    };

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers,
      ...options,
    });

    const json = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw new Error(json.error || json.detail || `HTTP ${response.status}`);
    }

    return { data: json.data || json, error: null, status: response.status };
  } catch (error) {
    return { data: null, error: error as Error, status: 500 };
  }
}

// =====================================================
// AUTHENTICATION API
// =====================================================

export const authApi = {
  async signUp(
    email: string,
    password: string,
    username: string,
    firstName: string,
    lastName: string,
    role: UserRole
  ): Promise<ApiResponse<AuthUser>> {
    const response = await apiRequest<{ user: AuthUser; tokens: AuthTokens }>('/api/auth/register/', {
      method: 'POST',
      body: JSON.stringify({
        email,
        password,
        username,
        first_name: firstName,
        last_name: lastName,
        role,
      }),
    });

    if (response.data?.tokens) {
      localStorage.setItem('authToken', response.data.tokens.access);
      localStorage.setItem('refreshToken', response.data.tokens.refresh);
      if (response.data.user?.id) {
        localStorage.setItem('userId', response.data.user.id);
        localStorage.setItem('userRole', response.data.user.role);
      }
    }

    return {
      data: response.data?.user || null,
      error: response.error,
      status: response.status,
    };
  },

  async signIn(email: string, password: string): Promise<ApiResponse<AuthUser>> {
    const response = await apiRequest<{ user: AuthUser; tokens: AuthTokens }>('/api/auth/login/', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });

    if (response.data?.tokens) {
      localStorage.setItem('authToken', response.data.tokens.access);
      localStorage.setItem('refreshToken', response.data.tokens.refresh);
      if (response.data.user?.id) {
        localStorage.setItem('userId', response.data.user.id);
        localStorage.setItem('userRole', response.data.user.role);
      }
    }

    return {
      data: response.data?.user || null,
      error: response.error,
      status: response.status,
    };
  },

  async signOut(): Promise<ApiResponse<null>> {
    const response = await apiRequest('/api/auth/logout/', {
      method: 'POST',
    });

    localStorage.removeItem('authToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('userId');
    localStorage.removeItem('userRole');

    return response;
  },

  async getSession(): Promise<ApiResponse<AuthUser | null>> {
    const token = localStorage.getItem('authToken');

    if (!token) {
      return { data: null, error: null, status: 200 };
    }

    const response = await apiRequest<AuthUser>('/api/auth/me/', {
      method: 'GET',
    });

    if (response.data) {
      return {
        data: response.data,
        error: null,
        status: response.status,
      };
    }

    return { data: null, error: response.error, status: response.status };
  },

  async refreshToken(): Promise<ApiResponse<AuthTokens>> {
    const refreshToken = localStorage.getItem('refreshToken');

    if (!refreshToken) {
      return { data: null, error: new Error('No refresh token found'), status: 401 };
    }

    const response = await apiRequest<AuthTokens>('/api/auth/refresh/', {
      method: 'POST',
      body: JSON.stringify({ refresh: refreshToken }),
    });

    if (response.data) {
      localStorage.setItem('authToken', response.data.access);
    }

    return response;
  },
};

// =====================================================
// USERS API
// =====================================================

export const usersApi = {
  async getUser(userId: string): Promise<ApiResponse<AuthUser>> {
    return apiRequest(`/api/users/${userId}/`, {
      method: 'GET',
    });
  },

  async updateUser(userId: string, updates: Partial<AuthUser>): Promise<ApiResponse<AuthUser>> {
    return apiRequest(`/api/users/${userId}/`, {
      method: 'PATCH',
      body: JSON.stringify(updates),
    });
  },

  async getAllUsers(role?: UserRole): Promise<ApiListResponse<AuthUser>> {
    const queryParams = role ? `?role=${role}` : '';
    return apiRequest(`/api/users/${queryParams}`, {
      method: 'GET',
    });
  },

  async getEncadreurs(): Promise<ApiListResponse<AuthUser>> {
    return apiRequest('/api/users/?role=encadreur', {
      method: 'GET',
    });
  },

  async getEtudiants(): Promise<ApiListResponse<AuthUser>> {
    return apiRequest('/api/users/?role=etudiant', {
      method: 'GET',
    });
  },

  async getJury(): Promise<ApiListResponse<AuthUser>> {
    return apiRequest('/api/users/?role=jury', {
      method: 'GET',
    });
  },
};

// =====================================================
// PROJECTS API (SUJETS)
// =====================================================

export const projectsApi = {
  async getProject(projectId: string): Promise<ApiResponse<Project>> {
    return apiRequest(`/soutenances/sujets/${projectId}/`, {
      method: 'GET',
    });
  },

  async createProject(project: Omit<Project, 'id' | 'created_at' | 'updated_at'>): Promise<ApiResponse<Project>> {
    return apiRequest('/soutenances/sujets/', {
      method: 'POST',
      body: JSON.stringify(project),
    });
  },

  async updateProject(projectId: string, updates: Partial<Project>): Promise<ApiResponse<Project>> {
    return apiRequest(`/soutenances/sujets/${projectId}/`, {
      method: 'PATCH',
      body: JSON.stringify(updates),
    });
  },

  async deleteProject(projectId: string): Promise<ApiResponse<null>> {
    return apiRequest(`/soutenances/sujets/${projectId}/`, {
      method: 'DELETE',
    });
  },

  async getStudentProjects(studentId: string): Promise<ApiListResponse<Project>> {
    return apiRequest(`/soutenances/sujets/?etudiant=${studentId}`, {
      method: 'GET',
    });
  },

  async getEncadreurProjects(encadreurId: string): Promise<ApiListResponse<Project>> {
    return apiRequest(`/soutenances/sujets/?encadreur=${encadreurId}`, {
      method: 'GET',
    });
  },

  async getAllProjects(): Promise<ApiListResponse<Project>> {
    return apiRequest('/soutenances/sujets/', {
      method: 'GET',
    });
  },

  async assignEncadreur(projectId: string, encadreurId: string): Promise<ApiResponse<Project>> {
    return apiRequest(`/soutenances/sujets/${projectId}/`, {
      method: 'PATCH',
      body: JSON.stringify({ encadreur_id: encadreurId }),
    });
  },
};

// =====================================================
// REPORTS API (RAPPORTS)
// =====================================================

export const reportsApi = {
  async getReport(reportId: string): Promise<ApiResponse<Report>> {
    return apiRequest(`/rapports/${reportId}/`, {
      method: 'GET',
    });
  },

  async uploadReport(
    sujetId: string,
    file: File,
    soutenanceId?: string
  ): Promise<ApiResponse<Report>> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('sujet', sujetId);
    if (soutenanceId) {
      formData.append('soutenance', soutenanceId);
    }

    const token = localStorage.getItem('authToken');
    const headers: HeadersInit = {
      ...(token && { Authorization: `Bearer ${token}` }),
    };

    try {
      const response = await fetch(`${API_BASE_URL}/rapports/`, {
        method: 'POST',
        headers,
        body: formData,
      });

      const json = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(json.error || json.detail || `HTTP ${response.status}`);
      }

      return { data: json.data || json, error: null, status: response.status };
    } catch (error) {
      return { data: null, error: error as Error, status: 500 };
    }
  },

  async getSujetReports(sujetId: string): Promise<ApiListResponse<Report>> {
    return apiRequest(`/rapports/?sujet=${sujetId}`, {
      method: 'GET',
    });
  },

  async getSoutenanceReport(soutenanceId: string): Promise<ApiResponse<Report>> {
    return apiRequest(`/rapports/?soutenance=${soutenanceId}`, {
      method: 'GET',
    });
  },

  async deleteReport(reportId: string): Promise<ApiResponse<null>> {
    return apiRequest(`/rapports/${reportId}/`, {
      method: 'DELETE',
    });
  },

  async updateReport(reportId: string, updates: Partial<Report>): Promise<ApiResponse<Report>> {
    return apiRequest(`/rapports/${reportId}/`, {
      method: 'PATCH',
      body: JSON.stringify(updates),
    });
  },
};

// =====================================================
// DEFENSES API (SOUTENANCES)
// =====================================================

export const defensesApi = {
  async getDefense(defenseId: string): Promise<ApiResponse<Defense>> {
    return apiRequest(`/soutenances/soutenances/${defenseId}/`, {
      method: 'GET',
    });
  },

  async createDefense(defense: Omit<Defense, 'id' | 'created_at' | 'updated_at'>): Promise<ApiResponse<Defense>> {
    return apiRequest('/soutenances/soutenances/', {
      method: 'POST',
      body: JSON.stringify(defense),
    });
  },

  async updateDefense(defenseId: string, updates: Partial<Defense>): Promise<ApiResponse<Defense>> {
    return apiRequest(`/soutenances/soutenances/${defenseId}/`, {
      method: 'PATCH',
      body: JSON.stringify(updates),
    });
  },

  async deleteDefense(defenseId: string): Promise<ApiResponse<null>> {
    return apiRequest(`/soutenances/soutenances/${defenseId}/`, {
      method: 'DELETE',
    });
  },

  async getProjectDefense(sujetId: string): Promise<ApiResponse<Defense>> {
    return apiRequest(`/soutenances/soutenances/?sujet=${sujetId}`, {
      method: 'GET',
    });
  },

  async getAllDefenses(): Promise<ApiListResponse<Defense>> {
    return apiRequest('/soutenances/soutenances/', {
      method: 'GET',
    });
  },

  async getUpcomingDefenses(): Promise<ApiListResponse<Defense>> {
    return apiRequest('/soutenances/soutenances/?status=scheduled', {
      method: 'GET',
    });
  },

  async getCompletedDefenses(): Promise<ApiListResponse<Defense>> {
    return apiRequest('/soutenances/soutenances/?status=completed', {
      method: 'GET',
    });
  },
};

// =====================================================
// EVALUATIONS API
// =====================================================

export const evaluationsApi = {
  async submitEvaluation(
    evaluation: Omit<Evaluation, 'id' | 'created_at' | 'updated_at'>
  ): Promise<ApiResponse<Evaluation>> {
    return apiRequest('/evaluations/', {
      method: 'POST',
      body: JSON.stringify(evaluation),
    });
  },

  async getDefenseEvaluations(soutenanceId: string): Promise<ApiListResponse<Evaluation>> {
    return apiRequest(`/evaluations/?soutenance=${soutenanceId}`, {
      method: 'GET',
    });
  },

  async getJuryEvaluation(soutenanceId: string, juryId: string): Promise<ApiResponse<Evaluation>> {
    return apiRequest(`/evaluations/?soutenance=${soutenanceId}&jury=${juryId}`, {
      method: 'GET',
    });
  },

  async updateEvaluation(
    evaluationId: string,
    updates: Partial<Evaluation>
  ): Promise<ApiResponse<Evaluation>> {
    return apiRequest(`/evaluations/${evaluationId}/`, {
      method: 'PATCH',
      body: JSON.stringify(updates),
    });
  },

  async deleteEvaluation(evaluationId: string): Promise<ApiResponse<null>> {
    return apiRequest(`/evaluations/${evaluationId}/`, {
      method: 'DELETE',
    });
  },

  async getDefenseAverage(soutenanceId: string): Promise<ApiResponse<{ average: number; count: number }>> {
    return apiRequest(`/evaluations/?soutenance=${soutenanceId}&average=true`, {
      method: 'GET',
    });
  },

  async getUserEvaluations(userId: string): Promise<ApiListResponse<Evaluation>> {
    return apiRequest(`/evaluations/?jury=${userId}`, {
      method: 'GET',
    });
  },
};

// =====================================================
// NOTIFICATIONS API
// =====================================================

export const notificationsApi = {
  async getNotifications(): Promise<ApiListResponse<any>> {
    return apiRequest('/notifications/', {
      method: 'GET',
    });
  },

  async getUserNotifications(userId: string): Promise<ApiListResponse<any>> {
    return apiRequest(`/notifications/?user=${userId}`, {
      method: 'GET',
    });
  },

  async markAsRead(notificationId: string): Promise<ApiResponse<any>> {
    return apiRequest(`/notifications/${notificationId}/`, {
      method: 'PATCH',
      body: JSON.stringify({ is_read: true }),
    });
  },

  async markAllAsRead(): Promise<ApiResponse<null>> {
    return apiRequest('/notifications/mark_all_as_read/', {
      method: 'POST',
    });
  },

  async deleteNotification(notificationId: string): Promise<ApiResponse<null>> {
    return apiRequest(`/notifications/${notificationId}/`, {
      method: 'DELETE',
    });
  },
};

// =====================================================
// DASHBOARD API
// =====================================================

export const dashboardApi = {
  async getStats(): Promise<ApiResponse<{
    total_users: number;
    users_by_role: Array<{ role: string; total: number }>;
    total_soutenances: number;
    total_sujets: number;
    total_rapports: number;
    total_evaluations: number;
    moyenne_notes: number;
    soutenances_par_statut: Array<{ status: string; total: number }>;
  }>> {
    return apiRequest('/dashboard/stats/', {
      method: 'GET',
    });
  },
};

// =====================================================
// ERROR HANDLING & UTILITIES
// =====================================================

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
    public details?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export function isApiError(error: unknown): error is ApiError {
  return error instanceof ApiError;
}

// =====================================================
// EXPORT CLIENT
// =====================================================

export const apiClient = {
  auth: authApi,
  users: usersApi,
  projects: projectsApi,
  reports: reportsApi,
  defenses: defensesApi,
  evaluations: evaluationsApi,
  notifications: notificationsApi,
  dashboard: dashboardApi,
};

export default apiClient;
