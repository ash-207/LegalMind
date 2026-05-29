import api from "./axios";

export const uploadPdf = async (file) => {

    const formData = new FormData();

    formData.append("file", file);

    const response = await api.post(
        "/documents/upload",
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

export const getDocuments = async () => {

    const response = await api.get(
        "/documents/my-documents"
    );

    return response.data;
};