import { useCallback, useEffect, useRef } from 'react';
import { useChatStore } from '@/store/chatStore';
import { ChatMessage } from '@/types';
import axiosClient from '@/lib/axiosClient';

interface WebSocketMessage {
  type: string;
  content?: string;
  data?: unknown;
  intent?: string;
}

export const useChat = () => {
  const addMessage = useChatStore((state) => state.addMessage);
  const setLoading = useChatStore((state) => state.setLoading);
  const setError = useChatStore((state) => state.setError);
  const clearMessages = useChatStore((state) => state.clearMessages);
  
  const messages = useChatStore((state) => state.messages);
  const isLoading = useChatStore((state) => state.isLoading);
  const error = useChatStore((state) => state.error);

  const wsRef = useRef<WebSocket | null>(null);
  const reconnectAttemptsRef = useRef<number>(0);
  const maxReconnectAttemptsRef = useRef<number>(5);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const isConnectingRef = useRef<boolean>(false);
  const isMountedRef = useRef<boolean>(true);
  const botResponseBufferRef = useRef<string>('');
  const botResponseTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const botResponseMetadataRef = useRef<{
    intent?: string;
    data?: unknown;
  }>({}); 

  useEffect(() => {
    isMountedRef.current = true;

    const connectWebSocket = () => {
      if (!isMountedRef.current) return;
      
      if (isConnectingRef.current || wsRef.current?.readyState === WebSocket.OPEN) {
        console.log('⏭️ Skipping connect - already connected or connecting');
        return;
      }

      isConnectingRef.current = true;

      try {
        const baseWsUrl = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000';
        const wsUrl = `${baseWsUrl.replace(/\/$/, '')}/ws/chat`;
        console.log('🔗 Connecting to', wsUrl);

        wsRef.current = new WebSocket(wsUrl);

        wsRef.current.onopen = () => {
          if (!isMountedRef.current) {
            console.log('⚠️ Component unmounted, closing connection');
            wsRef.current?.close();
            return;
          }
          
          console.log('✅ WebSocket connected');
          reconnectAttemptsRef.current = 0;
          isConnectingRef.current = false;
          setError(null);

          wsRef.current?.send(JSON.stringify({ type: 'init' }));
        };

        wsRef.current.onmessage = (event: MessageEvent<string>) => {
          if (!isMountedRef.current) return;

          try {
            const message: WebSocketMessage = JSON.parse(event.data);

            if (message.type === 'ping') {
              wsRef.current?.send(JSON.stringify({ type: 'pong' }));
              return;
            }

            if (message.type === 'init_ack') {
              console.log('✅ Connection acknowledged:', message.content);
              return;
            }

            if (message.type === 'error') {
              setError(message.content || 'An error occurred');
              return;
            }

            if (message.type === 'message') {
              
              botResponseBufferRef.current += (message.content || '');
              if (message.intent) {
                botResponseMetadataRef.current.intent = message.intent;
              }
              if (message.data) {
                botResponseMetadataRef.current.data = message.data;
              }

              if (botResponseTimeoutRef.current) {
                clearTimeout(botResponseTimeoutRef.current);
              }

              botResponseTimeoutRef.current = setTimeout(() => {
                if (botResponseBufferRef.current && isMountedRef.current) {
                  const chatMessage: ChatMessage = {
                    id: Date.now().toString(),
                    sender: 'bot',
                    content: botResponseBufferRef.current,
                    timestamp: new Date().toISOString(),
                    metadata: botResponseMetadataRef.current,
                  };
                  addMessage(chatMessage);
                  botResponseBufferRef.current = '';
                  botResponseMetadataRef.current = {};
                }
              }, 500);
            }
          } catch (error) {
            console.error('Error parsing WebSocket message:', error);
          }
        };

        wsRef.current.onerror = (event) => {
          isConnectingRef.current = false;
          if (reconnectAttemptsRef.current === 0 || reconnectAttemptsRef.current % 5 === 0) {
            console.error('💥 WebSocket error', event);
          }
        };

        wsRef.current.onclose = (event) => {
          isConnectingRef.current = false;
          console.warn('🔻 WebSocket closed', event.code, event.reason);

          if (!isMountedRef.current) {
            console.log('Component unmounted, not reconnecting');
            return;
          }

          if (reconnectAttemptsRef.current < maxReconnectAttemptsRef.current) {
            const backoffDelay = Math.min(
              Math.pow(2, reconnectAttemptsRef.current) * 1000,
              30000
            );

            reconnectAttemptsRef.current += 1;

            if (reconnectAttemptsRef.current === 1) {
              setError('Chat service unavailable. Attempting to reconnect...');
            }

            console.log(`⏳ Reconnecting in ${backoffDelay}ms (attempt ${reconnectAttemptsRef.current})`);
            reconnectTimeoutRef.current = setTimeout(connectWebSocket, backoffDelay);
          } else {
            setError('Chat service unavailable. Please refresh the page or try again later.');
          }
        };
      } catch (error) {
        isConnectingRef.current = false;
        console.error('Failed to initialize WebSocket connection', error);
      }
    };

    connectWebSocket();

    return () => {
      console.log('🧹 Cleaning up WebSocket');
      isMountedRef.current = false;
      isConnectingRef.current = false;

      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
        reconnectTimeoutRef.current = null;
      }

      if (botResponseTimeoutRef.current) {
        clearTimeout(botResponseTimeoutRef.current);
        botResponseTimeoutRef.current = null;
      }

      if (wsRef.current) {
        wsRef.current.close();
        wsRef.current = null;
      }
    };
  }, [addMessage, setError, setLoading]); 

  const sendMessage = useCallback(
    async (content: string) => {
      try {
        setError(null);
        setLoading(true);

        const userMessage: ChatMessage = {
          id: Date.now().toString(),
          sender: 'user',
          content,
          timestamp: new Date().toISOString(),
        };
        addMessage(userMessage);

        if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
          wsRef.current.send(
            JSON.stringify({
              type: 'message',
              content,
              timestamp: new Date().toISOString(),
            })
          );
        } else {
          console.warn('WebSocket not connected, falling back to HTTP');
          const response = await axiosClient.post('/chat', { message: content });
          if (response.data.data) {
            const botMessage: ChatMessage = {
              id: (Date.now() + 1).toString(),
              sender: 'bot',
              content: response.data.data.reply || '',
              timestamp: new Date().toISOString(),
              metadata: {
                intent: response.data.data.intent,
                data: response.data.data.data,
              },
            };
            addMessage(botMessage);
          }
        }
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Failed to send message';
        setError(errorMessage);
      } finally {
        setLoading(false);
      }
    },
    [addMessage, setError, setLoading] 
  );

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    clearMessages,
  };
};
