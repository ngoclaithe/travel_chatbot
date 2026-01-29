import { create } from 'zustand';
import { ChatMessage } from '@/types';

interface ChatStore {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  
  addMessage: (message: ChatMessage) => void;
  clearMessages: () => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  updateMessage: (id: string, updates: Partial<ChatMessage>) => void;
}

export const useChatStore = create<ChatStore>((set) => ({
  messages: [],
  isLoading: false,
  error: null,

  addMessage: (message: ChatMessage) =>
    set((state) => ({
      messages: [...state.messages, message],
    })),

  clearMessages: () =>
    set({
      messages: [],
      error: null,
    }),

  setLoading: (loading: boolean) =>
    set({
      isLoading: loading,
    }),

  setError: (error: string | null) =>
    set({
      error,
    }),

  updateMessage: (id: string, updates: Partial<ChatMessage>) =>
    set((state) => ({
      messages: state.messages.map((msg) =>
        msg.id === id ? { ...msg, ...updates } : msg
      ),
    })),
}));
