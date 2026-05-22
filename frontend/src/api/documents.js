import api from './client';
export const uploadDocument = (file) => {
  const form = new FormData();
  form.append('file', file);
  return api.post('/documents/upload', form);
};
export const getDocuments = () => api.get('/documents');
export const getDocument = (id) => api.get(`/documents/${id}`);
