import 'package:flutter/material.dart';
import '../services/websocket_service.dart';
import '../models/message.dart';
import '../widgets/message_bubble.dart';
import '../widgets/typing_indicator.dart';
import 'dart:async';

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final WebSocketService _socketService = WebSocketService();
  final TextEditingController _messageController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final List<Message> _messages = [];
  bool _isTyping = false;
  bool _isConnected = false;
  bool _isConnecting = false;

  String _messageBuffer = '';
  Timer? _bufferTimer;

  @override
  void initState() {
    super.initState();
  }

  void _connectToSocket() {
    if (_socketService.isConnecting || _socketService.isConnected) {
      print('⏭️ Đã kết nối hoặc đang kết nối');
      return;
    }

    setState(() {
      _isConnecting = true;
    });

    _socketService.connect(
      onMessage: (message) {
        if (mounted) {
          if (_messageBuffer.isEmpty) {
            _messageBuffer = message;
          } else {
            _messageBuffer += '\n$message';
          }

          _bufferTimer?.cancel();

          _bufferTimer = Timer(const Duration(milliseconds: 500), () {
            if (mounted && _messageBuffer.isNotEmpty) {
              setState(() {
                _isTyping = false;
                _messages.add(
                  Message(
                    text: _messageBuffer,
                    isUser: false,
                    timestamp: DateTime.now(),
                  ),
                );
                _messageBuffer = '';
              });
              _scrollToBottom();
            }
          });
        }
      },
      onConnected: () {
        if (mounted) {
          setState(() {
            _isConnected = true;
            _isConnecting = false;
          });
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Đã kết nối với chatbot'),
              backgroundColor: Colors.green,
              duration: Duration(seconds: 2),
            ),
          );
        }
      },
      onError: (error) {
        if (mounted) {
          setState(() {
            _isConnecting = false;
          });

          if (_socketService.reconnectAttempts <= 1) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text('✗ $error'),
                backgroundColor: Colors.red,
                duration: const Duration(seconds: 3),
                action: SnackBarAction(
                  label: 'Thử lại',
                  textColor: Colors.white,
                  onPressed: () => _socketService.retry(),
                ),
              ),
            );
          }
        }
      },
      onDisconnected: () {
        if (mounted) {
          setState(() {
            _isConnected = false;
            _isConnecting = false;
          });
        }
      },
    );
  }

  void _sendMessage() {
    final text = _messageController.text.trim();
    if (text.isEmpty) return;

    if (!_isConnected) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: const Text('Chưa kết nối. Vui lòng kết nối trước.'),
          backgroundColor: Colors.orange,
          action: SnackBarAction(
            label: 'Kết nối',
            textColor: Colors.white,
            onPressed: _connectToSocket,
          ),
        ),
      );
      return;
    }

    setState(() {
      _messages.add(
        Message(text: text, isUser: true, timestamp: DateTime.now()),
      );
      _isTyping = true;
    });

    _messageController.clear();
    _scrollToBottom();
    _socketService.sendMessage(text);
  }

  void _scrollToBottom() {
    Future.delayed(const Duration(milliseconds: 100), () {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  void dispose() {
    _socketService.disconnect();
    _messageController.dispose();
    _scrollController.dispose();
    _bufferTimer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        elevation: 0,
        title: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: theme.colorScheme.primaryContainer,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Icon(
                Icons.travel_explore,
                color: theme.colorScheme.primary,
              ),
            ),
            const SizedBox(width: 12),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Trợ Lý Du Lịch',
                  style: theme.textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
                Row(
                  children: [
                    Container(
                      width: 8,
                      height: 8,
                      decoration: BoxDecoration(
                        color: _isConnected
                            ? Colors.green
                            : (_isConnecting ? Colors.orange : Colors.grey),
                        shape: BoxShape.circle,
                      ),
                    ),
                    const SizedBox(width: 4),
                    Text(
                      _isConnecting
                          ? 'Đang kết nối...'
                          : (_isConnected ? 'Đang hoạt động' : 'Chưa kết nối'),
                      style: theme.textTheme.bodySmall,
                    ),
                  ],
                ),
              ],
            ),
          ],
        ),
        actions: [
          if (!_isConnected && !_isConnecting)
            IconButton(
              icon: const Icon(Icons.wifi),
              onPressed: _connectToSocket,
              tooltip: 'Kết nối',
            ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: _messages.isEmpty
                ? Center(
                    child: _isConnected
                        ? Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(
                                Icons.chat_bubble_outline,
                                size: 80,
                                color: theme.colorScheme.primary.withOpacity(
                                  0.3,
                                ),
                              ),
                              const SizedBox(height: 16),
                              Text(
                                'Xin chào! 👋',
                                style: theme.textTheme.headlineSmall?.copyWith(
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              const SizedBox(height: 8),
                              Text(
                                'Tôi có thể giúp bạn lên kế hoạch du lịch',
                                style: theme.textTheme.bodyLarge?.copyWith(
                                  color: theme.colorScheme.onSurface
                                      .withOpacity(0.6),
                                ),
                              ),
                              const SizedBox(height: 24),
                              Wrap(
                                spacing: 8,
                                runSpacing: 8,
                                alignment: WrapAlignment.center,
                                children: [
                                  _suggestChip('Địa điểm du lịch nổi tiếng'),
                                  _suggestChip('Khách sạn giá tốt'),
                                  _suggestChip('Món ăn đặc sản'),
                                ],
                              ),
                            ],
                          )
                        : Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(
                                Icons.wifi_off,
                                size: 80,
                                color: theme.colorScheme.error.withOpacity(0.5),
                              ),
                              const SizedBox(height: 16),
                              Text(
                                'Chưa kết nối',
                                style: theme.textTheme.headlineSmall?.copyWith(
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              const SizedBox(height: 8),
                              Text(
                                'Vui lòng kết nối để bắt đầu trò chuyện',
                                style: theme.textTheme.bodyLarge?.copyWith(
                                  color: theme.colorScheme.onSurface
                                      .withOpacity(0.6),
                                ),
                                textAlign: TextAlign.center,
                              ),
                              const SizedBox(height: 24),
                              FilledButton.icon(
                                onPressed: _isConnecting
                                    ? null
                                    : _connectToSocket,
                                icon: _isConnecting
                                    ? const SizedBox(
                                        width: 20,
                                        height: 20,
                                        child: CircularProgressIndicator(
                                          strokeWidth: 2,
                                          color: Colors.white,
                                        ),
                                      )
                                    : const Icon(Icons.wifi),
                                label: Text(
                                  _isConnecting
                                      ? 'Đang kết nối...'
                                      : 'Kết nối ngay',
                                ),
                                style: FilledButton.styleFrom(
                                  padding: const EdgeInsets.symmetric(
                                    horizontal: 32,
                                    vertical: 16,
                                  ),
                                ),
                              ),
                            ],
                          ),
                  )
                : ListView.builder(
                    controller: _scrollController,
                    padding: const EdgeInsets.all(16),
                    itemCount: _messages.length + (_isTyping ? 1 : 0),
                    itemBuilder: (context, index) {
                      if (index == _messages.length && _isTyping) {
                        return const TypingIndicator();
                      }
                      return MessageBubble(message: _messages[index]);
                    },
                  ),
          ),
          Container(
            decoration: BoxDecoration(
              color: theme.colorScheme.surface,
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.05),
                  blurRadius: 10,
                  offset: const Offset(0, -2),
                ),
              ],
            ),
            padding: const EdgeInsets.all(16),
            child: SafeArea(
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _messageController,
                      decoration: InputDecoration(
                        hintText: 'Nhập tin nhắn...',
                        filled: true,
                        fillColor: theme.colorScheme.surfaceVariant,
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(24),
                          borderSide: BorderSide.none,
                        ),
                        contentPadding: const EdgeInsets.symmetric(
                          horizontal: 20,
                          vertical: 12,
                        ),
                      ),
                      textInputAction: TextInputAction.send,
                      onSubmitted: (_) => _sendMessage(),
                      enabled: _isConnected,
                    ),
                  ),
                  const SizedBox(width: 8),
                  FilledButton(
                    onPressed: _isConnected ? _sendMessage : null,
                    style: FilledButton.styleFrom(
                      padding: const EdgeInsets.all(16),
                      shape: const CircleBorder(),
                    ),
                    child: const Icon(Icons.send),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _suggestChip(String label) {
    return ActionChip(
      label: Text(label),
      onPressed: _isConnected
          ? () {
              _messageController.text = label;
              _sendMessage();
            }
          : null,
    );
  }
}
