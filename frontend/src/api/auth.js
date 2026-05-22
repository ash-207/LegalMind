export const signup = async (formData) => {

  const users =
    JSON.parse(localStorage.getItem("users")) || [];

  const existingUser = users.find(
    user => user.email === formData.email
  );

  if (existingUser) {
    throw {
      response: {
        data: {
          message: "User already exists"
        }
      }
    };
  }

  users.push(formData);

  localStorage.setItem(
    "users",
    JSON.stringify(users)
  );

  return {
    data: {
      token: "fake-token",
      email: formData.email
    }
  };
};


export const login = async (formData) => {

  const users =
    JSON.parse(localStorage.getItem("users")) || [];

  const user = users.find(
    u =>
      u.email === formData.email &&
      u.password === formData.password
  );

  if (!user) {
    throw {
      response: {
        data: {
          message: "Invalid credentials"
        }
      }
    };
  }

  return {
    data: {
      token: "fake-token",
      email: user.email
    }
  };
};