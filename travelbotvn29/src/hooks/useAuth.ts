import { useCallback, useEffect } from 'react';
import { useAuthStore } from '@/store/authStore';
import { AuthUser } from '@/types';

interface LoginCredentials {
  email: string;
  password: string;
}

const ADMIN_ACCOUNT = {
  email: 'admin@example.com',
  password: 'password123',
};

const ADMIN_USER: AuthUser = {
  id: 'admin-001',
  email: 'admin@example.com',
  name: 'Admin',
  role: 'admin',
  created_at: new Date().toISOString(),
};

const ADMIN_TOKEN = 'admin-token-12345';

export const useAuth = () => {
  const {
    user,
    token,
    isAuthenticated,
    isLoading,
    error,
    setUser,
    setLoading,
    setError,
    logout: storeLogout,
    login: storeLogin,
    initializeFromStorage,
  } = useAuthStore();

  useEffect(() => {
    initializeFromStorage();
  }, [initializeFromStorage]);

  const login = useCallback(
    async (credentials: LoginCredentials) => {
      try {
        setLoading(true);
        setError(null);

        if (
          credentials.email === ADMIN_ACCOUNT.email &&
          credentials.password === ADMIN_ACCOUNT.password
        ) {
          storeLogin(ADMIN_USER, ADMIN_TOKEN);
          return true;
        } else {
          setError('Invalid email or password');
          return false;
        }
      } catch (error) {
        const errorMessage =
          error instanceof Error ? error.message : 'Login failed. Please try again.';
        setError(errorMessage);
        return false;
      } finally {
        setLoading(false);
      }
    },
    [setLoading, setError, storeLogin]
  );

  const logout = useCallback(() => {
    storeLogout();
  }, [storeLogout]);

  const updateUser = useCallback(
    (authUser: AuthUser) => {
      setUser(authUser);
    },
    [setUser]
  );

  return {
    user,
    token,
    isAuthenticated,
    isLoading,
    error,
    login,
    logout,
    updateUser,
  };
};
