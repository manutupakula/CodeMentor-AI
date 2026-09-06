import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Attach JWT token to requests if present
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('codementor_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => Promise.reject(error));

// Handle 401 Unauthorized globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Don't auto redirect on login/register endpoints
      const url = error.config.url;
      if (!url.includes('/auth/login') && !url.includes('/auth/register')) {
        localStorage.removeItem('codementor_token');
        localStorage.removeItem('codementor_user');
        if (window.location.pathname !== '/login') {
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (data) => api.post('/api/auth/register', data),
  login: (data) => api.post('/api/auth/login', data),
  getMe: () => api.get('/api/auth/me'),
};

export const profileAPI = {
  getProfile: () => api.get('/api/profile'),
  updateProfile: (data) => api.put('/api/profile', data),
};

export const assessmentAPI = {
  start: () => api.post('/api/assessment/start'),
  submit: (answers) => api.post('/api/assessment/submit', { answers }),
  getLatest: () => api.get('/api/assessment/latest'),
};

export const problemsAPI = {
  list: (params) => api.get('/api/problems', { params }),
  getById: (id) => api.get(`/api/problems/${id}`),
};

export const sessionsAPI = {
  create: (problemId) => api.post('/sessions', { problem_id: problemId }),
  get: (sessionId) => api.get(`/sessions/${sessionId}`),
  submitAttempt: (sessionId, code, language = 'python') => 
    api.post(`/sessions/${sessionId}/attempt`, { code, language }),
  requestHint: (sessionId, requestedLevel = null) => 
    api.post(`/sessions/${sessionId}/hint`, { requested_level: requestedLevel }),
  getSolution: (sessionId) => api.get(`/sessions/${sessionId}/solution`),
};

export const tutorAPI = {
  chat: (data) => api.post('/tutor/chat', data),
  customProblem: (data) => api.post('/tutor/custom-problem', data),
};

export const learnerAPI = {
  getProfile: () => api.get('/api/learner/profile'),
  getWeakTopics: () => api.get('/api/learner/weak-topics'),
  getRecommendations: (limit = 5) =>
    api.get('/api/learner/recommendations', { params: { limit } }),
  getReviseMistakes: () => api.get('/api/learner/revise-mistakes'),
  getHistory: (limit = 20) =>
    api.get('/api/learner/history', { params: { limit } }),
};

export default api;
