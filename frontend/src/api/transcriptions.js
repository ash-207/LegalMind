import api from './client';
export const uploadAudio = (file) => {
  const form = new FormData();
  form.append('file', file);
  return api.post('/api/ai/transcribe', form);
};
export const getTranscriptions = () => api.get('/transcriptions');
export const getTranscription = (id) => api.get(`/transcriptions/${id}`);
