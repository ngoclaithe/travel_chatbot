import 'dart:async';
import 'dart:convert';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

class WebSocketService {
  WebSocketChannel? _channel;
  Timer? _reconnectTimer;
  Timer? _pingTimer;

  int _reconnectAttempts = 0;
  final int _maxReconnectAttempts = 5;
  bool _isConnecting = false;
  bool _isManualDisconnect = false;

  Function(String)? _onMessage;
  Function()? _onConnected;
  Function(String)? _onError;
  Function()? _onDisconnected;

  bool get isConnected => _channel != null;
  bool get isConnecting => _isConnecting;
  int get reconnectAttempts => _reconnectAttempts;

  void connect({
    required Function(String) onMessage,
    required Function() onConnected,
    required Function(String) onError,
    Function()? onDisconnected,
  }) {
    _onMessage = onMessage;
    _onConnected = onConnected;
    _onError = onError;
    _onDisconnected = onDisconnected;

    _connectWebSocket();
  }

  void _connectWebSocket() {
    if (_isConnecting || (_channel != null)) {
      print('⏭️ Đã kết nối hoặc đang kết nối');
      return;
    }

    _isConnecting = true;
    _isManualDisconnect = false;

    try {
      final socketUrl =
          dotenv.env['SOCKET_URL'] ?? 'ws://localhost:8000/ws/chat';
      print('🔗 Đang kết nối tới: $socketUrl');

      _channel = WebSocketChannel.connect(Uri.parse(socketUrl));

      // Gửi init message
      _channel!.sink.add(jsonEncode({'type': 'init'}));

      // Lắng nghe tin nhắn
      _channel!.stream.listen(
        _handleMessage,
        onError: _handleError,
        onDone: _handleDisconnect,
        cancelOnError: false,
      );

      // Thành công
      _isConnecting = false;
      _reconnectAttempts = 0;
      _onConnected?.call();
      print('✅ Đã kết nối WebSocket');

      // Bắt đầu ping để giữ kết nối
      _startPingTimer();
    } catch (e) {
      _isConnecting = false;
      print('💥 Lỗi kết nối: $e');
      _onError?.call('Không thể kết nối: $e');
    }
  }

  void _handleMessage(dynamic message) {
    try {
      final data = jsonDecode(message);
      final type = data['type'] ?? '';

      // Xử lý ping/pong
      if (type == 'ping') {
        _channel?.sink.add(jsonEncode({'type': 'pong'}));
        return;
      }

      // Xử lý init acknowledgment
      if (type == 'init_ack') {
        print('✅ Server đã xác nhận kết nối: ${data['content']}');
        return;
      }

      // Xử lý lỗi từ server
      if (type == 'error') {
        _onError?.call(data['content'] ?? 'Lỗi từ server');
        return;
      }

      // Xử lý tin nhắn thông thường
      if (type == 'message') {
        _onMessage?.call(data['content'] ?? message.toString());
        return;
      }

      // Tin nhắn khác
      _onMessage?.call(data['content'] ?? message.toString());
    } catch (e) {
      print('⚠️ Lỗi parse message: $e');
      // Nếu không parse được JSON, gửi raw message
      _onMessage?.call(message.toString());
    }
  }

  void _handleError(error) {
    _isConnecting = false;

    if (_reconnectAttempts == 0 || _reconnectAttempts % 5 == 0) {
      print('💥 WebSocket error: $error');
    }

    if (!_isManualDisconnect) {
      _onError?.call('Lỗi kết nối: $error');
    }
  }

  void _handleDisconnect() {
    _isConnecting = false;
    print('🔻 WebSocket đã đóng');

    _stopPingTimer();
    _channel = null;
    _onDisconnected?.call();

    // Tự động reconnect nếu không phải disconnect thủ công
    if (!_isManualDisconnect && _reconnectAttempts < _maxReconnectAttempts) {
      _scheduleReconnect();
    } else if (_reconnectAttempts >= _maxReconnectAttempts) {
      _onError?.call(
        'Không thể kết nối sau $_maxReconnectAttempts lần thử. Vui lòng thử lại sau.',
      );
    }
  }

  void _scheduleReconnect() {
    // Exponential backoff: 1s, 2s, 4s, 8s, 16s, max 30s
    final backoffDelay = (1 << _reconnectAttempts).clamp(1, 30);
    _reconnectAttempts++;

    if (_reconnectAttempts == 1) {
      _onError?.call('Mất kết nối. Đang thử kết nối lại...');
    }

    print(
      '⏳ Thử kết nối lại sau ${backoffDelay}s (lần thử $_reconnectAttempts)',
    );

    _reconnectTimer?.cancel();
    _reconnectTimer = Timer(Duration(seconds: backoffDelay), () {
      _connectWebSocket();
    });
  }

  void _startPingTimer() {
    _stopPingTimer();
    // Gửi ping mỗi 30 giây để giữ kết nối
    _pingTimer = Timer.periodic(const Duration(seconds: 30), (timer) {
      if (_channel != null) {
        try {
          _channel!.sink.add(jsonEncode({'type': 'ping'}));
        } catch (e) {
          print('⚠️ Lỗi gửi ping: $e');
        }
      }
    });
  }

  void _stopPingTimer() {
    _pingTimer?.cancel();
    _pingTimer = null;
  }

  void sendMessage(String message) {
    if (_channel == null) {
      _onError?.call('Chưa kết nối. Vui lòng kết nối trước.');
      return;
    }

    try {
      final data = jsonEncode({
        'type': 'message',
        'content': message,
        'timestamp': DateTime.now().toIso8601String(),
      });
      _channel!.sink.add(data);
    } catch (e) {
      print('💥 Lỗi gửi tin nhắn: $e');
      _onError?.call('Không thể gửi tin nhắn: $e');
    }
  }

  void disconnect() {
    print('🧹 Đóng kết nối WebSocket');
    _isManualDisconnect = true;

    _reconnectTimer?.cancel();
    _reconnectTimer = null;

    _stopPingTimer();

    _channel?.sink.close();
    _channel = null;

    _reconnectAttempts = 0;
    _isConnecting = false;
  }

  void retry() {
    print('🔄 Thử kết nối lại thủ công');
    _reconnectAttempts = 0;
    disconnect();

    // Đợi một chút trước khi kết nối lại
    Future.delayed(const Duration(milliseconds: 500), () {
      _connectWebSocket();
    });
  }
}
