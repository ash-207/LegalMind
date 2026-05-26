import api from "./axios";

export const uploadAudio = async (file) => {

    const formData = new FormData();

    formData.append("file", file);

    const response = await api.post(
        "/Transcription/upload",
        formData,
        {
            headers: {
                "Content-Type":
                    "multipart/form-data",
            },
        }
    );

    return response.data;
};