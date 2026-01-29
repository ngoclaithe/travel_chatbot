import { useCallback, useState } from 'react';
import axiosClient from '@/lib/axiosClient';
import { ApiResponse } from '@/types';

interface UseCRUDOptions<T> {
  endpoint: string;
  onSuccess?: (data: T | T[]) => void;
  onError?: (error: Error) => void;
}

interface UseCRUDReturn<T> {
  data: T[];
  isLoading: boolean;
  error: string | null;
  fetchData: () => Promise<void>;
  createItem: (item: Omit<T, 'id'>) => Promise<T | null>;
  updateItem: (id: string, item: Partial<T>) => Promise<T | null>;
  deleteItem: (id: string) => Promise<boolean>;
  setData: (data: T[]) => void;
  clearError: () => void;
}

function isApiResponse<U>(obj: unknown): obj is ApiResponse<U> {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'data' in obj
  );
}

export const useAdminCRUD = <T extends { id: string }>(
  options: UseCRUDOptions<T>
): UseCRUDReturn<T> => {
  const [data, setData] = useState<T[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { endpoint, onSuccess, onError } = options;

  const fetchData = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await axiosClient.get<T[] | ApiResponse<T[]>>(
        `/${endpoint}/`
      );

      const dataArray = isApiResponse<T[]>(response.data)
        ? response.data.data ?? []
        : response.data;

      setData(dataArray);
      onSuccess?.(dataArray);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch data';
      setError(errorMessage);
      onError?.(err instanceof Error ? err : new Error(errorMessage));
    } finally {
      setIsLoading(false);
    }
  }, [endpoint, onSuccess, onError]);

  const createItem = useCallback(
    async (item: Omit<T, 'id'>): Promise<T | null> => {
      try {
        setError(null);
        setIsLoading(true);

        const response = await axiosClient.post<T | ApiResponse<T>>(
          `/${endpoint}/`,
          item
        );

        const newItem = isApiResponse<T>(response.data)
          ? response.data.data
          : response.data;

        if (newItem && newItem.id) {
          setData((prev) => [...prev, newItem]);
          onSuccess?.(newItem);
          return newItem;
        }
        return null;
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Failed to create item';
        setError(errorMessage);
        onError?.(err instanceof Error ? err : new Error(errorMessage));
        return null;
      } finally {
        setIsLoading(false);
      }
    },
    [endpoint, onSuccess, onError]
  );

  const updateItem = useCallback(
    async (id: string, item: Partial<T>): Promise<T | null> => {
      try {
        setError(null);
        setIsLoading(true);

        const response = await axiosClient.put<T | ApiResponse<T>>(
          `/${endpoint}/${id}/`,
          item
        );

        const updatedItem = isApiResponse<T>(response.data)
          ? response.data.data
          : response.data;

        if (updatedItem && updatedItem.id) {
          setData((prev) =>
            prev.map((existing) =>
              existing.id === id ? updatedItem : existing
            )
          );
          onSuccess?.(updatedItem);
          return updatedItem;
        }
        return null;
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Failed to update item';
        setError(errorMessage);
        onError?.(err instanceof Error ? err : new Error(errorMessage));
        return null;
      } finally {
        setIsLoading(false);
      }
    },
    [endpoint, onSuccess, onError]
  );

  const deleteItem = useCallback(
    async (id: string): Promise<boolean> => {
      try {
        setError(null);
        setIsLoading(true);

        await axiosClient.delete(`/${endpoint}/${id}/`);
        setData((prev) => prev.filter((item) => item.id !== id));
        return true;
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Failed to delete item';
        setError(errorMessage);
        onError?.(err instanceof Error ? err : new Error(errorMessage));
        return false;
      } finally {
        setIsLoading(false);
      }
    },
    [endpoint, onError]
  );

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    data,
    isLoading,
    error,
    fetchData,
    createItem,
    updateItem,
    deleteItem,
    setData,
    clearError,
  };
};
