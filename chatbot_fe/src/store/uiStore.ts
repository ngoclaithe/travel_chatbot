import { create } from 'zustand';

interface UIStore {
  isChatOpen: boolean;
  isModalOpen: boolean;
  modalTitle: string;
  modalContent: React.ReactNode | null;
  isLoading: boolean;
  notification: {
    show: boolean;
    message: string;
    type: 'success' | 'error' | 'info' | 'warning';
  };

  toggleChat: () => void;
  openChat: () => void;
  closeChat: () => void;
  openModal: (title: string, content: React.ReactNode) => void;
  closeModal: () => void;
  setLoading: (loading: boolean) => void;
  showNotification: (message: string, type: 'success' | 'error' | 'info' | 'warning') => void;
  hideNotification: () => void;
}

export const useUIStore = create<UIStore>((set) => ({
  isChatOpen: false,
  isModalOpen: false,
  modalTitle: '',
  modalContent: null,
  isLoading: false,
  notification: {
    show: false,
    message: '',
    type: 'info',
  },

  toggleChat: () =>
    set((state) => ({
      isChatOpen: !state.isChatOpen,
    })),

  openChat: () =>
    set({
      isChatOpen: true,
    }),

  closeChat: () =>
    set({
      isChatOpen: false,
    }),

  openModal: (title: string, content: React.ReactNode) =>
    set({
      isModalOpen: true,
      modalTitle: title,
      modalContent: content,
    }),

  closeModal: () =>
    set({
      isModalOpen: false,
      modalTitle: '',
      modalContent: null,
    }),

  setLoading: (loading: boolean) =>
    set({
      isLoading: loading,
    }),

  showNotification: (message: string, type: 'success' | 'error' | 'info' | 'warning') =>
    set({
      notification: {
        show: true,
        message,
        type,
      },
    }),

  hideNotification: () =>
    set({
      notification: {
        show: false,
        message: '',
        type: 'info',
      },
    }),
}));
