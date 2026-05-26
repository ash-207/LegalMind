import api from "./axios";

export const signup = async (data) => {

    const response = await api.post(
        "/auth/signup",
        data
    );

    return response.data;
};

export const login = async (data) => {

    const response = await api.post(
        "/auth/login",
        data
    );

    return response.data;
};