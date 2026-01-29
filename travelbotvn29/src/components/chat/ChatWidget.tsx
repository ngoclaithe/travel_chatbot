'use client';

import React, { useEffect, useRef } from 'react';
import { X, MessageCircle } from 'lucide-react';
import { useChat } from '@/hooks/useChat';
import { useUIStore } from '@/store/uiStore';
import { ChatMessage } from './ChatMessage';
import { MessageInput } from './MessageInput';

export const ChatWidget: React.FC = () => {
  const { isChatOpen, toggleChat, closeChat } = useUIStore();
  const { messages, isLoading, error, sendMessage } = useChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  if (!isChatOpen) {
    return (
      <button
        onClick={toggleChat}
        className="fixed bottom-6 right-6 z-40 w-14 h-14 bg-ocean-blue hover:bg-ocean-dark text-white rounded-full flex items-center justify-center shadow-lg transition-all hover:scale-110"
      >
        <MessageCircle className="w-6 h-6" />
      </button>
    );
  }

  return (
    <div className="fixed bottom-6 right-6 z-40 w-96 h-[600px] flex flex-col bg-white dark:bg-dark-gray rounded-lg shadow-2xl border border-border">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-border bg-ocean-blue text-white rounded-t-lg">
        <div>
          <h3 className="font-semibold text-lg">Travelbot</h3>
          <p className="text-xs opacity-80">Always here to help</p>
        </div>
        <button
          onClick={closeChat}
          className="p-1 hover:bg-ocean-dark rounded transition-colors"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 bg-white dark:bg-card">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center">
            <MessageCircle className="w-12 h-12 text-muted-foreground mb-3 opacity-50" />
            <p className="text-muted-foreground">
              Hi! How can we help you today?
            </p>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}
            {error && (
              <div className="bg-destructive/10 border border-destructive text-destructive p-3 rounded mb-4 text-sm">
                {error}
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Input */}
      <MessageInput onSend={sendMessage} isLoading={isLoading} />
    </div>
  );
};
