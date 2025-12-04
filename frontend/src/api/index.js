import request from './request'

// 认证API
export const authAPI = {
  login: (data) => request.post('/auth/login', data),
  getMe: () => request.get('/auth/me'),
  logout: () => request.post('/auth/logout'),
  changePassword: (data) => request.post('/auth/change-password', data)
}

// 用户API
export const userAPI = {
  list: (params) => request.get('/users/', { params }),
  get: (id) => request.get(`/users/${id}`),
  create: (data) => request.post('/users/', data),
  update: (id, data) => request.put(`/users/${id}`, data),
  delete: (id) => request.delete(`/users/${id}`)
}

// 组织API
export const organizationAPI = {
  list: (params) => request.get('/organizations/', { params }),
  get: (id) => request.get(`/organizations/${id}`),
  create: (data) => request.post('/organizations/', data),
  update: (id, data) => request.put(`/organizations/${id}`, data),
  delete: (id) => request.delete(`/organizations/${id}`)
}

// 奖项API
export const awardAPI = {
  list: (params) => request.get('/awards/', { params }),
  get: (id) => request.get(`/awards/${id}`),
  create: (data) => request.post('/awards/', data),
  update: (id, data) => request.put(`/awards/${id}`, data),
  listCycles: (params) => request.get('/awards/cycles/', { params }),
  createCycle: (data) => request.post('/awards/cycles/', data)
}

// 申报API
export const applicationAPI = {
  list: (params) => request.get('/applications/', { params }),
  get: (id) => request.get(`/applications/${id}`),
  create: (data) => request.post('/applications/', data),
  update: (id, data) => request.put(`/applications/${id}`, data),
  submit: (id) => request.post(`/applications/${id}/submit`),
  updateStatus: (id, data) => request.put(`/applications/${id}/status`, data),
  uploadAttachment: (id, formData) => request.post(`/applications/${id}/attachments`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  getAttachments: (id) => request.get(`/applications/${id}/attachments`),
  delete: (id) => request.delete(`/applications/${id}`)
}

// 评审API
export const reviewAPI = {
  myReviews: (params) => request.get('/reviews/my-reviews', { params }),
  getByApplication: (appId) => request.get(`/reviews/application/${appId}`),
  create: (data) => request.post('/reviews/', data),
  update: (id, data) => request.put(`/reviews/${id}`, data),
  submit: (id) => request.post(`/reviews/${id}/submit`),
  assign: (data) => request.post('/reviews/assign', data),
  getScoreSummary: (appId) => request.get(`/reviews/score-summary/${appId}`)
}

// 评审委员会API
export const committeeAPI = {
  listDecisions: (params) => request.get('/committee/decisions', { params }),
  getDecision: (id) => request.get(`/committee/decisions/${id}`),
  createDecision: (data) => request.post('/committee/decisions', data),
  updateDecision: (id, data) => request.put(`/committee/decisions/${id}`, data),
  deleteDecision: (id) => request.delete(`/committee/decisions/${id}`),
  getApplicationDecisions: (appId) => request.get(`/committee/decisions/application/${appId}`)
}

// 公示API
export const announcementAPI = {
  list: (params) => request.get('/announcements/', { params }),
  get: (id) => request.get(`/announcements/${id}`),
  create: (data) => request.post('/announcements/', data),
  update: (id, data) => request.put(`/announcements/${id}`, data),
  createObjection: (id, data) => request.post(`/announcements/${id}/objections`, data),
  listObjections: (id) => request.get(`/announcements/${id}/objections`)
}

// 统计API
export const statisticsAPI = {
  overview: () => request.get('/statistics/overview'),
  byStatus: () => request.get('/statistics/applications-by-status'),
  byYear: () => request.get('/statistics/applications-by-year'),
  exportApplications: () => request.get('/statistics/export/applications', { responseType: 'blob' }),
  exportStatistics: () => request.get('/statistics/export/statistics', { responseType: 'blob' })
}

// 文件API
export const fileAPI = {
  upload: (formData) => request.post('/files/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  download: (filePath) => request.get(`/files/download/${filePath}`, { responseType: 'blob' }),
  downloadTemplate: () => request.get('/files/template/application', { responseType: 'blob' })
}
